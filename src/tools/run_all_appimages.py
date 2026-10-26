#!/usr/bin/env python3
"""Run the GUI compatibility suite against every FreeCAD AppImage in ``app/``.

The script delegates each run to ``run_with_gui.sh`` so source selection,
timestamped output folders, and FreeCAD startup behavior remain centralized.
It parses each generated result summary and prints one release-readiness report.
"""

from __future__ import annotations

import argparse
import datetime
import pathlib
import re
import subprocess
import sys
from typing import List, Optional, Tuple


SUMMARY_PATTERN = re.compile(
    r"Tests complete\.\s+(\d+) passed,\s+(\d+) failed out of (\d+) total tests\."
)
KNOWN_GMSH_FAILURE = "GMSH did not generate mesh (with hole)"
REQUIRED_SOURCE_FILES = (
    "SelectionSet.FCMacro",
    "selection_set_core.py",
    "selection_set_tests.py",
)


def _project_dir() -> pathlib.Path:
    """Return the development repository root."""
    return pathlib.Path(__file__).resolve().parents[2]


def _resolve_path(path: pathlib.Path, base_dir: pathlib.Path) -> pathlib.Path:
    """Resolve a path, interpreting relative paths below the supplied base directory."""
    expanded_path = pathlib.Path(path).expanduser()
    if not expanded_path.is_absolute():
        expanded_path = base_dir / expanded_path
    return expanded_path.resolve()


def _validate_source(source_dir: pathlib.Path) -> Optional[str]:
    """Return a diagnostic if a source directory is not a complete macro source."""
    missing_files = [
        filename
        for filename in REQUIRED_SOURCE_FILES
        if not (source_dir / filename).is_file()
    ]
    if missing_files:
        return "missing required file(s): %s" % ", ".join(missing_files)
    return None


def _source_label(project_dir: pathlib.Path, source_dir: pathlib.Path) -> str:
    """Return a stable results label for the selected source directory."""
    development_source = (project_dir / "src" / "macro").resolve()
    clone_source = (
        project_dir.parent / "GitHub_FC_macros" / "FreeCAD-macros" / "FEM" / "SelectionSet"
    ).resolve()
    if source_dir == development_source:
        return "development"
    if source_dir == clone_source:
        return "clone"
    return "external"


def _result_summary(result_root: pathlib.Path) -> Optional[pathlib.Path]:
    """Return the newest test-summary file below a launcher result root."""
    summaries = sorted(
        result_root.glob("*/selection_set_test_results.txt"),
        key=lambda path: path.stat().st_mtime,
    )
    return summaries[-1] if summaries else None


def _classify(
    passed: int,
    failed: int,
    total: int,
    summary_text: str,
    appimage_name: str,
) -> str:
    """Classify one compatibility result for the final report."""
    if failed == 0 and passed == total:
        return "PASS"
    if (
        "1.0.2" in appimage_name
        and failed == 1
        and KNOWN_GMSH_FAILURE in summary_text
    ):
        return "KNOWN GMSH LIMITATION"
    return "UNEXPECTED FAILURE"


def _run_appimage(
    launcher: pathlib.Path,
    appimage: pathlib.Path,
    source_dir: pathlib.Path,
    result_root: pathlib.Path,
) -> Tuple[str, str, str, int, Optional[pathlib.Path]]:
    """Run one AppImage and return its report fields."""
    result_root.mkdir(parents=True, exist_ok=True)
    command = [
        str(launcher),
        "--freecad",
        str(appimage),
        "--source",
        str(source_dir),
        "--results",
        str(result_root),
        "--exit",
    ]
    log_path = result_root / "launcher.log"
    with log_path.open("w", encoding="utf-8") as log_file:
        completed = subprocess.run(
            command,
            cwd=str(_project_dir()),
            stdout=log_file,
            stderr=subprocess.STDOUT,
            check=False,
        )
    summary_path = _result_summary(result_root)
    if summary_path is None:
        return appimage.name, "launcher produced no test summary", "UNEXPECTED FAILURE", completed.returncode, None
    summary_text = summary_path.read_text(encoding="utf-8", errors="replace")
    match = SUMMARY_PATTERN.search(summary_text)
    if match is None:
        return appimage.name, "unrecognized test summary", "UNEXPECTED FAILURE", completed.returncode, summary_path
    passed, failed, total = (int(value) for value in match.groups())
    status = _classify(passed, failed, total, summary_text, appimage.name)
    counts = "%d passed, %d failed, %d total" % (passed, failed, total)
    if completed.returncode != 0 and status == "PASS":
        status = "UNEXPECTED FAILURE"
        counts += ", launcher exit %d" % completed.returncode
    return appimage.name, counts, status, completed.returncode, summary_path


def main() -> int:
    """Run all available AppImages and print a compatibility summary."""
    parser = argparse.ArgumentParser(
        description="Run the SelectionSet compatibility suite against every FreeCAD AppImage."
    )
    parser.add_argument(
        "--source",
        type=pathlib.Path,
        help="SelectionSet source directory (default: src/macro).",
    )
    args = parser.parse_args()

    project_dir = _project_dir()
    source_dir = _resolve_path(
        args.source or pathlib.Path("src") / "macro",
        project_dir,
    )
    source_error = _validate_source(source_dir)
    if source_error is not None:
        print(
            "SelectionSet source is invalid: %s" % source_error,
            file=sys.stderr,
        )
        print("Source directory: %s" % source_dir, file=sys.stderr)
        return 2

    appimages = sorted((project_dir / "app").glob("FreeCAD*.AppImage"))
    if not appimages:
        print("No FreeCAD AppImages found in %s" % (project_dir / "app"), file=sys.stderr)
        return 2

    run_id = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    matrix_root = (
        project_dir
        / "results"
        / "automated-matrix"
        / _source_label(project_dir, source_dir)
        / run_id
    )
    launcher = project_dir / "src" / "tools" / "run_with_gui.sh"
    if not launcher.is_file():
        print("Launcher not found: %s" % launcher, file=sys.stderr)
        return 2
    reports: List[Tuple[str, str, str, int, Optional[pathlib.Path]]] = []
    print("Using SelectionSet source: %s" % source_dir)
    for appimage in appimages:
        print("Running %s..." % appimage.name)
        reports.append(
            _run_appimage(
                launcher,
                appimage,
                source_dir,
                matrix_root / appimage.stem,
            )
        )

    print("\nFreeCAD compatibility summary")
    print("=============================")
    print("%-42s %-31s %s" % ("AppImage", "Tests", "Status"))
    for name, counts, status, _, summary_path in reports:
        print("%-42s %-31s %s" % (name, counts, status))
        if summary_path is not None:
            print("  summary: %s" % summary_path)

    unexpected = [report for report in reports if report[2] == "UNEXPECTED FAILURE"]
    if unexpected:
        print("\nOverall: FAIL (unexpected compatibility result)")
        return 1
    if any(report[2] == "KNOWN GMSH LIMITATION" for report in reports):
        print("\nOverall: PASS WITH KNOWN COMPATIBILITY LIMITATION")
    else:
        print("\nOverall: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
