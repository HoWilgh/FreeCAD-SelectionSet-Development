# SelectionSet workflow — start here

> `TODO.md` tracks unfinished work.
> `WORKFLOW_STATUS.md` documents the current verified workflow and status.

This folder is the authoritative development, compatibility, and evidence
workspace for the FreeCAD SelectionSet macro. The Git-connected clone is a
separate sibling repository used for release-candidate verification:
`GitHub_FC_macros/FreeCAD-macros/FEM/SelectionSet`.

The Git-connected repository is the separate clone at
`GitHub_FC_macros/FreeCAD-macros`. Files are currently moved between the two
locations manually. Use the clone for GitHub synchronization, commits, and
pushes; use this folder for development, experiments, tests, and local
FreeCAD files.

## Release decisions and naming

- The proposed name for the development repository is
  `FreeCAD-SelectionSet-Development`.
- Keep `selection_set_tests.py` in the release tree for now. The current
  `SelectionSet.FCMacro` imports it for the optional test toolbar, so it is
  currently part of the self-contained runtime package. Reassess this only
  after the test toolbar has been separated from the user-facing macro.
- This repository's root `README.md` is the guide to the development project:
  its tools, tests, AppImages, results, release preparation, and structure.
  The `src/macro/README.md` is a separate, copy-ready guide for users of the
  SelectionSet macro. Do not copy either README over the other.
- The sibling clone is based on upstream `master`. An upstream update of the
  remote `FreeCAD-macros` `master` is probably needed before treating the
  SelectionSet release candidate as current.
- The development source is at macro version **1.1.0**
  (`__version__` in `selection_set_core.py`, `__Version__` in
  `SelectionSet.FCMacro`, `REQUIRED_MACRO_VERSION` in
  `selection_set_tests.py`, and `release/package.xml`). The bump covers the
  1.1.0 feature set: SelectionSet edges mode and SelectionSetLink
  `TargetProperty` (References | Direction) plus the PartDesign FEM beam
  example. The sibling clone still contains the committed 1.0.1
  release-candidate state until the files are synchronized and committed
  there.

### Package metadata preparation

FreeCAD's current Addon Academy describes three mutually exclusive publishing
routes: a portable archive, a repository referenced as a custom Addon Manager
source, or an indexed addon. The independent-repository route is the one
currently prepared here. It requires a final repository URL, maintainer
identity, version and date, a license file, an icon path, and a valid
`package.xml`; the placeholder values in `release/package.xml` must not be
published unchanged. A clean-clone installation test is also required.

If the macro is instead submitted to the official `FreeCAD-macros` repository,
do not add `package.xml`. That route uses single-line metadata in
`SelectionSet.FCMacro`, including `__Name__`, `__Comment__`, `__Author__`,
`__Date__`, `__Version__`, `__License__`, `__Files__`, and the other applicable
fields, with every auxiliary file listed in `__Files__`. The current macro
already has a `__Name__`, `__Version__`, and `__Files__` block, but its
metadata should be completed before submission.

References:

- [FreeCAD Addon Academy: Publishing Your Addon](https://freecad.github.io/Addon-Academy/Guides/Publishing/)
- [FreeCAD-macros submission guidelines](https://github.com/FreeCAD/FreeCAD-macros#guidelines-for-submitting-a-macro)
- [FreeCAD package metadata](https://wiki.freecad.org/Package_Metadata)

## Current status

- The clone is based on remote `master` and contains the committed
  `SelectionSet` 1.0.1 release-candidate changes.
- The remote SelectionSet directory contains:
  - `README.md`
  - `SelectionSet.FCMacro`
  - `highlight_subelements.py`
  - `selection_set_core.py`
  - `selection_set_tests.py`
  - the `icons/` directory
- The clone was restored to its upstream state after the initial source
  isolation experiment. Implementation files are synchronized into it only at
  an explicit release-candidate checkpoint.
- The clone's `README.md` and `icons/` remain the release/upstream copies.
  The development README is not identical and was not overwritten.
- This development folder contains additional local/development material,
  including `src/macro/SelectionSet.FCMacro`, `release/package.xml`, test runners, logs,
  FreeCAD documents, backups, and the `tmp/` directory. These are not all
  part of the remote SelectionSet directory.
- The latest remote `README.md` is therefore not yet present in this
  development folder. Copy it from the clone only when the development copy
  should be updated.

  ## New-user quick start

  This repository is the development and test workspace. The runtime macro files
  are under `src/macro/`; extend the macro implementation in
  `selection_set_core.py`, extend or add regression tests in
  `selection_set_tests.py`, and keep test orchestration and shell helpers under
  `src/tools/`. The sibling `GitHub_FC_macros/FreeCAD-macros` repository is the
  release clone and must be tested separately after synchronization.

  Run the complete 22-test matrix against the development source and every
  AppImage in `app/`:

  ```bash
  python3 src/tools/run_all_appimages.py
  ```

  Run the identical automated matrix against the synchronized clone source:

  ```bash
  python3 src/tools/run_all_appimages.py \
    --source ../GitHub_FC_macros/FreeCAD-macros/FEM/SelectionSet
  ```

  The runner invokes `src/tools/run_with_gui.sh` once per AppImage, validates the
  selected source, and writes results to
  `results/automated-matrix/development/<timestamp>/` or
  `results/automated-matrix/clone/<timestamp>/`. FreeCAD 1.0.2 may report the
  documented GMSH cantilever-with-hole limitation; other failures are unexpected
  and make the runner return a failure status. Older manual and intermediate
  evidence is preserved under `results/archive/`.

  ## Release-file set and test workflow

The release file set is:

- `src/macro/SelectionSet.FCMacro`
- `src/macro/selection_set_core.py`
- `src/macro/selection_set_tests.py`
- `src/macro/highlight_subelements.py`
- `src/macro/icons/`
- `src/macro/README.md`

The complete `src/macro/` directory is the copy-ready user package. Copy its
contents, including `README.md` and `icons/`, into a FreeCAD macro directory.
The startup/test launchers under `src/tools/` are development-side helpers and
are not required for normal macro use.

Development-only files stay outside `src/macro/`: AppImages, logs, results,
FreeCAD documents, backups, local rules, plans, and test launchers.

Develop and run the normal compatibility matrix from this folder. At a
release-candidate checkpoint, synchronize only the approved implementation
files into the sibling clone and then run the tests against the clone source
explicitly:

```bash
./src/tools/run_with_gui.sh \
  --source ../GitHub_FC_macros/FreeCAD-macros/FEM/SelectionSet \
  --results ./results/automated-matrix/clone \
  --freecad ./app/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage \
  --exit
```

The launcher sets `SELECTIONSET_SOURCE_DIR`; the startup runner then imports
the core and test modules and loads `SelectionSet.FCMacro` from that directory.
The launcher also sets `SELECTIONSET_OUTPUT_DIR`; all generated documents,
meshes, solver files, debug exports, and result summaries are written there,
independently of the selected source directory. When `--results PATH` is
provided, the launcher creates a unique timestamped run directory below PATH.
Always use `--results` for clone-source tests so the clone release tree remains
clean. Automated matrix outputs are stored under
`results/automated-matrix/<source>/<timestamp>/`; older evidence is preserved
under `results/archive/`.

The complete local matrix can be run automatically:

```bash
python3 src/tools/run_all_appimages.py
```

The same automation can test the sibling clone:

```bash
python3 src/tools/run_all_appimages.py \
  --source ../GitHub_FC_macros/FreeCAD-macros/FEM/SelectionSet
```

The runner discovers every `app/FreeCAD*.AppImage`, delegates execution to
`src/tools/run_with_gui.sh`, stores each run below
`results/automated-matrix/<source>/<timestamp>/`, parses the generated test
summary, and prints one final report. Pass `--source PATH` to test the
development source or the clone source. The FreeCAD 1.0.2 GMSH
cantilever-with-hole failure is classified as a known limitation; any other
failure is reported as unexpected and produces a nonzero exit status.
Both sources have been tested against all four available AppImages. The
development and clone results are kept in separate source directories below
`results/automated-matrix/`; earlier evidence remains under
`results/archive/`.

Use the clone for Git synchronization and release review. Do not develop in
both repositories simultaneously. Do not push until the clone-source test and
the release-file diff have been reviewed.

Do not use `git pull` in this development folder. It is a separate local
repository without the GitHub remote.

## Release-candidate synchronization

The development entry point `SelectionSet.FCMacro` maps to the release
entry point `SelectionSet.FCMacro` in the clone. The approved implementation
mapping is:

| Development workspace | Clone release directory |
| --- | --- |
| `src/macro/SelectionSet.FCMacro` | `SelectionSet.FCMacro` |
| `src/macro/selection_set_core.py` | `selection_set_core.py` |
| `src/macro/selection_set_tests.py` | `selection_set_tests.py` |
| `src/macro/highlight_subelements.py` | `highlight_subelements.py` |

The clone's `README.md` remains a separately maintained release README; the
copy-ready development README documents the contents of `src/macro/`.
Generated FreeCAD documents,
backups, meshes, solver files, logs, and result summaries must remain outside
the clone.

## Suggested future simplification

The Git-connected clone is the release source under test only after a
deliberate synchronization checkpoint. Keep experiments, FreeCAD documents,
logs, and backups in ignored directories outside the release tree. A small
explicit synchronization script or documented file manifest could later
replace the manual mapping above; it should copy only approved release files,
report missing or extra files, and show a hash comparison before anything is
overwritten.

If a separate development folder is required, add a small explicit
synchronization script or documented file manifest. It should copy only
approved release files, report missing or extra files, and show a hash
comparison before anything is overwritten. Avoid copying the whole folder,
because development-only files can then enter the addon unintentionally.

## Implementation and test evidence

The implementation is split between `selection_set_core.py` and
`selection_set_tests.py`. The core module provides SelectionSet and
SelectionSetLink objects, spatial face/solid selection, fully-inside and
intersection modes, coordinate-point selection, solid filtering, FEM
reference helpers, GUI commands, icons, view providers, observer handling,
macro-version metadata, and document-restoration support.

The test module builds deterministic test geometry and runs assertions against
the stored element names. The intended sequence is:

1. Load the macro, which reloads the core and test modules and adds the main
   and test toolbars.
2. Build the required test geometry on demand.
3. Create or update SelectionSets from the geometry.
4. Recompute the sets and compare their `ElementList` values with the
   authoritative expected values in the test code.
5. Exercise SelectionSetLinks and FEM references.
6. Build and mesh the FEM cantilever example, run CalculiX where available,
   read the results, and check displacement ranges.
7. Write the result summary and optional debug exports.

The automated result file recorded 22 passed tests and 0 failed tests. The
coverage included basic faces and solids, fully-inside and intersection
selection, BooleanFragments, solid filtering, coordinate selection, FEM
objects and links, and three FEM cantilever cases: a cut beam, an uncut beam,
and a cut beam with a 400 mm cylinder radius.

The recorded displacement results were:

- cut beam: 96.1992 mm;
- uncut beam: 88.3911 mm;
- 400 mm radius cut: 375.9298 mm.

These values were accepted within the tolerances used by the test runner.
They are evidence for the recorded runs, not a guarantee for all meshes,
platforms, solver versions, or future FreeCAD releases.

### PartDesign-body examples (fillet topology change)

Two PartDesign variants of the cantilever example exist and are verified:

- The macro-internal example `run_fem_partdesign_beam_example`
  (`src/macro/selection_set_tests.py`, Tests pulldown entry
  **FEM beam example (PartDesign body)**): PartDesign Body (sketch 8000x1000
  + pad 1000), mesh geometry = Body, fillet feature on the long top edge
  (suppressed by default, radius via `PD beam variables`.FilletRadius), direct
  and link-driven constraint references.
- The standalone pair in `src/tools/`:
  `ccx_cantilever_faceload_partdesign.py` (direct references only) and
  `ccx_cantilever_faceload_partdesign_selectionset.py` (SelectionSets,
  SelectionSetLinks, and `renew_selection_references(doc)`), kept structurally
  close to the upstream `ccx_cantilever_faceload.py`.

Verified behaviour (FreeCAD 1.1.4 and 26.3rc2; 21/21 checks each; evidence in
`results/pd-beam-verify/` and `results/pd-cantilever-files-verify/`):

- Introducing the fillet changes the Body face numbering: force face
  `Face2` -> `Face5`, and `Face2` then names the fixed end.
- Direct references break: FreeCAD 1.1 invalidates them (`?Face2`, `?Face4`);
  on 1.0 they may silently resolve to a different face.
- `Update all sets and links` / `renew_selection_references(doc)` restores the
  intended references (force -> x=8000, fixed -> x=0); the mesh geometry stays
  on the Body and GMSH regenerates the fillet shape (27371 nodes recorded).
- GMSH meshing of the plain pad shape also worked in the standalone file
  (9190 nodes recorded).

Direction-edge extension (user-confirmed need: the force Direction edge is a
separate reference that also breaks):

- SelectionSet Mode gained `edges` (coordinates mode via new
  `get_edges_by_point`; volume modes via common-length containment /
  intersection), and SelectionSetLink gained `TargetProperty`
  (`References` default, `Direction` applies the first edge ref to e.g.
  `ConstraintForce.Direction`).
- The PartDesign examples create an edges SelectionSet plus a Direction link
  (`PD_Beam_ForceDirection` / `FEM_PDBeam_Link_ForceDirection`, and
  `Cantilever_ForceDirectionEdge` / `Link_ForceDirection` in the standalone
  file).
- Verified on FreeCAD 1.1.4 and 26.3rc2 (25/25 checks each for the macro
  example and the standalone pair; evidence in `results/pd-direction-verify/`):
  after the fillet the stale Direction retargets (e.g. to `Edge14`) or breaks;
  renewal restores a vertical direction edge at x=8000. The direction edge
  itself was kept on the y=width side (opposite the fillet at y=0), so the
  check asserts the renewal path rather than the exact stale value.

## Recorded FreeCAD runs and logs

The available logs show runs with:

- FreeCAD 1.0.2, Libs 1.0.2R39319 (Git);
- FreeCAD 1.1.0, Libs 1.1.0rc3R20260223 (Git shallow).

Additional verified GUI runs recorded for the PartDesign examples:

- FreeCAD 1.1.4, Libs 1.1.4R20260928 (Git shallow): example and standalone-pair
  verification, 21/21 checks each (`results/pd-beam-verify/FreeCAD_1.1.4_rerun/`,
  `results/pd-cantilever-files-verify/FreeCAD_1.1.4/`);
- FreeCAD 26.3 RC2: same verifications, 21/21 checks each
  (`results/pd-beam-verify/FreeCAD_26.3rc2/`,
  `results/pd-cantilever-files-verify/FreeCAD_26.3rc2/`).

These targeted runs verify build, meshing, direct-reference breakage, and
renewal, but they are not part of the automated test suite: the PartDesign
example has no automated test case yet, and the runs were not bound to
recorded executable hashes or a full metadata set.

The 1.0.2 log confirms macro loading, test-geometry creation, successful
creation of the FEM cut through BOPTools, and SelectionSetLink application.
The 1.1.0 RC3 logs additionally show successful cut creation, GMSH mesh-file
creation, CalculiX completion without solver error, and reading of FRD and DAT
results. The test-result summary identifies the macro version used for that run.

The logs also contain important limitations:

- The reported `FreeCAD version` is `<built-in function Version>`, showing
  that the current version-detection path references `FreeCAD.Version` rather
  than reliably calling it.
- The FEM test reports unexpected reference counts but continues and marks
  the overall FEM test as passed. These warnings need classification or
  stricter assertions before FEM compatibility can be certified.
- FreeCAD 1.1 reports that the document should be saved before a solver or
  mesh operation. This is an environment/work-directory warning that must be
  handled or documented in future reproducible runs.
- The source currently has general SelectionSet debug output enabled, while
  FEM-specific debug-file writing is disabled by default. The TODO item to
  disable all debugging by default is therefore not fully complete.

The logs demonstrate successful executions, but they do not constitute a
complete compatibility certificate. The result summary is not consistently
bound to a repository commit, exact executable, operating system, dependency
versions, and a unique run identifier. Those fields should be recorded for
future campaigns.

## Test scope not yet fully evidenced

The code contains document-restoration support and observer detach/attach
logic, but the available evidence does not yet demonstrate the complete
Plan B lifecycle sequence: save, close, restart, reopen without first
running the macro, refresh after geometry changes, undo/redo, and independent
deletion of targets, selectors, and sets.

Likewise, the available evidence does not yet provide a dedicated
two-document isolation test with identically named objects, or a structured
compatibility matrix covering pinned baseline, target, and development
FreeCAD builds. GUI code exists for toolbars, menus, highlighting, icons, and
selection observers, but those surfaces still require explicit per-build
evidence.

The current evidence therefore supports this status:

> The SelectionSet implementation has broad working geometry, GUI,
> SelectionSetLink, FEM, GMSH, and automated-test coverage. Recorded runs
> succeeded on FreeCAD 1.0.2 and FreeCAD 1.1.0 RC3, including an end-to-end
> FEM cantilever calculation. Cross-version certification, lifecycle
> validation, multi-document isolation, reliable version detection, and
> complete evidence metadata remain open.

## Plans and development directions

There are several `Plan_*.md` documents in this folder. They are separate
planning documents with different goals and development directions; they are
not interchangeable and should not be treated as one linear task list.

In particular, `Plan_B_Compatibility_Regression.md` describes the
compatibility and regression campaign: baseline freezing, version detection,
FEM and GUI audits, persistence, observer cleanup, multiple documents, a
tiered test matrix, and required evidence. Other `Plan_*.md` files may
address different development, physics, FEM, analytical, or release goals.
Before starting work, read the plan relevant to that task and check its
assumptions against the current source and logs. Keep implementation results,
suspected issues, and verified compatibility evidence distinct.

## Expectations for future FreeCAD versions

A newer FreeCAD version should not be considered supported solely because the
macro imports or the basic tests pass. For each new version:

1. Record the exact FreeCAD build, libraries, OS, solver, GMSH, repository
   commit, and macro version.
2. Run the existing geometry and FEM tests unchanged.
3. Preserve and classify failures; do not change expected values merely to
   make a new version pass.
4. Check capability-sensitive APIs, including version reporting, PartDesign
   properties, FEM references, GMSH invocation, Qt/PySide imports, and
   observer APIs.
5. Repeat persistence, reload, GUI, and multi-document tests.
6. Record warnings separately from passes and failures.
7. Add a version to the compatibility matrix only after the results are
   reproducible and known limitations are documented.

Future-version support should be described as tested for the recorded build,
not guaranteed for an entire release series or development branch.

### FreeCAD 26.3 FEM boundary-condition API

FreeCAD 26.3 renamed the electrostatic potential boundary condition to the
electromagnetic boundary condition. The compatibility test therefore selects
the API matching the detected FreeCAD version:

- before 26.3: `ObjectsFem.makeConstraintElectrostaticPotential` and
  `Fem::ConstraintElectrostaticPotential`;
- from 26.3 onward: `ObjectsFem.makeConstraintElectromagnetic` and
  `Fem::ConstraintElectromagnetic`.

This is one logical FEM boundary-condition test, not an added or removed test.
The selected factory and document type are recorded in the test output. The
initial 26.3 RC2 result of `21 passed, 1 failed` was caused by the test still
requesting the pre-26.3 API. After the compatibility path was implemented,
the rerun selected `Fem::ConstraintElectromagnetic` and passed all 22 logical
tests.

The post-change compatibility reruns are archived in version-specific
directories with timestamped files:

- `results/archive/FreeCAD_1.0.2/2026-10-25_170656_*`: 21 passed, 1 expected
  GMSH-related FEM cantilever failure;
- `results/archive/FreeCAD_1.1rc3/2026-10-25_170722_*`: 22 passed, 0 failed;
- `results/archive/FreeCAD_1.1.4/2026-10-25_170801_*`: 22 passed, 0 failed;
- `results/archive/FreeCAD_26.3rc2/2026-10-25_170848_*`: 22 passed, 0 failed.

The 1.0.2, 1.1 RC3, and 1.1.4 runs logged
`Fem::ConstraintElectrostaticPotential`; the 26.3 RC2 run logged
`Fem::ConstraintElectromagnetic`. The logical test count remained 22.

## Exact test-run procedure

The tests run inside the selected FreeCAD AppImage using FreeCAD's embedded
Python. No external Python environment, Conda activation, Pixi environment,
virtualenv, or `python3 selection_set_tests.py` invocation is required.

From the project root, select the AppImage explicitly and run:

```bash
FREECAD_EXIT_AFTER_TESTS=1 \
./app/FreeCAD_<version>.AppImage \
./src/tools/run_macro_and_tests_at_startup.FCMacro
```

For example:

```bash
FREECAD_EXIT_AFTER_TESTS=1 \
./app/FreeCAD_1.0.2-conda-Linux-x86_64-py311.AppImage \
./src/tools/run_macro_and_tests_at_startup.FCMacro
```

The startup macro waits for the GUI, loads `SelectionSet.FCMacro`, builds
the test geometry, activates the FEM workbench when available, calls
`selection_set_tests.run_selectionset_tests()`, writes the result and debug
files, and closes FreeCAD when `FREECAD_EXIT_AFTER_TESTS=1` is set.

The launcher can also be used from the project root with an explicit
executable:

```bash
./src/tools/run_with_gui.sh \
  --freecad ./app/FreeCAD_1.1rc3-Linux-x86_64-py311.AppImage \
  --exit
```

Before each run, archive the current result files and the corresponding
FreeCAD log. The test runner writes to shared filenames and can report a
successful process exit even when an individual test fails. Always inspect
`selection_set_test_results.txt` for the `passed`, `failed`, and
`Failing tests` lines.

The explicit launcher procedure was verified with the documented builds:

- FreeCAD 1.0.2: `21 passed, 1 failed`; the failure was the known FEM
  cantilever GMSH mesh-generation limitation.
- FreeCAD 1.1.0 RC3: `22 passed, 0 failed`; the FEM cantilever mesh and
  CalculiX workflow completed.

The archived explicit-path reruns are:

- `results/archive/FreeCAD_1.0.2-explicit-2026-10-25/`
- `results/archive/FreeCAD_1.1rc3-explicit-2026-10-25/`

The current launcher accepts `--freecad PATH` and no longer depends on the
first AppImage found in the launcher's directory. The remaining evidence
metadata task is to record the AppImage SHA-256, OS, repository commit,
solver/GMSH versions, and exit status in a per-run manifest.
