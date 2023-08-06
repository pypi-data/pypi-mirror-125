# Copyright Kevin Deldycke <kevin@deldycke.com> and contributors.
# All Rights Reserved.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import re

import pytest
import simplejson as json
from boltons.iterutils import flatten
from boltons.strutils import strip_ansi

from .. import __version__
from ..cli import RENDERING_MODES
from ..pool import DEFAULT_MANAGER_IDS

""" Common tests for all CLI basic features and templates for subcommands. """


TEST_CONF_FILE = """
    # Comment

    top_level_param = "to_ignore"

    [mpm]
    verbosity = "DEBUG"
    blahblah = 234
    manager = ["pip", "npm", "gem"]

    [garbage]

    [mpm.search]
    exact = true
    dummy_parameter = 3
    """


class TestBaseCLI:

    """This collection is testing basic CLI behavior shared by all
    subcommands.

    Also regroups tests not involving subcommands.

    Also includes a bunch of tests performed once on an arbitrary sub-command,
    for situation when the tested behavior is shared by all subcommands. The
    arbitrary sub-command is `managers`, as it is a safe read-only operation
    supposed to work on all platforms, whatever the environment.
    """

    def test_conf_file_overrides_defaults(self, invoke, create_toml):
        conf_path = create_toml("conf.toml", TEST_CONF_FILE)
        result = invoke("--config", str(conf_path), "managers", color=False)
        assert result.exit_code == 0
        assert " │ pip │ " in result.stdout
        assert " │ npm │ " in result.stdout
        assert " │ gem │ " in result.stdout
        assert "brew" not in result.stdout
        assert "cask" not in result.stdout
        assert "debug: " in result.stderr

    def test_conf_file_cli_override(self, invoke, create_toml):
        conf_path = create_toml("conf.toml", TEST_CONF_FILE)
        result = invoke(
            "--config",
            str(conf_path),
            "--verbosity",
            "CRITICAL",
            "managers",
            color=False,
        )
        assert result.exit_code == 0
        assert " │ pip │ " in result.stdout
        assert " │ npm │ " in result.stdout
        assert " │ gem │ " in result.stdout
        assert "brew" not in result.stdout
        assert "cask" not in result.stdout
        assert "error: " not in result.stderr
        assert "warning: " not in result.stderr
        assert "info: " not in result.stderr
        assert "debug: " not in result.stderr


class CLISubCommandTests:

    """All these tests runs on each subcommand.

    This class doesn't starts with `Test` as it is meant to be used as a
    template, inherited by sub-command specific test cases.
    """

    @pytest.mark.parametrize("opt_stats", ("--stats", "--no-stats", None))
    def test_stats(self, invoke, subcmd, opt_stats):
        """Test the result on all combinations of optional options."""
        result = invoke(opt_stats, subcmd)
        assert result.exit_code == 0

    strict_selection_match = True
    """All user-selected managers are expected to be reported in CLI output."""

    @classmethod
    def check_manager_selection(
        cls,
        result,
        selected=DEFAULT_MANAGER_IDS,
        reference_set=DEFAULT_MANAGER_IDS,
    ):
        """Check that user-selected managers are found in CLI's output.

        At this stage of the CLI, the order in which the managers are reported doesn't
        matter because:
        * ``<stdout>`` and ``<stderr>`` gets mangled
        * paging is async
        * we may introduce parrallel execution of manager in the future

        This explain the use of ``set()`` everywhere.

        .. todo:

            Parametrize/fixturize signals to pin point output depending on
            subcommand.
        """
        assert isinstance(selected, (list, tuple, frozenset, set))
        assert isinstance(reference_set, (list, tuple, frozenset, set))

        found_managers = set()
        skipped_managers = set()

        # Strip colors to simplify checks.
        stdout = strip_ansi(result.stdout)
        stderr = strip_ansi(result.stderr)

        for mid in reference_set:

            # List of signals indicating a package manager has been retained by
            # the CLI. Roughly sorted from most specific to more forgiving.
            signals = (
                # Common "not found" warning message.
                f"warning: Skip unavailable {mid} manager." in stderr,
                # Common "not implemented" optional command warning message.
                bool(
                    re.search(
                        fr"warning: {mid} does not implement "
                        r"(search|outdated|upgrade|sync|cleanup|install|upgrade_all) "
                        "command.",
                        stderr,
                    )
                ),
                # Stats line at the end of output.
                f"{mid}: " in stdout.splitlines()[-1] if stdout else "",
                # Match output of managers command.
                bool(
                    re.search(
                        fr"\s+│\s+{mid}\s+│\s+(✓|✘).+│\s+(✓|✘)",
                        stdout,
                    )
                ),
                # Sync command.
                f"Sync {mid} package info..." in stderr,
                # Upgrade command.
                f"Updating all outdated packages from {mid}..." in stderr,
                # Cleanup command.
                f"Cleanup {mid}..." in stderr,
                # Log message for backup command.
                f"Dumping packages from {mid}..." in stderr,
                # Restoring message.
                f"Restore {mid} packages..." in stderr,
                # Warning message for restore command.
                f"warning: No [{mid}] section found." in stderr,
                # Install message.
                bool(
                    re.search(
                        fr"Install \S+ package from {mid}...",
                        stderr,
                    )
                ),
                bool(
                    re.search(
                        fr"warning: No \S+ package found on {mid}.",
                        stderr,
                    )
                ),
            )

            if True in signals:
                found_managers.add(mid)
            else:
                skipped_managers.add(mid)

        # Check consistency of reported findings.
        assert len(found_managers) + len(skipped_managers) == len(reference_set)
        assert found_managers.union(skipped_managers) == set(reference_set)

        # Compare managers reported by the CLI and those expected.
        if cls.strict_selection_match:
            assert found_managers == set(selected)
        # Partial reporting of found manager is allowed in certain cases like install
        # command, which is only picking one manager among the user's selection.
        else:
            assert set(found_managers).issubset(selected)

    @pytest.mark.parametrize("selector", ("--manager", "--exclude"))
    def test_invalid_manager_selector(self, invoke, subcmd, selector):
        result = invoke(selector, "unknown", subcmd)
        assert result.exit_code == 2
        assert not result.stdout
        assert "Error: Invalid value for " in result.stderr
        assert selector in result.stderr

    def test_default_all_managers(self, invoke, subcmd):
        """Test all available managers are selected by default."""
        result = invoke(subcmd)
        assert result.exit_code == 0
        self.check_manager_selection(result)

    @pytest.mark.parametrize(
        "args,expected",
        [
            pytest.param(("--manager", "apm"), {"apm"}, id="single_selector"),
            pytest.param(("--manager", "apm") * 2, {"apm"}, id="duplicate_selectors"),
            pytest.param(
                ("--manager", "apm", "--manager", "gem"),
                {"apm", "gem"},
                id="multiple_selectors",
            ),
            pytest.param(
                ("--manager", "gem", "--manager", "apm"),
                {"apm", "gem"},
                id="ordered_selectors",
            ),
            pytest.param(
                ("--exclude", "apm"),
                set(DEFAULT_MANAGER_IDS) - {"apm"},
                id="single_exclusion",
            ),
            pytest.param(
                ("--exclude", "apm") * 2,
                set(DEFAULT_MANAGER_IDS) - {"apm"},
                id="duplicate_exclusions",
            ),
            pytest.param(
                ("--exclude", "apm", "--exclude", "gem"),
                set(DEFAULT_MANAGER_IDS) - {"apm", "gem"},
                id="multiple_exclusions",
            ),
            pytest.param(
                ("--manager", "apm", "--exclude", "gem"),
                {"apm"},
                id="selector_priority_ordered",
            ),
            pytest.param(
                ("--exclude", "gem", "--manager", "apm"),
                {"apm"},
                id="selector_priority_reversed",
            ),
            pytest.param(
                ("--manager", "apm", "--exclude", "apm"),
                set(),
                id="exclusion_override_ordered",
            ),
            pytest.param(
                ("--exclude", "apm", "--manager", "apm"),
                set(),
                id="exclusion_override_reversed",
            ),
        ],
    )
    def test_manager_selection(self, invoke, subcmd, args, expected):
        result = invoke(*args, subcmd)
        assert result.exit_code == 0
        self.check_manager_selection(result, expected)


class CLITableTests:

    """Test subcommands whose output is a configurable table.

    A table output is also allowed to be rendered as JSON.
    """

    # List of all supported rendering modes IDs, their expected output and the other
    # mode they are allowed to conflict with.
    expected_renderings = {
        "ascii": ("---+---", None),
        "csv": (",", None),
        "csv-tab": ("\t", None),
        "double": ("═══╬═══", None),
        "fancy_grid": ("═══╪═══", "psql_unicode"),
        "github": ("---|---", None),
        "grid": ("===+===", "ascii"),
        "html": ("<table>", None),
        "jira": (" || ", None),
        "json": ('": {', None),
        "latex": ("\\hline", None),
        "latex_booktabs": ("\\toprule", None),
        "mediawiki": ('{| class="wikitable" ', "jira"),
        "minimal": ("  ", None),
        "moinmoin": (" ''' || ''' ", "jira"),
        "orgtbl": ("---+---", None),
        "pipe": ("---|:---", None),
        "plain": ("  ", None),
        "psql": ("---+---", None),
        "psql_unicode": ("───┼───", None),
        "rst": ("===  ===", None),
        "simple": ("---  ---", None),
        "textile": (" |_. ", None),
        "tsv": ("\t", None),
        "vertical": ("***[ 1. row ]***", None),
    }

    def test_recognized_modes(self):
        """Check all rendering modes proposed by the table module are
        accounted for."""
        assert RENDERING_MODES == set(self.expected_renderings.keys())

    def test_default_table_rendering(self, invoke, subcmd):
        """Check default rendering is psql_unicode."""
        result = invoke(subcmd)
        assert result.exit_code == 0

        expected = self.expected_renderings["psql_unicode"][0]

        # If no package found, check that no table gets rendered. Else, check
        # the selected mode is indeed rendered in <stdout>, so the CLI result
        # can be grep-ed.
        if result.stdout.startswith("0 package total ("):
            assert expected not in result.stdout
        else:
            assert expected in result.stdout

        assert expected not in result.stderr

    @pytest.mark.parametrize(
        "mode,expected,conflict",
        (pytest.param(*v, id=v[0]) for v in map(flatten, expected_renderings.items())),
    )
    def test_all_table_rendering(self, invoke, subcmd, mode, expected, conflict):
        """Check that from all rendering modes, only the selected one appears
        in <stdout> and only there. Any other mode are not expected neither in
        <stdout> or <stderr>.
        """
        result = invoke("--output-format", mode, subcmd)
        assert result.exit_code == 0

        # If no package found, check that no table gets rendered. Else, check
        # the selected mode is indeed rendered in <stdout>, so the CLI result
        # can be grep-ed.
        if result.stdout.startswith("0 package total ("):
            # CSV mode will match on comma.
            if mode != "csv":
                assert expected not in result.stdout
        else:
            assert expected in result.stdout

        # Collect all possible unique traces from all possible rendering modes.
        unexpected_traces = {
            v[0]
            for v in self.expected_renderings.values()
            # Exclude obvious character sequences shorter than 3 characters to
            # eliminate false negative.
            if len(v[0]) > 2
        }
        # Remove overlapping edge-cases.
        if conflict:
            unexpected_traces.remove(self.expected_renderings[conflict][0])

        for unexpected in unexpected_traces:
            if unexpected != expected:
                # The unexpected trace is not the selected one, it should not
                # appears at all in stdout.
                assert unexpected not in result.stdout
            # Any expected output from all rendering modes must not appears in
            # <stderr>, including the selected one.
            assert unexpected not in result.stderr

    def test_json_debug_output(self, invoke, subcmd):
        """Output is expected to be parseable if read from <stdout> even in
        debug level as these messages are redirected to <stderr>.

        Also checks that JSON output format is not supported by all commands.
        """
        result = invoke("--output-format", "json", "--verbosity", "DEBUG", subcmd)
        assert result.exit_code == 0
        assert "debug:" in result.stderr
        json.loads(result.stdout)
        json.loads(result.output)
        with pytest.raises(json.decoder.JSONDecodeError):
            json.loads(result.stderr)
