# -*- coding: utf-8 -*-
"""
Run the SelectionSet macro and then build test geometry and run tests, after FreeCAD GUI is ready.

The repeatable version-matrix procedure is:

1. From the project root, choose one FreeCAD AppImage explicitly:

   FREECAD_EXIT_AFTER_TESTS=1 \
   ./app/FreeCAD_<version>.AppImage \
   ./src/tools/run_macro_and_tests_at_startup.FCMacro

2. To test the GitHub clone directly, pass its SelectionSet directory through
   the launcher:

   ./src/tools/run_with_gui.sh --source ../GitHub_FC_macros/FreeCAD-macros/FEM/SelectionSet \
       --freecad ./app/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage --exit

3. Preserve `selection_set_test_results.txt`, the two
   `selection_set_debug_export*.log` files, and the FreeCAD console log in a
   version-specific results directory before running another version.
4. Compare the result count, warnings, failures, FEM displacement values, and
   reported FreeCAD build. The process can exit successfully even when an
   individual test fails, so inspect the result file.

The shell launcher in `src/tools/run_with_gui.sh` also accepts:

   ./src/tools/run_with_gui.sh --freecad ./app/FreeCAD_<version>.AppImage --exit

Do not rely on the first `FreeCAD*.AppImage` match when comparing versions.

To run manually or automatically, use one of these methods:

A) Pass script when starting FreeCAD (if your build runs it):
   ./app/FreeCAD_1.0.2-conda-Linux-x86_64-py311.AppImage src/tools/run_macro_and_tests_at_startup.FCMacro

B) Run from FreeCAD after GUI is open: Macro -> Macros -> open this file -> Execute.

C) Run from FreeCAD Python console:
   exec(open("/full/path/to/run_macro_and_tests_at_startup.py").read())
"""
from __future__ import print_function
import os
from pathlib import Path
import sys

_script_path = Path(__file__).resolve()
_script_dir = _script_path.parent
_project_dir = _script_path.parents[1]


def _resolve_path(value, base_dir):
    """Resolve a path relative to the project root unless it is absolute."""
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = base_dir / path
    return path.resolve()


_default_source_dir = _project_dir / "src" / "macro"
_source_dir = _resolve_path(
    os.environ.get("SELECTIONSET_SOURCE_DIR", _default_source_dir),
    _project_dir,
)
_output_dir = _resolve_path(
    os.environ.get("SELECTIONSET_OUTPUT_DIR", _project_dir),
    _project_dir,
)
if not os.path.isdir(_output_dir):
    os.makedirs(_output_dir)
_source_dir_real = os.path.realpath(str(_source_dir))
sys.path = [
    path for path in sys.path
    if os.path.realpath(path or os.curdir) != _source_dir_real
    and os.path.realpath(path or os.curdir) != os.path.realpath(_script_dir)
]
sys.path.insert(0, str(_source_dir))


def run_macro():
    """Load macro (toolbar, buttons)."""
    try:
        import FreeCADGui
        if FreeCADGui.getMainWindow() is None:
            print("[run_macro_and_tests_at_startup] Main window not ready yet, skipping macro.")
            return
    except Exception as e:
        print("[run_macro_and_tests_at_startup] Error checking GUI: %s" % e)
        return
    print("\n[run_macro_and_tests_at_startup] Loading SelectionSet macro...")
    try:
        for module_name in ("selection_set_core", "selection_set_tests"):
            sys.modules.pop(module_name, None)
        path = os.path.join(_source_dir, "SelectionSet.FCMacro")
        with open(path) as f:
            code = compile(f.read(), path, "exec")
        g = globals().copy()
        g["__file__"] = path
        g["__name__"] = "__main__"
        exec(code, g)
        print("[run_macro_and_tests_at_startup] Macro loaded.")
    except Exception as e:
        print("[run_macro_and_tests_at_startup] Failed to load macro: %s" % e)
        import traceback
        traceback.print_exc()


def export_selectionset_debug_properties(target_name_or_label=None, out_path=None):
    """
    Export all properties relevant for debugging SelectionSet/SelectionSetLink (visibility, view, etc.)
    to a text file. If target_name_or_label is given, export that object (match by Name or Label);
    otherwise export all objects whose Label starts with 'SelectionSet ' or 'SelectionSetLink '.
    """
    import FreeCAD
    import FreeCADGui
    import time
    out_path = out_path or os.path.join(_output_dir, "selection_set_debug_export.log")
    lines = []
    lines.append("=== SelectionSet/SelectionSetLink debug export ===")
    lines.append("Time: %s" % time.strftime("%Y-%m-%d %H:%M:%S"))
    try:
        lines.append("FreeCAD version: %s" % (getattr(FreeCAD, "Version", ()) or "?"))
    except Exception:
        lines.append("FreeCAD version: ?")
    doc = FreeCAD.ActiveDocument
    if not doc:
        lines.append("Document: None (no active document)")
        with open(out_path, "w") as f:
            f.write("\n".join(lines))
        return out_path
    lines.append("Document: %s" % doc.Name)
    lines.append("")
    to_export = []
    if target_name_or_label:
        obj = doc.getObject(target_name_or_label)
        if obj:
            to_export.append(obj)
        else:
            for o in doc.Objects:
                if getattr(o, "Label", None) == target_name_or_label:
                    to_export.append(o)
                    break
        if not to_export:
            lines.append("Object not found by Name or Label: %s" % target_name_or_label)
            lines.append("Available objects: %s" % [o.Name for o in doc.Objects])
    else:
        for o in doc.Objects:
            label = getattr(o, "Label", "") or ""
            if label.startswith("SelectionSet ") or label.startswith("SelectionSetLink "):
                to_export.append(o)
    for obj in to_export:
        lines.append("--- Object: %s (Name: %s) ---" % (getattr(obj, "Label", "?"), obj.Name))
        lines.append("TypeId: %s" % getattr(obj, "TypeId", "?"))
        lines.append("")
        lines.append("[DocumentObject / Data tab properties]")
        try:
            for prop in obj.PropertiesList:
                try:
                    val = getattr(obj, prop)
                    if hasattr(val, "x") and hasattr(val, "y") and hasattr(val, "z"):
                        val = "Vector(%.6g, %.6g, %.6g)" % (val.x, val.y, val.z)
                    elif isinstance(val, (list, tuple)) and len(str(val)) > 200:
                        val = "%s (len=%s)" % (type(val).__name__, len(val))
                    lines.append("  %s = %s" % (prop, repr(val)))
                except Exception as e:
                    lines.append("  %s = <error: %s>" % (prop, e))
        except Exception as e:
            lines.append("  (error listing properties: %s)" % e)
        lines.append("")
        vo = getattr(obj, "ViewObject", None)
        if vo is None:
            lines.append("[ViewObject] None (no GUI)")
        else:
            lines.append("[ViewObject / View tab properties]")
            try:
                for prop in vo.PropertiesList:
                    try:
                        val = getattr(vo, prop)
                        if hasattr(val, "x") and hasattr(val, "y") and hasattr(val, "z"):
                            val = "Vector(%.6g, %.6g, %.6g)" % (val.x, val.y, val.z)
                        lines.append("  %s = %s" % (prop, repr(val)))
                    except Exception as e:
                        lines.append("  %s = <error: %s>" % (prop, e))
            except Exception as e:
                lines.append("  (error listing properties: %s)" % e)
            lines.append("  ViewObject type: %s" % type(vo).__name__)
            proxy = getattr(vo, "Proxy", None)
            lines.append("  ViewObject.Proxy: %s" % (type(proxy).__name__ if proxy is not None else "None"))
            try:
                gui_doc = FreeCADGui.ActiveDocument
                if gui_doc and hasattr(gui_doc, "getViewObject"):
                    gui_vo = gui_doc.getViewObject(obj.Name)
                    lines.append("  FreeCADGui.ActiveDocument.getViewObject(%s): %s" % (
                        repr(obj.Name), "None" if gui_vo is None else "present"))
                    if gui_vo is not None:
                        lines.append("  GUI ViewObject.Visibility = %s" % getattr(gui_vo, "Visibility", "?"))
            except Exception as e:
                lines.append("  (GUI getViewObject error: %s)" % e)
        lines.append("")
    with open(out_path, "w") as f:
        f.write("\n".join(lines))
    print("[run_macro_and_tests_at_startup] Debug export written to: %s" % out_path)
    return out_path


def run_build_and_tests():
    """Build test geometry and run the test suite."""
    print("\n[run_macro_and_tests_at_startup] Building test geometry and running tests...")
    try:
        # Activate FEM workbench so Fem::FemAnalysis and Fem::ConstraintFixed are registered (needed for Test FEM)
        import FreeCADGui
        try:
            FreeCADGui.activateWorkbench("FemWorkbench")
        except Exception:
            pass
        import selection_set_tests
        import selection_set_core
        print("[run_macro_and_tests_at_startup] Source directory: %s" % _source_dir)
        print("[run_macro_and_tests_at_startup] selection_set_core: %s" % selection_set_core.__file__)
        print("[run_macro_and_tests_at_startup] selection_set_tests: %s" % selection_set_tests.__file__)
        if not os.path.realpath(selection_set_core.__file__).startswith(_source_dir_real + os.sep):
            raise RuntimeError("selection_set_core loaded outside source directory: %s" % selection_set_core.__file__)
        if not os.path.realpath(selection_set_tests.__file__).startswith(_source_dir_real + os.sep):
            raise RuntimeError("selection_set_tests loaded outside source directory: %s" % selection_set_tests.__file__)
        selection_set_tests.build_all_test_geometry()
        result = selection_set_tests.run_selectionset_tests()
        # Export debug properties for SelectionSet/SelectionSetLink unless disabled (set env SELECTIONSET_SKIP_DEBUG_EXPORT=1 to skip)
        if not os.environ.get("SELECTIONSET_SKIP_DEBUG_EXPORT"):
            try:
                export_selectionset_debug_properties("Test10_Faces_Coordinates_Face6")
                export_selectionset_debug_properties(None, out_path=os.path.join(_output_dir, "selection_set_debug_export_all.log"))
            except Exception as ex:
                print("[run_macro_and_tests_at_startup] Debug export failed: %s" % ex)
        print("[run_macro_and_tests_at_startup] Done. Check %s for results." % os.path.join(_output_dir, "selection_set_test_results.txt"))
        # Append summary to Report view after a delay so it appears at the very bottom (FEM/CalculiX/SelectionSetLink often flush to Report view later)
        from PySide import QtCore
        _r = result  # capture for closure
        QtCore.QTimer.singleShot(2000, lambda: selection_set_tests.append_test_summary_to_report(*_r))
    except Exception as e:
        print("[run_macro_and_tests_at_startup] Tests failed: %s" % e)
        import traceback
        traceback.print_exc()
    if os.environ.get("FREECAD_EXIT_AFTER_TESTS"):
        from PySide import QtCore
        def do_exit():
            import FreeCAD
            try:
                if FreeCAD.ActiveDocument:
                    FreeCAD.closeDocument(FreeCAD.ActiveDocument.Name)
            except Exception:
                pass
            # Close FreeCAD: try Qt app quit first, then main window close
            app = QtCore.QCoreApplication.instance()
            if app:
                app.quit()
            else:
                try:
                    import FreeCADGui
                    mw = FreeCADGui.getMainWindow()
                    if mw:
                        mw.close()
                except Exception:
                    pass
        QtCore.QTimer.singleShot(3500, do_exit)
        print("[run_macro_and_tests_at_startup] FreeCAD will close in 3.5 s (FREECAD_EXIT_AFTER_TESTS).")


def try_schedule():
    """Wait for main window then schedule macro and tests."""
    import FreeCADGui
    from PySide import QtCore
    if FreeCADGui.getMainWindow() is None:
        QtCore.QTimer.singleShot(300, try_schedule)
        return
    print("[run_macro_and_tests_at_startup] Main window ready. Scheduling macro (1.5s) and tests (4.5s).")
    QtCore.QTimer.singleShot(1500, run_macro)
    QtCore.QTimer.singleShot(4500, run_build_and_tests)


if __name__ == "__main__":
    try:
        import FreeCADGui
    except ImportError:
        print("FreeCADGui not available (console mode?). Run this script from FreeCAD GUI: Macro -> Execute.")
        sys.exit(1)
    from PySide import QtCore
    # Poll until main window exists, then schedule macro and tests
    QtCore.QTimer.singleShot(500, try_schedule)
    print("[run_macro_and_tests_at_startup] Started. Waiting for main window...")
