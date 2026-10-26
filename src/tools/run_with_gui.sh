#!/bin/bash
# Start FreeCAD and run the SelectionSet macro + build test geometry + run tests (passes .FCMacro so it runs at startup).
#
# Run from this directory or pass an explicit AppImage and source directory:
#   ./run_with_gui.sh --freecad ../../app/FreeCAD_1.0.2-conda-Linux-x86_64-py311.AppImage --exit
#   ./run_with_gui.sh --freecad ../../app/FreeCAD_1.1rc3-Linux-x86_64-py311.AppImage --exit
#   ./run_with_gui.sh --source ../GitHub_FC_macros/FreeCAD-macros/FEM/SelectionSet \
#       --results ../../results/clone-source/FreeCAD_1.1.4 \
#       --freecad ../../app/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage --exit
# Without --freecad, the historical 1.0.2 filename is preferred, followed by
# the first FreeCAD*.AppImage found in the project root.
#
# Without --results, test output is written in the project folder for
# compatibility with the historical workflow. With --results, the launcher
# creates a unique timestamped run folder below the supplied path.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_DIR"

APPIMAGE=""
SOURCE_DIR="$PROJECT_DIR/src/macro"
RESULTS_DIR="$PROJECT_DIR"
HAS_RESULTS_ARG=0
EXIT_AFTER_TESTS=0

resolve_path() {
    local path="$1"
    path="${path/#\~/$HOME}"
    if [ "${path#/}" = "$path" ]; then
        path="$PROJECT_DIR/$path"
    fi
    realpath -m "$path"
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        --freecad)
            [ "$#" -ge 2 ] || { echo "Missing path after --freecad" >&2; exit 2; }
            APPIMAGE="$2"
            shift 2
            ;;
        --source)
            [ "$#" -ge 2 ] || { echo "Missing path after --source" >&2; exit 2; }
            SOURCE_DIR="$2"
            shift 2
            ;;
        --results)
            [ "$#" -ge 2 ] || { echo "Missing path after --results" >&2; exit 2; }
            RESULTS_DIR="$2"
            HAS_RESULTS_ARG=1
            shift 2
            ;;
        --exit)
            EXIT_AFTER_TESTS=1
            shift
            ;;
        *)
            echo "Usage: $0 [--source PATH] [--results PATH] [--freecad PATH] [--exit]" >&2
            exit 2
            ;;
    esac
done

SOURCE_DIR="$(resolve_path "$SOURCE_DIR")"
if [ ! -d "$SOURCE_DIR" ]; then
    echo "SelectionSet source directory not found: $SOURCE_DIR" >&2
    exit 1
fi
for required_file in selection_set_core.py selection_set_tests.py; do
    if [ ! -f "$SOURCE_DIR/$required_file" ]; then
        echo "SelectionSet source is missing required file: $SOURCE_DIR/$required_file" >&2
        exit 1
    fi
done
if [ ! -f "$SOURCE_DIR/SelectionSet.FCMacro" ]; then
    echo "SelectionSet source is missing an entry point: $SOURCE_DIR/SelectionSet.FCMacro" >&2
    exit 1
fi
RESULTS_DIR="$(resolve_path "$RESULTS_DIR")"
if [ "$HAS_RESULTS_ARG" -eq 1 ]; then
    RESULTS_ROOT="$RESULTS_DIR"
    mkdir -p "$RESULTS_ROOT"
    RUN_TIMESTAMP="$(date '+%Y-%m-%d_%H%M%S')"
    RESULTS_DIR="$RESULTS_ROOT/$RUN_TIMESTAMP"
    run_number=1
    while [ -e "$RESULTS_DIR" ]; do
        RESULTS_DIR="$RESULTS_ROOT/${RUN_TIMESTAMP}_$(printf '%02d' "$run_number")"
        run_number=$((run_number + 1))
    done
fi
mkdir -p "$RESULTS_DIR"
if [ -z "$APPIMAGE" ]; then
    if [ -x "$PROJECT_DIR/app/FreeCAD_1.0.2-conda-Linux-x86_64-py311.AppImage" ] || [ -f "$PROJECT_DIR/app/FreeCAD_1.0.2-conda-Linux-x86_64-py311.AppImage" ]; then
        APPIMAGE="$PROJECT_DIR/app/FreeCAD_1.0.2-conda-Linux-x86_64-py311.AppImage"
    else
        for f in "$PROJECT_DIR"/app/FreeCAD*.AppImage; do
            [ -f "$f" ] && APPIMAGE="$f" && break
        done
    fi
fi

if [ -z "$APPIMAGE" ]; then
    echo "No FreeCAD AppImage found in: $PROJECT_DIR/app"
    exit 1
fi
APPIMAGE="$(resolve_path "$APPIMAGE")"
if [ ! -f "$APPIMAGE" ]; then
    echo "FreeCAD AppImage not found: $APPIMAGE" >&2
    exit 1
fi
if [ ! -x "$APPIMAGE" ]; then
    echo "FreeCAD AppImage is not executable: $APPIMAGE" >&2
    exit 1
fi

if [ "$EXIT_AFTER_TESTS" -eq 1 ]; then
    export FREECAD_EXIT_AFTER_TESTS=1
fi

export SELECTIONSET_SOURCE_DIR="$SOURCE_DIR"
export SELECTIONSET_OUTPUT_DIR="$RESULTS_DIR"
echo "Using SelectionSet source: $SOURCE_DIR"
echo "Using SelectionSet output: $RESULTS_DIR"
"$APPIMAGE" "$PROJECT_DIR/src/tools/run_macro_and_tests_at_startup.FCMacro"
exit $?
