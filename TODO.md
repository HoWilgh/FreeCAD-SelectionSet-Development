# SelectionSet macro – TODO

> `TODO.md` tracks unfinished work.
> `WORKFLOW_STATUS.md` documents the current verified workflow and status.

## Suggested next steps

1. **Before release:** Make all debugging off by default (no debug output unless enabled).
2. **Release prep:** Fill in `release/package.xml` (maintainer, repo URL), add LICENSE, follow **release/RELEASE.md**. Test on FreeCAD 1.0.2 and 1.1. Document installation in README.
3. **Git – exclude dev-only files from addon repo:** Ensure `rules.md` and `TODO.md` are not shipped with the addon. They are in `.gitignore`. If they were already committed, run:
   ```bash
   git rm --cached rules.md TODO.md
   git commit -m "Stop tracking rules.md and TODO.md; do not ship with addon"
   ```
   Then the release repo (e.g. GitHub source for Addon Manager) will not contain them.
4. **Optional:** List macro on wiki (Macros recipes) or submit a minimal version to FreeCAD-macros.

## Release decisions recorded

- Proposed development-repository name: `FreeCAD-SelectionSet-Development`.
- Keep `selection_set_tests.py` in the release tree for now. The current
  `SelectionSet.FCMacro` imports it to provide the optional test toolbar, so
  removing it would change the current runtime package. Revisit this when the
  test toolbar is separated from the user macro.
- The current release metadata is a template only. Before using
  `release/package.xml`, provide the final repository URL, maintainer name and
  email, license file, and release date. Keep `release/RELEASE.md` aligned with
  the selected distribution route.
- The sibling clone currently tracks the upstream `FreeCAD-macros` `master`
  repository. Its remote `master` will probably need an upstream update before
  the SelectionSet release candidate can be considered current.
- `README.md` documents this development project. `src/macro/README.md` is
  the standalone user guide for the SelectionSet macro and must remain
  focused on installation and macro use.


## To do

- [ ] after finished everything for releasing the macro: Make all debugging off by default (no debug output unless enabled).
- [ ] Prepare for release as macro for FreeCAD (Addon Manager) on v1.0.2 and v1.1: fill in `release/package.xml` (maintainer, repo URL), add LICENSE, then follow **release/RELEASE.md** (official doc links + own-GitHub + custom addon source). Optional: list on wiki or submit minimal version to FreeCAD-macros.
- [ ] Before publishing addon repo: if `rules.md` or `TODO.md` were ever committed, run `git rm --cached rules.md TODO.md` and commit so they are not in the addon package (see Suggested next steps and release/RELEASE.md).
- [x] Define the release-file set and use the GitHub clone's
  `FEM/SelectionSet` directory as a release-candidate source under test.
  Keep the sibling clone separate from the development workspace, and keep
  AppImages, evidence, documents, plans, and local rules outside the release
  directory.
- [x] Add explicit `--source PATH` support to the compatibility launcher so
  tests can import and load the clone source without copying test artifacts.
- [x] Restore the sibling clone to its upstream state after the initial source
  isolation experiment and remove generated artifacts from its release tree.
- [x] Synchronize the approved development release files into the sibling
  clone, run the clone-source verification, and review the resulting Git diff
  before any commit or push. Use `src/tools/sync_release_files.sh`; it derives both
  repository paths from its own location, validates both Git roots, copies only
  the approved file mapping, and verifies SHA-256 hashes.
- [x] Make source execution path handling robust and consistent across the
  runners: relative paths resolve from the development repository root, `~` is
  expanded, required files are validated, and the exact source directory used
  by FreeCAD is printed.
- [x] Isolate generated test output from the selected source: use
  `src/tools/run_with_gui.sh --results PATH` to set `SELECTIONSET_OUTPUT_DIR` for
  documents, meshes, solver files, debug exports, and result summaries. The
  launcher creates a unique timestamped run folder below `PATH` so later runs
  do not overwrite earlier evidence.
- [x] Add source-specific automated matrix results under
  `results/automated-matrix/<source>/<timestamp>/` and preserve older evidence
  under `results/archive/`.

- [ ] Optional: Extend SelectionSet to points and edges.
- [ ] Optional: Enhance highlighting involved elements. When unhiding the selection in the model tree, temporarily show only MainObject, SelectionShape, or the coordinate point.





---

## Done
[x] 0.1 make size of "Coordinate Point Marker" changeable/adopable. -> added `CoordinatePointSize` (Display) on SelectionSet; used as sphere radius in view provider; visible only for VolumeMode = 'coordinates'.
[x] 0. make it possible to cancel the 'Create/Update SelectionSet' operation. If the button is pressed a window opens up where the user should select 'Solids' or 'Faces' but there is no possibility to cancel this operation. The X at the title-bar does not work and does not close the window, which is unexpected.

[x] -1. Creating a SelectionSet in FreeCAD version 1.1RC3 (this does not apply for version 1.0.2) by clicking the button gives the following error. This also happens if two shapes are already selected:
"[DEBUG] SelectionSet button callback triggered!
[DEBUG] FreeCADGui.Selection.getSelection(): []
[DEBUG] FreeCADGui.Selection.getSelectionEx(): []

--- SelectionSet Button Pressed ---
Selection count: 0
Selected objects (in order):

Selected subelements (per object):
Direct selection: elements []18:30:10  Traceback (most recent call last):
18:30:10    File ".../FreeCAD_macro_SelectionSet/selection_set_core.py", line 1277, in create_or_update_selectionset_from_current
18:30:10      createSelectionSetFromCurrent(selection_set_name=selection_set_name, force_mode=force_mode, volume_mode=volume_mode)
18:30:10    File ".../FreeCAD_macro_SelectionSet/selection_set_core.py", line 1536, in createSelectionSetFromCurrent
18:30:10      obj = FreeCAD.ActiveDocument.addObject("App::FeaturePython", selection_set_name)
18:30:10            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
18:30:10  TypeError: argument 2 must be str, not bool
"

- [x] update documentation, feature list and comments (README: FEM beam CylinderRadius default 300 / variable-driven, test list 9c–10f and FEM cantilever full, icons toolbar, Requirements 1.0.2 and 1.1; Features: FEM beam example bullet).
- [x] Optional: Add a "Text-Document"-element into the FEM-beam-example: App::TextDocument "FEM_Beam_Readme" in group FEM Cantilever with readme and expected deflections (no hole ~88.4 mm, hole r=300 mm ~96.2 mm, hole r=400 mm ~375.3 mm).

- [x] Make all newly implemented functionality fully available via Python: `get_faces_by_point`, `get_solids_by_point`, `get_faces_by_selection_shape`, `create_selectionset()` (new helper), `recomputeSelectionSetFromShapes`, `createSelectionSetLink`, FEM helpers; README "Python API (scripting without GUI selection)" documents usage and example.

- [x] Debug output file extension: use **.log** for debug logs (fem_cantilever_debug.log, gmsh_mesh_debug.log, selection_set_debug_export.log / selection_set_debug_export_all.log) so they are clearly log output; test results remain selection_set_test_results.txt.

- [x] GMSH meshing on FreeCAD 1.0.2: use `GmshTools.create_mesh()` when `run()` is not available. Added `_run_gmsh_for_mesh(mesh)` that tries femexamples, then `tool.run(blocking=True)`, then `tool.create_mesh()`; used in full test and in FEM beam example. Also set `CharacteristicLengthMax` in test when present (1.0.x).

- [x] Add version number of macro as meta-data to SelectionSet and SelectionSetLink: property **MacroVersion** (group Meta, read-only) set to `__version__` on create; onDocumentRestored adds it if missing for old documents.

- [x] Add a version number to the macro and use this version to test if the loaded macro meets expectations: `__version__` in selection_set_core (e.g. "1.0.0"), printed in entry-point banner and in test runner; REQUIRED_MACRO_VERSION and _macro_version_ok() in tests to warn if version is below required.
- [x] Set in FEM example 'Suppressed' by default to no: use cut (hole) by default (config, var, and Beam_Cut.Suppressed = False).

- [ ] Add FEM-cantilever test for hole radius 400 mm (same x-pos, same h_max): deflection ~375.31 mm; add CylinderRadius to FEM beam variables (FEM_Beam_Variables / FEM_Beam_VarSet), drive Beam_CylinderCut.Radius from it; include in all-test-cases (Case 3 in _run_fem_cantilever_full_test).
 -> now it is only reported in the variables but i want to change it there.
- [x] FEM beam links: set AddShapes=[], SubtractSelectionSets=[], SubtractShapes=[] when configuring the three beam links (material, fixed, force) so they use only the intended SelectionSets and never inherit test geometry from the GUI selection (fixes "SelectionSetLink Beam (1 solid) Material (5 solids)" and Test FEM cantilever full failure).

- [x] make multiple target objects possible for SelectionSetLink – only **Target objects** (PropertyLinkList); single property, click … to add one or more targets (constraint, material, etc.). Same combined refs applied to each. Create from selection with multiple FEM objects selected, or add in Data tab. If the same object is used by several links, each Renew overwrites its References.
- [x] shift for "run all" the geometry of the FEM-cantilever example to not overlay the other test-shapes/geometries – `run_fem_cantilever_beam_example` accepts `geometry_offset` and the full FEM cantilever test builds the beam at `FreeCAD.Vector(0, 3000, 0)` so it does not overlap the other test geometries near the origin.
- [x] Check if a selection set can directly expose elements as reference for a FEM element (e.g. boundary condition) without affecting other behaviour – confirmed current design: SelectionSet does not and should not expose a `References` property; FEM objects should be driven via helper functions (`get_fem_references_from_selectionset`, `apply_selectionset_to_fem_constraint`) or `SelectionSetLink`, keeping SelectionSet behaviour independent.
- [x] GMSH mesh + SelectionSetLink – Document/work around that referencing a GMSH mesh with SelectionSetLink uses FEM mesh → shape, not References like other FEM elements. Added short “suggestions for FreeCAD” list (homogenise references, shapes for GMSH/material) to README.
- [x] FEM beam constraints: apply only beam-shape refs (Beam_Box/Cut) so no test-geometry refs are applied → avoids "Empty femnodes_mesh" when running in same document as SelectionSet tests.
- [x] Quiet mode for Create/Update SelectionSet callback during test run (SELECTIONSET_VERBOSE_CALLBACK = False in run_selectionset_tests); verbose callback output gated by flag.

## Compatibility test infrastructure and evidence preservation

The following sequence is the planned order for extending compatibility
testing without losing the existing evidence.

### 1. Preserve the current baseline results

- [x] Create and preserve the read-only historical baseline directory
  `results/archive/baseline-2026-03-17/`. Do not overwrite it.
- [x] Copy the historical `selection_set_test_results.txt`,
  `selection_set_debug_export.log`, and
  `selection_set_debug_export_all.log` into that directory.
- [x] Copy the recorded FreeCAD run logs from `tmp/`, including the
  FreeCAD 1.0.2 and FreeCAD 1.1.0 RC3 runs.
- [x] Preserve the baseline unchanged. Future test runs write to
  version-specific result directories rather than replacing these files.
- [x] Treat the historical `22 passed, 0 failed` result as historical
  evidence. New automated results are bound to source-specific,
  timestamped, version-specific directories.

### 2. Define the repeatable version-matrix run

- [x] Add explicit FreeCAD executable selection to the test launcher instead
  of relying on the first `FreeCAD*.AppImage` found in a directory.
- [x] Define one result directory per tested build:
  `FreeCAD_1.0.2`, `FreeCAD_1.1rc3`, `FreeCAD_1.1.4`, and
  `FreeCAD_26.3rc2`.
- [ ] Record for every run: timestamp, executable name and SHA-256, reported
  FreeCAD/library build, OS, repository commit, macro version, solver/GMSH
  versions, command line, result file, warnings, failures, and exit status.
- [x] Run the existing tests unchanged before changing expected values or
  interpreting a version-specific difference.

### 3. Run and compare the newly added FreeCAD builds

- [x] Run the full GUI test campaign with FreeCAD 1.0.2 from both the
  development and clone sources; classify the documented GMSH limitation.
- [x] Run the full GUI test campaign with FreeCAD 1.1 RC3 from both the
  development and clone sources.
- [x] Run the full GUI test campaign with FreeCAD 1.1.4 from the development
  and clone sources (22 passed, 0 failed; legacy electrostatic API).
- [x] Run the full GUI test campaign with FreeCAD 26.3 RC2 from the
  development and clone sources (22 passed, 0 failed; electromagnetic API).
- [x] Preserve each run's console output, FreeCAD log, test-result summary,
  debug exports, and generated FEM evidence in its own result directory.
- [x] Compare test counts, expected element lists, FEM reference counts,
  mesh/solver outcomes, displacement ranges, warnings, and errors against
  the preserved baseline.
- [x] Classify every difference as a SelectionSet defect, an upstream
  FreeCAD/API change, an environment/toolchain issue, or unresolved.

### 4. Complete the compatibility evidence

- [x] Fix or verify the `FreeCAD.Version` detection path before relying on
  version-dependent test conclusions.
- [ ] Resolve or explicitly classify the FEM reference-count warnings that
  currently do not fail the test.
- [ ] Repeat save/close/reopen, macro reload, observer cleanup, GUI, and
  two-document isolation tests for each supported build.
- [ ] Keep expected test-oracle values unchanged unless a reproducible
  geometry or API reason is confirmed and the user approves the update.
- [ ] Update `Plan_B_Compatibility_Regression.md` and
  `WORKFLOW_STATUS.md` with reproducible evidence and known limitations.

### 5. Reorganize only after the evidence is preserved

- [x] Separate AppImages into `app/`, source and tests into `src/`, and
  source tools formerly under `tmp/` into `src/tools/`. Keep generated
  artifacts and evidence outside `src/`.
- [x] Move AppImages and source files only after current paths and baseline
  references were recorded; update launchers and documentation accordingly.
- [x] Update launcher paths and `.gitignore` together after the layout was
  approved.
- [ ] Consider a separate private compatibility/showcase repository only
  after the local evidence structure and version matrix are stable. Do not
  commit AppImages or credentials to that repository.
- [x] Full automated FEM cantilever test: run mesh, run simulation with hole, check max. deflection. Included in run_selectionset_tests as "Test FEM cantilever full" (\_run_fem_cantilever_full_test).
- [x] make FEM-cantilever example also work under 1.1, because currently the cut is not created in v1.1
- [x] Group test geometries and FEM beam: Test 1/2/9 geometry and FEM cantilever (geometry + SelectionSets + links + config) are placed in App::DocumentObjectGroup (Test1_Geometry, Test2_Geometry, Test9_Geometry, FEM_Beam_Group).
- [x] Right-click menu on SelectionSet → Create SelectionSetLink: context menu item "Create SelectionSetLink"; if a FEM object (e.g. constraint) is in the selection, set it as target and apply refs.
- [x] Use Variables in 1.1 / VarSet in 1.0 for FEM beam geometry switch: when version >= 1.1 try App::Variables (FEM_Beam_Variables), else App::VarSet (FEM_Beam_VarSet); link config.Suppressed via expression.
- [x] Research FEM beam geometry switch vs existing FreeCAD: not possible with standard objects only (PropertyLink has no conditional expression; no built-in switch; recompute/apply-link are imperative). Documented in README "FEM beam geometry switch" and in-code comment; implementation detail (FEM_Beam_Config + onChanged → mesh, SelectionSets, links) described there.
- [x] Combine all tests into a pulldown menu: single "Tests" toolbar button with menu (Run Test 1, Build test geometry, Run Test 3, Run SelectionSet Tests, FEM beam example).
- [x] Add button to update all SelectionSets and all SelectionSetLinks (after another): toolbar "Update all sets and links" runs recompute on every SelectionSet then applies every SelectionSetLink.
- [x] Create `selection_set_core.py` with SelectionSet logic and GUI (Create/Expand/Update, observer, commands).
- [x] Create `selection_set_tests.py` with test runner and test geometry builders (tests 1–9, 9a, 9b).
- [x] Slim down `SelectionSet.FCMacro` to entry point only (toolbar + optional test buttons).
- [x] Build test geometry on demand; only create geometry if required objects are missing; allow re-run after changing shapes.
- [x] Reload modules on macro run so latest code is used (`importlib.reload`).
- [x] Prominent print banner when macro starts (“SelectionSet macro – RUN STARTED”).
- [x] Put Mode and VolumeMode properties in the “Selection” group (subset) instead of “Shapes”.
- [x] Automated test run: `./run_with_gui.sh` runs macro + tests; results in `selection_set_test_results.txt`; `--exit` for scripted use.
- [x] Test FEM: FEM analysis + ConstraintFixed + the capability-selected
  electrostatic/electromagnetic boundary condition + FEM material + three
  SelectionSetLinks; skip if FEM is not loaded. FreeCAD 1.0.2, 1.1 RC3, and
  1.1.4 use `Fem::ConstraintElectrostaticPotential`; FreeCAD 26.3 RC2 uses
  `Fem::ConstraintElectromagnetic`.
- [x] FEM integration: `get_fem_references_from_selectionset` / `apply_selectionset_to_fem_constraint`; double-click expand to constraint; **SelectionSetLink** object (add/subtract sets and shapes → target).
- [x] Right-click menu on Element list and stored shapes to select individually.
- [x] Filter faces by solid: SolidFilterRefs (click ... to select solids); select main + shape + SelectionSet with solids (e.g. Test 9b); Test 9c uses this.
- [x] SelectionSet link: TargetObjects, AddSelectionSets, SubtractSelectionSets, AddShapes, SubtractShapes, ShapeRefMode, UseOneByOneWorkaround; toolbar “Create SelectionSet link”; **Renew elements** (target updated only from this, not on recompute).
- [x] Update SelectionSet in menu and submenu for selection-set entries (bold, background #e0e8f0).
- [x] FEM material geometry: documented Face/Edge only; link or manual selection.
- [x] Refresh docs: target updated only via **Renew elements**; no auto-apply to avoid “still touched after recompute”.
- [x] Naming: new SelectionSets get tree label **SelectionSet …**; new SelectionSetLinks get **SelectionSetLink …** (RefSummary appends e.g. “ (6 faces)”).
- [x] Apply when 0 elements: target References cleared instead of leaving stale refs.
- [x] Option to select/find solids or faces by coordinates (e.g. add "coordinates" to Volume mode and rename).
- [x] Reuse or define icons for SelectionSet / SelectionSetLink (bundled SVGs; work when run via FCMacro/CLI).
- [x] Fix Test 9c – Solid filter: \_get_solid_for_face uses majority vote over face vertices+center and tolerance; Test 9c enabled.
- [x] Test 9d: SolidFilterRefs → Solid2 → [Face8, Face9]; test and README doc.
- [x] Document how to use SolidFilterRefs (README: “Filter faces by solid” + second row in link dialog for sub-elements).
- [x] Further tests with coordinates: Test 10c–10f (Face5, Face2/4/5, BooleanFragments.Face7, CylTwoHalves Face5,6,8,9).
- [x] Shift/Alt/Ctrl+Click on SelectionSet: main object, selection shape, or elements.
- [x] Icons on toolbar buttons (icon beside text, not replacing).
- [x] When **Create SelectionSet** is pressed with one or more SelectionSets selected: update those sets from the rest of the selection (main/shape/filter) and recompute; no new set created.
- [x] Combine "Create SelectionSet" and "Update SelectionSet" into one button **Create/Update SelectionSet**: when only SelectionSet(s) selected → update; else → create or update from selection.
- [x] **Run Test 1 button** – enable `add_run_test_1_button_to_toolbar()` so the button creates two cubes + Test 1 SelectionSet programmatically (using `run_test_1_only`) and the object is deletable.
- [x] Deletion robustness: deleting test SelectionSets and SelectionSets referenced from SelectionSetLinks/FEM does not delete shapes or links; links are unlinked safely and a context-menu action **Delete SelectionSet only (keep shapes)** is available on SelectionSet.
- [x] Run-test1 creates a new document if necessary, and Run-Selection-test now also creates/uses a dedicated 'SelectionSetTest' document so both paths are aligned.
- [x] main and selection shape in Test 1 (when using Run Test 1 button) are now assigned (MainObject/SelectionShape set the same way as in the full test runner).
- [x] Create a dedicated third test button that builds **only the required geometry** for a specific combined test (two shapes, one SelectionSet, one SelectionSetLink and FEM objects), instead of creating all test geometries. Implemented as Run Test 3: uses Test 1 cubes, one SelectionSet, one SelectionSetLink and a simple FEM fixed constraint.
- [x] Test case for TestCube_main as main; TestCube_Selection as selection; mode solids; Volume-mode intersection -> implemented as Test 3a (solids, intersection) in the full test runner, expecting ElementList = ['TestCube_main.Solid1']. Original Test 3 (solids, main first, expect \[\]) restored.
- [x] add logic so that "coordinate-point" in "Selection"-view is only shown if coordinates are choosen. similar for all other selections. only show what is necessary.
- [x] Check if button "Remove SelectionSet observer" does anything and if still needed: button removed; observer is detached automatically on each macro run (quiet) so no duplicate observers. Right-click/single-click observer remains off by default; no UI button for it.
- [x] Sort test buttons to R1, R2, R3: toolbar order is now Run Test 1, Build test geometry (R2), Run Test 3, Run SelectionSet Tests.
- [x] Ensure selection by points works on boolean-fragments: Test 10e (coordinates on BooleanFragments → Face7) and Test 10f (BooleanFragments_CylTwoHalves) verify it; both use get_faces_by_point / coordinates mode.
- [x] Adopt for FreeCAD 1.1 while keeping 1.0: module comments and \_freecad_version_tuple() in selection_set_core; observer attach/detach comments (1.0 vs 1.1 API); PartDesign Pad uses SideType when present (1.1), else Midplane (1.0). Entry point and tests describe compatibility in comments.
- [x] **FEM cantilever beam example** – Toolbar button "FEM beam example" builds rectangular beam (1000×100×100 mm), SelectionSets (fixed/force face, beam solid), ConstraintFixed, ConstraintForce, material, GMSH mesh, solver, SelectionSetLinks. Template: ccx_cantilever_faceload.py (local copy in macro folder). **Confirm after testing (rules.md) before marking done.**
  + A) Material and GMSH mesh: implemented – material (FEM_Beam_Material) and GMSH mesh (FEM_Beam_Mesh) are created and added to the analysis; material refs come from SelectionSetLink (Beam_Solid SelectionSet). Verify in FreeCAD that both appear in the analysis and refs apply.
  + B) Cylinder cut: implemented – Both Beam_Box and Beam_Cut are always created. Toggle **FEM_Beam_Config.UseCylinderCut** in the Data tab to switch between box and cut geometry; mesh, SelectionSets, and links update automatically. Basic model starts with Beam_Box (executable). Verify in FreeCAD that toggling works and constraints/mesh/material follow the switch.
