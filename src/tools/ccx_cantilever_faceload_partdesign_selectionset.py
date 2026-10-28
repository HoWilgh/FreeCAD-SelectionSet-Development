# Development helper derived from FreeCAD FEM examples (ccx_cantilever_faceload).
# Copy of ccx_cantilever_faceload_partdesign.py, extended with SelectionSets and
# SelectionSetLinks (SelectionSet macro) to circumvent the issue of losing the
# allocations/selections for the mesh and the boundary conditions:
#
# - The mesh geometry is the BODY (object-level link), so it follows the body tip
#   (pad or fillet) after any feature change.
# - The constraint and material references are applied through SelectionSetLinks
#   from SelectionSets that store geometric selection criteria (coordinates mode,
#   MainObject = Body). After a topology change (e.g. Fillet.Suppressed = False),
#   run renew_selection_references(doc) (or the macro toolbar button
#   'Update all sets and links') to restore the intended references.
# - The force's Direction edge is a separate reference property and breaks too;
#   it is covered by an edges SelectionSet and a link with TargetProperty =
#   'Direction' (see Link_ForceDirection).
#
# Without this (see ccx_cantilever_faceload_partdesign.py), the direct references
# break when the fillet is introduced: force face Face2 -> Face5 and Face2 then
# names the fixed end.
#
# ***************************************************************************
# *   Copyright (c) 2019 Bernd Hahnebach <bernd@bimstatik.org>              *
# *   Copyright (c) 2020 Sudhanshu Dubey <sudhanshu.thethunder@gmail.com    *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# ***************************************************************************

import os
import sys

import FreeCAD
import Part
import ObjectsFem

# SelectionSet macro core (src/macro next to src/tools). __file__ is not defined
# when this file is executed via the FreeCAD Macro menu (the macro runs in a copy
# of the __main__ namespace), so fall back to the working directory.


def _locate_macro_dir():
    candidates = []
    try:
        candidates.append(os.path.dirname(os.path.abspath(__file__)))
    except NameError:
        pass
    candidates.append(os.getcwd())
    for here in candidates:
        if not here:
            continue
        macro_dir = os.path.abspath(os.path.join(here, "..", "macro"))
        if os.path.isfile(os.path.join(macro_dir, "selection_set_core.py")):
            return macro_dir
    return None


_MACRO_DIR = _locate_macro_dir()
if _MACRO_DIR and _MACRO_DIR not in sys.path:
    sys.path.insert(0, _MACRO_DIR)

import selection_set_core
from selection_set_core import (
    SelectionSet,
    apply_selectionset_view_defaults,
    createSelectionSetLink,
    get_fem_references_from_selectionsets,
    apply_references_to_fem_constraint_one_by_one,
    recomputeSelectionSetFromShapes,
)


def get_information():
    return {
        "name": "CCX cantilever face load (PartDesign body, SelectionSets)",
        "meshtype": "solid",
        "meshelement": "Tet10",
        "constraints": ["fixed", "force"],
        "solvers": ["ccxtools"],
        "material": "solid",
        "equations": ["mechanical"],
    }


def get_explanation(header=""):
    return (
        header
        + """

To run the example use one of:
- FreeCAD menu: Macro -> Macros -> select this file -> Execute
  (the __main__ guard at the end of this file calls setup() automatically), or
- Python console:
  exec(open("<repo>/src/tools/ccx_cantilever_faceload_partdesign_selectionset.py").read())

Same cantilever as ccx_cantilever_faceload_partdesign (PartDesign Body,
fillet on the long top edge, suppressed by default), but the material and
constraint references are applied through SelectionSetLinks from
SelectionSets (coordinates mode, MainObject = Body).

Set Fillet.Suppressed = False and recompute to change the topology, then run
renew_selection_references(doc) (or the macro toolbar button 'Update all sets
and links') and mesh/solve again: the intended references are restored.


"""
    )


def _make_partdesign_body(doc):
    """Create the cantilever as PartDesign Body: sketch 8000 x 1000 on XY + pad 1000.

    Face numbering of the Body shape (verified on FreeCAD 1.1.4):
    Face2 = free end (x = 8000), Face4 = fixed end (x = 0), Edge5 = vertical
    edge at the free end, so the literal references of the original example
    (Face2, Edge5) stay valid.
    """
    body = doc.addObject("PartDesign::Body", "Body")
    doc.recompute()
    xy_plane = None
    for o in doc.Objects:
        if "XY_Plane" in (getattr(o, "Name", "") or "") and body in getattr(
            o, "InListRecursive", []
        ):
            xy_plane = o
            break
    sketch = body.newObject("Sketcher::SketchObject", "Sketch")
    if xy_plane:
        try:
            sketch.AttachmentSupport = [(xy_plane, [""])]
            sketch.MapMode = "FlatFace"
        except Exception:
            pass
    length, width = 8000.0, 1000.0
    pts = [
        FreeCAD.Vector(0, 0, 0),
        FreeCAD.Vector(length, 0, 0),
        FreeCAD.Vector(length, width, 0),
        FreeCAD.Vector(0, width, 0),
    ]
    for i in range(4):
        sketch.addGeometry(Part.LineSegment(pts[i], pts[(i + 1) % 4]), False)
    doc.recompute()
    pad = body.newObject("PartDesign::Pad", "Pad")
    pad.Profile = (sketch, [""])
    pad.Length = 1000.0
    doc.recompute()
    return body, sketch, pad


def _make_fillet_feature(body, pad, radius=100.0):
    """Create a fillet on the LONG top edge of the beam (full length, y = 0 side).

    Introducing this fillet changes the face numbering of the Body:
    force face Face2 -> Face5, and Face2 then names the fixed end.
    Returns the fillet feature (created suppressed) or None.
    """
    length = 8000.0
    edge_name = None
    long_edges = []
    for i, e in enumerate(pad.Shape.Edges, start=1):
        vs = e.Vertexes
        if len(vs) < 2:
            continue
        p0, p1 = vs[0].Point, vs[-1].Point
        d = p1.sub(p0)
        if abs(abs(d.x) - length) < 1e-3 and abs(d.y) < 1e-6 and abs(d.z) < 1e-6:
            long_edges.append((i, min(p0.y, p1.y), max(p0.z, p1.z)))
    if long_edges:
        y_min = min(e[1] for e in long_edges)
        top_edges = [e for e in long_edges if abs(e[1] - y_min) < 1e-6]
        z_max = max(e[2] for e in top_edges)
        for e in top_edges:
            if abs(e[2] - z_max) < 1e-6:
                edge_name = "Edge%d" % e[0]
                break
    if not edge_name:
        FreeCAD.Console.PrintWarning(
            "Fillet: long top edge not found; no fillet created.\n"
        )
        return None
    fillet = body.newObject("PartDesign::Fillet", "Fillet")
    fillet.Base = (pad, [edge_name])
    for rad_prop in ("Radius", "FilletRadius"):
        if hasattr(fillet, rad_prop):
            setattr(fillet, rad_prop, radius)
            break
    fillet.Suppressed = True  # introduce it later to change the topology
    doc = body.Document
    doc.recompute()
    return fillet


def _generate_gmsh_mesh(femmesh_obj):
    """Generate the GMSH mesh (standalone equivalent of femexamples generate_mesh)."""
    try:
        from femmesh.gmshtools import GmshTools

        tool = GmshTools(femmesh_obj)
        if hasattr(tool, "run"):
            return bool(tool.run(blocking=True))
        if hasattr(tool, "create_mesh"):
            return bool(tool.create_mesh())
    except Exception as e:
        FreeCAD.Console.PrintWarning(
            "GMSH mesh not generated ({}). Run GMSH from the mesh object.\n".format(e)
        )
    return False


def _make_selectionset(doc, name, point, mode, label_suffix):
    """Create (or replace) a SelectionSet in coordinates mode on the Body."""
    existing = doc.getObject(name)
    if existing:
        doc.removeObject(existing.Name)
    obj = doc.addObject("App::FeaturePython", name)
    SelectionSet(obj)
    obj.Label = "SelectionSet " + label_suffix
    obj.MainObject = doc.getObject("Body")
    obj.Mode = mode
    obj.VolumeMode = "coordinates"
    obj.CoordinatePoint = point
    recomputeSelectionSetFromShapes(obj)
    if FreeCAD.GuiUp:
        apply_selectionset_view_defaults(obj)
    return obj


def renew_selection_references(doc):
    """Recompute all SelectionSets in doc and apply all SelectionSetLinks to their
    targets (doc-scoped equivalent of the macro toolbar button
    'Update all sets and links'). Run after a topology change, before meshing/solving.
    """
    n_sets = 0
    for obj in doc.Objects:
        if getattr(obj, "Proxy", None) is None:
            continue
        if hasattr(obj, "ElementList") and hasattr(obj, "MainObject"):
            try:
                if recomputeSelectionSetFromShapes(obj):
                    n_sets += 1
            except Exception as e:
                FreeCAD.Console.PrintWarning(
                    "Renew: failed to update SelectionSet '%s': %s\n" % (obj.Name, e)
                )
    if n_sets:
        doc.recompute()
    n_links = 0
    for obj in doc.Objects:
        if not hasattr(obj, "Proxy") or not hasattr(
            getattr(obj, "Proxy", None), "apply_to_target"
        ):
            continue
        try:
            selection_set_core._apply_link_to_target(obj)
            n_links += 1
        except Exception as e:
            FreeCAD.Console.PrintWarning(
                "Renew: failed to apply link '%s': %s\n" % (obj.Name, e)
            )
    if n_links:
        doc.recompute()
    FreeCAD.Console.PrintMessage(
        "Renew: %d SelectionSet(s) updated, %d SelectionSetLink(s) applied.\n"
        % (n_sets, n_links)
    )


def setup(doc=None, solvertype="ccxtools", test_mode=False, fillet=False):

    # init FreeCAD document
    if doc is None:
        doc = FreeCAD.newDocument()

    # geometric object: PartDesign Body instead of Part::Box
    geom_obj, sketch, pad = _make_partdesign_body(doc)
    if FreeCAD.GuiUp:
        geom_obj.ViewObject.Document.activeView().viewAxonometric()
        geom_obj.ViewObject.Document.activeView().fitAll()

    # fillet feature on the long top edge (suppressed by default)
    fillet_obj = _make_fillet_feature(geom_obj, pad)
    if fillet_obj and fillet:
        fillet_obj.Suppressed = False
    doc.recompute()

    # analysis
    analysis = ObjectsFem.makeAnalysis(doc, "Analysis")

    # solver (same settings as ccx_cantilever_base_solid)
    if solvertype == "ccxtools":
        solver_obj = ObjectsFem.makeSolverCalculiXCcxTools(doc, "CalculiXCcxTools")
        solver_obj.WorkingDir = ""
        solver_obj.SplitInputWriter = False
        solver_obj.AnalysisType = "static"
        solver_obj.GeometricalNonlinearity = False
        solver_obj.ThermoMechSteadyState = False
        solver_obj.MatrixSolverType = "default"
        solver_obj.IterationsControlParameterTimeUse = False
    else:
        FreeCAD.Console.PrintWarning(
            "Unknown or unsupported solver type: {}. No solver object was created.\n".format(
                solvertype
            )
        )
        solver_obj = None
    if solver_obj:
        analysis.addObject(solver_obj)

    # material
    material_obj = ObjectsFem.makeMaterialSolid(doc, "FemMaterial")
    mat = material_obj.Material
    mat["Name"] = "CalculiX-Steel"
    mat["YoungsModulus"] = "210000 MPa"
    mat["PoissonRatio"] = "0.30"
    material_obj.Material = mat
    analysis.addObject(material_obj)

    # constraint fixed
    # (the original uses Face1 of the Part::Box; the fixed end of the Body is Face4)
    con_fixed = ObjectsFem.makeConstraintFixed(doc, "ConstraintFixed")
    con_fixed.References = [(geom_obj, "Face4")]
    analysis.addObject(con_fixed)

    # mesh: geometry is the BODY, so it follows the body tip (pad or fillet)
    femmesh_obj = analysis.addObject(ObjectsFem.makeMeshGmsh(doc, "Mesh"))[0]
    femmesh_obj.Shape = geom_obj
    femmesh_obj.SecondOrderLinear = False
    if hasattr(femmesh_obj, "ElementOrder"):
        femmesh_obj.ElementOrder = "2nd"
    if hasattr(femmesh_obj, "CharacteristicLengthMax"):
        femmesh_obj.CharacteristicLengthMax = 200.0

    # generate the mesh
    if not test_mode:
        _generate_gmsh_mesh(femmesh_obj)

    # constraint force
    con_force = ObjectsFem.makeConstraintForce(doc, "ConstraintForce")
    con_force.References = [(geom_obj, "Face2")]
    con_force.Force = "9000000.0 N"
    con_force.Direction = (geom_obj, ["Edge5"])
    con_force.Reversed = True
    analysis.addObject(con_force)

    # --- SelectionSets and SelectionSetLinks (the circumvention) ---
    # SelectionSets store the geometric selection criteria (coordinates mode,
    # MainObject = Body). Their links re-apply the CURRENT references to the
    # FEM objects, so the allocations survive topology changes (see renew).
    ss_fixed = _make_selectionset(
        doc,
        "Cantilever_FixedFace",
        FreeCAD.Vector(0, 500, 500),
        "faces",
        "cantilever fixed face (x=0)",
    )
    ss_force = _make_selectionset(
        doc,
        "Cantilever_ForceFace",
        FreeCAD.Vector(8000, 500, 500),
        "faces",
        "cantilever force face (x=8000)",
    )
    ss_solid = _make_selectionset(
        doc,
        "Cantilever_Solid",
        FreeCAD.Vector(1000, 500, 500),
        "solids",
        "cantilever solid",
    )
    # Direction edge of the force: vertical edge at the free end (y = width side)
    ss_direction = _make_selectionset(
        doc,
        "Cantilever_ForceDirectionEdge",
        FreeCAD.Vector(8000, 1000, 500),
        "edges",
        "cantilever force direction edge (vertical)",
    )
    doc.recompute()

    # material reference from the solid SelectionSet
    link_material = createSelectionSetLink(
        name="Link_Material",
        _target=material_obj,
        _add_sets=[ss_solid],
        _add_shapes=[],
        _targets=[material_obj],
    )
    if link_material:
        link_material.Label = "SelectionSetLink cantilever (1 solid) Material"
        link_material.ShapeRefMode = "solids"
        link_material.UseOneByOneWorkaround = True
        selection_set_core._apply_link_to_target(link_material)

    # constraint references from the face SelectionSets
    for link_name, constraint, ss in (
        ("Link_Fixed", con_fixed, ss_fixed),
        ("Link_Force", con_force, ss_force),
    ):
        link = createSelectionSetLink(
            name=link_name,
            _target=constraint,
            _add_sets=[ss],
            _add_shapes=[],
            _targets=[constraint],
        )
        if not link:
            continue
        n = len(getattr(ss, "ElementList", []) or [])
        unit = "face" if n == 1 else "faces"
        link.Label = "SelectionSetLink cantilever (%d %s) %s" % (
            n,
            unit,
            link_name.split("_")[1],
        )
        link.UseOneByOneWorkaround = True
        constraint.References = []
        refs = [
            r for r in get_fem_references_from_selectionsets([ss]) if r[0] is geom_obj
        ]
        if refs:
            apply_references_to_fem_constraint_one_by_one(refs, constraint, doc)

    # direction reference of the force constraint: the Direction property is a
    # separate reference and also breaks on topology changes, so it gets its own
    # edges SelectionSet and a link with TargetProperty = 'Direction'
    link_direction = createSelectionSetLink(
        name="Link_ForceDirection",
        _target=con_force,
        _add_sets=[ss_direction],
        _add_shapes=[],
        _targets=[con_force],
    )
    if link_direction:
        link_direction.Label = "SelectionSetLink cantilever (1 edge) Force direction"
        link_direction.TargetProperty = "Direction"
        link_direction.UseOneByOneWorkaround = True
        selection_set_core._apply_link_to_target(link_direction)

    # readme with the expected behaviour and values (same label/content family
    # as the macro example's FEM_PDBeam_Readme), placed in the group below
    try:
        td = doc.getObject("FEM_PDBeam_Readme")
        if td is None:
            td = doc.addObject("App::TextDocument", "FEM_PDBeam_Readme")
        if td is not None:
            td.Label = "FEM PD beam – readme and expected values"
            td.Text = """FEM Cantilever Beam (PartDesign Body, SelectionSets) – how to use this example

Geometry: PartDesign Body 'Body': sketch 8000 x 1000 mm on XY + pad 1000 mm.
Mesh geometry is the BODY ('Mesh'.Shape = Body), so it always follows the body
tip (pad or fillet).
Fillet feature 'Fillet' on the LONG top edge (full length, y=0 side); radius
100 mm (suppressed by default).

Face numbering of the Body (verified on FreeCAD 1.1.4):
• Without fillet (fillet suppressed): force face (x=8000) = Face2, fixed face (x=0) = Face4
• With fillet:                          force face (x=8000) = Face5, fixed face (x=0) = Face2

The demonstration:
1. The constraints start with DIRECT references (see their 'References' property):
   fixed -> Face4, force -> Face2, direction -> Edge5 (valid for the plain pad).
2. Set 'Fillet'.Suppressed = False in the Data tab and recompute.
   The face numbering changes and the direct references break (invalidated as
   '?FaceN'/'?EdgeN' on FreeCAD 1.1, silently wrong face on 1.0).
3. Run renew_selection_references(doc) from this file (or the macro toolbar
   button 'Update all sets and links'). The SelectionSets (coordinates mode,
   MainObject = Body) reevaluate and the SelectionSetLinks re-apply the
   intended references: fixed face at x=0, force face at x=8000, and the
   vertical direction edge at the free end (Link_ForceDirection -> Direction).
4. Check the constraints' References and Direction, then mesh and solve.

Expected max deflection (mesh size 200 mm, CalculiX-Steel):
• Without fillet: ~88.4 mm
• With fillet (r=100 mm): slightly above (removed material at the top edge).

Warning: without step 3 the constraint references stay stale (invalid or wrong):
the analysis then fails or produces wrong results without an obvious error message.
"""
    except Exception:
        pass

    # group the SelectionSets, links, and readme (tree clarity)
    group_members = [
        o
        for o in (
            ss_fixed,
            ss_force,
            ss_solid,
            ss_direction,
            link_material,
            doc.getObject("Link_Fixed"),
            doc.getObject("Link_Force"),
            doc.getObject("Link_ForceDirection"),
            doc.getObject("FEM_PDBeam_Readme"),
        )
        if o
    ]
    if group_members:
        grp = doc.getObject("SelectionSetGroup")
        if grp is None:
            grp = doc.addObject("App::DocumentObjectGroup", "SelectionSetGroup")
        grp.Label = "SelectionSets and links"
        for o in group_members:
            grp.addObject(o)
        doc.recompute()

    doc.recompute()
    return doc


# Executed via the FreeCAD Macro menu (runs in a copy of the __main__ namespace)
# or via exec(open(...).read()) from the Python console: build the example.
# A plain 'import' of this file does NOT trigger setup().
if __name__ == "__main__":
    setup()
