#!/bin/bash
# Synchronize the approved runtime files from src/macro/ into the sibling clone.
# This modifies FEM/SelectionSet in the clone; review its Git diff before committing.
set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd -P)"
DEV_DIR="$PROJECT_DIR"
CLONE_DIR="$PROJECT_DIR/../GitHub_FC_macros/FreeCAD-macros"

resolve_path() {
    local path="$1"
    path="${path/#\~/$HOME}"
    if [ "${path#/}" = "$path" ]; then
        path="$PROJECT_DIR/$path"
    fi
    realpath -m "$path"
}

if [ "$#" -gt 0 ]; then
    [ "$#" -eq 2 ] && [ "$1" = "--clone" ] || {
        echo "Usage: $0 [--clone PATH]" >&2
        exit 2
    }
    CLONE_DIR="$(resolve_path "$2")"
fi
RELEASE_DIR="$CLONE_DIR/FEM/SelectionSet"

if ! git -C "$DEV_DIR" rev-parse --show-toplevel >/dev/null 2>&1; then
    echo "Development directory is not a Git repository: $DEV_DIR" >&2
    exit 1
fi
if ! git -C "$CLONE_DIR" rev-parse --show-toplevel >/dev/null 2>&1; then
    echo "GitHub clone is not a Git repository: $CLONE_DIR" >&2
    exit 1
fi
if [ ! -d "$RELEASE_DIR" ]; then
    echo "Clone release directory not found: $RELEASE_DIR" >&2
    exit 1
fi

declare -a SOURCE_FILES=(
    "SelectionSet.FCMacro|SelectionSet.FCMacro"
    "selection_set_core.py|selection_set_core.py"
    "selection_set_tests.py|selection_set_tests.py"
    "highlight_subelements.py|highlight_subelements.py"
    "README.md|README.md"
)

echo "Preparing to synchronize ${#SOURCE_FILES[@]} release files:"
for mapping in "${SOURCE_FILES[@]}"; do
    source_file="${mapping%%|*}"
    target_file="${mapping#*|}"
    if [ ! -f "$DEV_DIR/src/macro/$source_file" ]; then
        echo "Missing development release file: $DEV_DIR/src/macro/$source_file" >&2
        exit 1
    fi
    if [ ! -f "$RELEASE_DIR/$target_file" ]; then
        echo "Missing clone release file: $RELEASE_DIR/$target_file" >&2
        exit 1
    fi
    printf '  %s -> %s\n' \
        "$DEV_DIR/src/macro/$source_file" \
        "$RELEASE_DIR/$target_file"
done

for mapping in "${SOURCE_FILES[@]}"; do
    source_file="${mapping%%|*}"
    target_file="${mapping#*|}"
    echo "Copying $source_file to clone release directory..."
    cp "$DEV_DIR/src/macro/$source_file" "$RELEASE_DIR/$target_file"
done

echo "Verifying synchronized files:"
for mapping in "${SOURCE_FILES[@]}"; do
    source_file="${mapping%%|*}"
    target_file="${mapping#*|}"
    source_hash="$(sha256sum "$DEV_DIR/src/macro/$source_file" | cut -d' ' -f1)"
    target_hash="$(sha256sum "$RELEASE_DIR/$target_file" | cut -d' ' -f1)"
    if [ "$source_hash" != "$target_hash" ]; then
        echo "Hash mismatch after synchronization: $target_file" >&2
        exit 1
    fi
    printf '  synced and verified: %s (SHA-256: %s)\n' "$target_file" "$target_hash"
done

if find "$RELEASE_DIR" -maxdepth 1 -type f \
    \( -name '*.FCStd' -o -name '*.FCBak' -o -name 'selection_set_test_results.txt' \) \
    -print -quit | grep -q .; then
    echo "Warning: generated FreeCAD artifacts exist in the clone release directory." >&2
fi

echo "Release files synchronized and hash-verified:"
for mapping in "${SOURCE_FILES[@]}"; do
    printf '  %s\n' "${mapping#*|}"
done
git -C "$CLONE_DIR" status --short -- FEM/SelectionSet
