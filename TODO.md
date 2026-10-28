# SelectionSet macro – TODO

> `TODO.md` tracks unfinished work.
> `WORKFLOW_STATUS.md` documents the current verified workflow and status.

## Showcase documentation to prepare

- [ ] Fill the five image placeholders in
  `SELECTIONSET_SHOWCASE_SUGGESTIONS.md` and select two to four of them for
  the final publications (short and extended descriptions are drafted in the
  same file).
- [ ] Verify the screenshots against **Tests -> FEM beam example**:
  plain beam, cut with hole, `FEM Cantilever`, `FEM beam variables`,
  SelectionSets/links, and the result after **Update all sets and links**.
- [ ] Record the exact FreeCAD version, macro version, hole switch state, and
  cylinder radius used for each published image.
- [ ] Publish the short version with the macro/release material and publish
  the clear introduction plus the extended explanation in the referenced
  FreeCAD forum discussion.

## Compatibility update and official FreeCAD-macros submission

### 1. Define the distribution route

- [ ] Decide whether the target is an entry in `FreeCAD/FreeCAD-macros`, a
  standalone repository installed through a custom Addon Manager source, or
  both. Do not mix the two package formats.
- [ ] For the official macro repository, omit `package.xml`; use the
  category directory and the macro's `__Files__` metadata.
- [ ] Exclude `TODO.md`, `AGENTS.md`, plans, AppImages, generated results,
  backups, credentials, and local test infrastructure from the submitted
  directory.
- [ ] Decide whether `selection_set_tests.py` remains an intentional part of
  the installed macro because it supplies the Tests button; update
  `__Files__` and documentation together with that decision.
- [ ] Choose the exact supported FreeCAD versions and document known
  FEM/GMSH limitations.

### 2. Synchronize and audit the current upstream

- [ ] Update the local `FreeCAD-macros` sibling clone from
  `FreeCAD/FreeCAD-macros`; record the upstream commit used for the audit.
- [ ] Prepare a clean branch from the current upstream default branch and
  copy only the intended release files.
- [ ] Audit imports, runtime paths, icons, and `__Files__` in a clean FreeCAD
  macro directory. Every installed dependency must be present and listed.
- [ ] Complete the official metadata near the top of `SelectionSet.FCMacro`:
  `__Name__`, `__Comment__`, `__Author__`, `__Date__`, `__Version__`,
  `__License__`, `__Web__`, `__Wiki__`, `__Help__`, `__Status__`,
  `__Requires__`, `__Communication__`, and `__Files__`. Use literal
  single-line strings.
- [ ] Resolve the current metadata gap: confirm the final license,
  author/contact, version/date, wiki URL, communication URL, status, and
  complete auxiliary file list before submission.
- [ ] Confirm the filename and category placement follow the official
  CamelCase and category conventions.

### 3. Produce compatibility evidence

- [ ] Run the automated matrix on the development source and clean release
  candidate with the supported FreeCAD builds.
- [ ] Run from a clean user macro directory. Verify toolbar creation, normal
  SelectionSet use, SelectionSetLink renewal, save/reopen, and the FEM beam
  example.
- [ ] Test the FEM example with and without the hole and with
  `CylinderRadius` 300 and 400. Confirm recompute followed by **Update all
  sets and links** refreshes the intended FEM references.
- [ ] Record every run as defined in the compatibility-evidence section
  below (timestamp, executable name and SHA-256, FreeCAD/library build, OS,
  repository commit, macro version, solver/GMSH versions, command line,
  result files, warnings, failures, and exit status).
- [ ] Classify each failure as a macro defect, upstream API change,
  solver/toolchain issue, or unresolved compatibility issue.
- [ ] Make debug output opt-in for the release candidate and verify normal
  use does not create development logs in the user's macro directory.
- [ ] Update the standalone macro README and release metadata only after
  clean-install results are reproducible.

### 4. Obtain community review

- [ ] Post the concise description, screenshots, installation steps,
  supported versions, limitations, and reproducible example in the FreeCAD
  Python Scripting and Macros forum.
- [ ] Ask reviewers to check the workflow, metadata, licensing, file list,
  and compatibility claims; record and address feedback.
- [ ] Wait for a clear positive review/green light before preparing the
  upstream pull request, following the official `FreeCAD-macros` procedure.

### 5. Prepare and validate the pull request

- [ ] Create a fresh feature branch from the latest upstream default branch.
- [ ] Add only the reviewed SelectionSet directory and required files. Do not
  add `package.xml` to the official macro-repository route.
- [ ] Run the repository's documented local checks, including pre-commit
  checks if enabled, and rerun clean-install and compatibility tests.
- [ ] Inspect the final diff for generated artifacts, local paths, private
  data, secrets, and unrelated changes.
- [ ] Push to the personal fork only when explicitly authorized, then open a
  PR against `FreeCAD/FreeCAD-macros` with summary, test matrix, screenshots,
  forum review link, limitations, and file list.
- [ ] Monitor CI and reviewer feedback; rerun affected tests and keep the PR
  description synchronized with the actual release.
- [ ] After merge, verify Addon Manager listing and installation/update from a
  clean FreeCAD profile.

### 6. Alternative standalone-repository route

- [ ] If the official route is declined or the file set is too large,
  complete `release/package.xml`, add the correct license, repository URL,
  maintainer, date, and version, and test a clean custom Addon Manager source.
- [ ] Keep `package.xml` in the standalone package only, never in the
  official `FreeCAD-macros` directory.

## Suggested next steps

1. **Before release:** Make all debugging off by default (no debug output
   unless enabled); part of the release checklist step 3 above.
2. **Git – exclude dev-only files from addon repo:** Ensure `rules.md` and
   `TODO.md` are not shipped with the addon. They are in `.gitignore`. If they
   were already committed, run:
   ```bash
   git rm --cached rules.md TODO.md
   git commit -m "Stop tracking rules.md and TODO.md; do not ship with addon"
   ```
   Then the release repo (e.g. GitHub source for Addon Manager) will not
   contain them.
3. All release-preparation, compatibility-evidence, community-review, and
   pull-request work is tracked in the release checklist above and in
   **release/RELEASE.md**; the wiki-listing option is decided in checklist
   step 1.

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

Release preparation, packaging, Addon Manager publishing, and the official
FreeCAD-macros submission are tracked in the release checklist and
**Suggested next steps** above; they are not repeated here.

- [ ] Consider bumping the macro version (`__version__` in `selection_set_core.py`) for the new edges mode and link TargetProperty feature before the next release.
- [ ] Optional: Extend the box/cut FEM beam example (`run_fem_cantilever_beam_example`) with a direction-edge SelectionSet/link like the PartDesign example, so its force Direction also survives the cut switch.
- [ ] Optional: Add an automated test case for edges mode (get_edges_by_point / coordinates) and for link TargetProperty='Direction'.
- [ ] Optional: Verify the FEM PartDesign beam example on FreeCAD 1.0.2 (PartDesign::Fillet property names, stale-reference behaviour without TNP: Face2 may silently resolve to the wrong face instead of '?Face2').
- [ ] Optional: Add an automated test case for the FEM PartDesign beam example (build, enable fillet, Update all sets and links, check constraint refs; expected deflection without fillet ~88.4 mm).
- [x] **FEM beam example (PartDesign body)** – Tests pulldown entry `run_fem_partdesign_beam_example`: PartDesign Body (sketch 8000x1000 + pad 1000), mesh geometry = Body, PartDesign::Fillet on the long top edge (suppressed by default, radius via `PD beam variables`.FilletRadius), direct + SelectionSetLink-driven constraint references. Verified on FreeCAD 1.1.4 and 26.3rc2 (results in `results/pd-beam-verify/`): fillet changes face numbering (force face Face2 -> Face5, Face2 -> fixed end), stale direct ref is invalidated ('?Face2') on 1.1, `Update all sets and links` restores the intended references.
- [x] Verify the standalone copy `src/tools/fem_beam_example_partdesign.py` with a GUI run (approved runs later completed; the PartDesign example with direction links verified 25/25 on FreeCAD 1.1.4 and 26.3rc2 in `results/pd-direction-verify/`; the copy is kept verbatim in sync with the tests-module example).
- [x] **Tree layout coherence** (user-reported: Tests menu put the Body inside 'FEM Cantilever (PartDesign)' while the standalone scripts leave it next to the analysis): removed `PD_Beam` from the group in `run_fem_partdesign_beam_example` and its standalone copy, so in all paths the Body sits at document top level next to the FEM analysis and the group holds only SelectionSets, links, variables, and readme. Verified on FreeCAD 1.1.4 (27/27 checks, `results/pd-group-verify/`). Also added the readme TextDocument 'FEM PD beam – readme and expected values' (FEM_PDBeam_Readme) to `ccx_cantilever_faceload_partdesign_selectionset.py` and its 'SelectionSets and links' group (7/7 checks, `results/macro-menu-verify/`).
- [x] **Macro-menu execution of the standalone PartDesign files** (user-reported: running from the FreeCAD Macro menu did nothing): the files only defined `setup()`/the example function without calling it. Added `if __name__ == "__main__": setup()` guards (FreeCAD's macro dialog runs the file in a copy of the `__main__` namespace) plus a `__file__`-less fallback that locates `src/macro` via the working directory. Verified on FreeCAD 1.1.4 (6/6 checks, `results/macro-menu-verify/`): all three files build their example via macro-menu semantics (with and without `__file__`), and a plain `import` does not trigger anything.
- [x] **Direction-edge allocation via SelectionSet/link** (user-confirmed need): SelectionSet Mode extended with **edges** (coordinates mode via new `get_edges_by_point`, volume modes via common-length containment/intersection), `createSelectionSetFromCurrent` accepts `force_mode='edges'`, and SelectionSetLink gained **TargetProperty** ('References' default, or 'Direction' to apply the first edge ref to e.g. `ConstraintForce.Direction`). The PartDesign examples (tests example + standalone copy + `ccx_cantilever_faceload_partdesign_selectionset.py`) now create `PD_Beam_ForceDirection`/`FEM_PDBeam_Link_ForceDirection` resp. `Cantilever_ForceDirectionEdge`/`Link_ForceDirection`. Verified on FreeCAD 1.1.4 and 26.3rc2 (25/25 checks each, results in `results/pd-direction-verify/`): after the fillet the stale Direction retargets (e.g. to 'Edge14') or breaks; renew restores a vertical direction edge at x=8000.
- [x] **Standalone PartDesign cantilever pair** (`src/tools/`): `ccx_cantilever_faceload_partdesign.py` (as near as possible to the original `ccx_cantilever_faceload.py`: same setup()/get_information()/get_explanation() structure, same solver/material/mesh settings, same literal direct refs `Face2`/`Edge5`, but PartDesign Body geometry and a suppressed fillet on the long top edge) and `ccx_cantilever_faceload_partdesign_selectionset.py` (copy extended with SelectionSets + SelectionSetLinks for mesh/material/constraints and `renew_selection_references(doc)`). Verified on FreeCAD 1.1.4 and 26.3rc2 (results in `results/pd-cantilever-files-verify/`, 21/21 checks each): direct refs break after the fillet (`?Face2`/`?Face4`), renew restores force -> Face5 (x=8000) and fixed -> Face2 (x=0), mesh geometry stays on the Body and GMSH regenerates.
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
  versions, command line, result file, warnings, failures, and exit status
  (see also step 3 of the release checklist above).
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
