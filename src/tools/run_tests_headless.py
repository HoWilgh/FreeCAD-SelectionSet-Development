#!/usr/bin/env python3
"""
Run SelectionSet logic without GUI to inspect Test 9c (solid filter) output.

Usage (from repo root or from this directory):
  freecad -c src/tools/run_tests_headless.py
  # or, from src/tools/:
  freecad -c run_tests_headless.py

Output is printed to stdout and written to test9c_headless_output.txt in this directory.
Use this to see what get_faces_by_selection_shape returns with solid_filter_list
when Test 9c is broken in the GUI test runner.
"""
from __future__ import print_function
import os
from pathlib import Path
import sys

# Ensure this macro's directory is on the path
_script_dir = Path(__file__).resolve().parent
_project_dir = _script_dir.parents[1]
_macro_dir = _project_dir / "src" / "macro"
if str(_macro_dir) not in sys.path:
    sys.path.insert(0, str(_macro_dir))

def main():
    import FreeCAD
    # Console mode: no GUI; avoid importing FreeCADGui for getMainWindow (would be None)
    output_lines = []

    def log(msg):
        print(msg)
        output_lines.append(msg)

    log("=== SelectionSet headless test (Test 9 / 9c geometry) ===")

    # Build Test 9 geometry (view/fitAll at end may fail in -c mode; geometry is created before that)
    import selection_set_tests
    try:
        boolean_cyl, body003 = selection_set_tests.build_test_3_cylinder_two_halves()
    except Exception as e:
        log("Build raised (expected in -c if Gui view calls fail): %s" % e)
    boolean_cyl = FreeCAD.ActiveDocument.getObject("BooleanFragments_CylTwoHalves")
    body003 = FreeCAD.ActiveDocument.getObject("Body003")
    if not boolean_cyl or not body003:
        log("ERROR: BooleanFragments_CylTwoHalves or Body003 not in document. Run with GUI once to create geometry, or fix build_test_3 for headless.")
        _write_output(output_lines)
        return 1
    log("Using BooleanFragments_CylTwoHalves and Body003.")

    main_obj = boolean_cyl
    selection_shape = body003

    import selection_set_core

    # 1) Faces fully inside (no solid filter) – like Test 9a
    log("\n--- get_faces_by_selection_shape(..., volume_mode='fully_inside', solid_filter_list=None) ---")
    faces_no_filter = selection_set_core.get_faces_by_selection_shape(
        main_obj, selection_shape.Shape, tol=1e-7, volume_mode="fully_inside", solid_filter_list=None
    )
    log("Count: %d" % len(faces_no_filter))
    log("ElementList: %s" % faces_no_filter)

    # 2) Faces fully inside WITH solid filter Solid3 – what Test 9c should give
    solid_filter = ["BooleanFragments_CylTwoHalves.Solid3"]
    log("\n--- get_faces_by_selection_shape(..., volume_mode='fully_inside', solid_filter_list=%s) ---" % solid_filter)
    faces_with_filter = selection_set_core.get_faces_by_selection_shape(
        main_obj, selection_shape.Shape, tol=1e-7, volume_mode="fully_inside", solid_filter_list=solid_filter
    )
    log("Count: %d (expected 3 for one half-sphere)" % len(faces_with_filter))
    log("ElementList: %s" % faces_with_filter)

    # 3) Per-face solid mapping for the faces we got without filter (debug)
    log("\n--- Face -> Solid mapping (for faces from step 1) ---")
    for fe in faces_no_filter:
        solid_name = selection_set_core._get_solid_for_face(main_obj, fe)
        log("  %s -> %s" % (fe, solid_name))

    log("\n=== End headless test ===")
    _write_output(output_lines)
    return 0


def _write_output(output_lines):
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = _script_dir / "test9c_headless_output.txt"
    try:
        with open(out_path, "w") as f:
            f.write("\n".join(output_lines))
        print("(Output also written to %s)" % out_path)
    except Exception as e:
        print("(Could not write file: %s)" % e)


if __name__ == "__main__":
    sys.exit(main())
