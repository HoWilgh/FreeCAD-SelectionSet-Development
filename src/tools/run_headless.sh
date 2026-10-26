#!/bin/bash
# Run the SelectionSet headless test (Test 9c debug) using an AppImage in app/.
#
# AppImages are stored in ../../app/, e.g.:
#   ../../app/FreeCAD_1.0.2-conda-Linux-x86_64-py311.AppImage
# Then run: ./run_headless.sh
#
# Output is printed and written to test9c_headless_output.txt in this folder.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_DIR"

APPIMAGE=""
if [ -x "$PROJECT_DIR/app/FreeCAD_1.0.2-conda-Linux-x86_64-py311.AppImage" ] || [ -f "$PROJECT_DIR/app/FreeCAD_1.0.2-conda-Linux-x86_64-py311.AppImage" ]; then
    APPIMAGE="$PROJECT_DIR/app/FreeCAD_1.0.2-conda-Linux-x86_64-py311.AppImage"
else
    for f in "$PROJECT_DIR"/app/FreeCAD*.AppImage; do
        [ -f "$f" ] && APPIMAGE="$f" && break
    done
fi

if [ -z "$APPIMAGE" ]; then
    echo "No FreeCAD AppImage found in: $PROJECT_DIR/app"
    echo "Put an AppImage in $PROJECT_DIR/app and make it executable (chmod +x)."
    exit 1
fi

# Pass script as argument (FreeCAD runs it and exits). Use -c only for interactive console.
"$APPIMAGE" "$SCRIPT_DIR/run_tests_headless.py"
exit $?
