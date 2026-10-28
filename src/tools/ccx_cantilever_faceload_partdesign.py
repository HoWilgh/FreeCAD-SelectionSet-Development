# Development helper derived from FreeCAD FEM examples (ccx_cantilever_faceload).
# Builds the same cantilever face-load setup, but the geometry is a PartDesign Body
# (sketch + pad), so further PartDesign features (e.g. the fillet created here) can be
# introduced. The mesh geometry is the Body. Direct constraint references are used,
# exactly as in the original example. Introducing the fillet (Fillet.Suppressed = False)
# changes the face numbering of the Body, so these direct references break:
# force face Face2 -> Face5 and Face2 then names the fixed end.
# The companion file ccx_cantilever_faceload_partdesign_selectionset.py extends this
# setup with SelectionSets and SelectionSetLinks to circumvent that issue.
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

import FreeCAD
import Part
import ObjectsFem


def get_information():
    return {
        "name": "CCX cantilever face load (PartDesign body)",
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
  exec(open("<repo>/src/tools/ccx_cantilever_faceload_partdesign.py").read())

The cantilever is a PartDesign Body (sketch 8000 x 1000 + pad 1000), like
ccx_cantilever_faceload, but with feature-based geometry. A fillet feature on
the long top edge is created and suppressed. Set Fillet.Suppressed = False and
recompute to introduce it: the face numbering of the Body changes and the
direct references of the constraints break. This file demonstrates the
conventional (breaking) workflow.


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
        if "XY_Plane" in (getattr(o, "Name", "") or "") and body in getattr(o, "InListRecursive", []):
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
        FreeCAD.Console.PrintWarning("Fillet: long top edge not found; no fillet created.\n")
        return None
    fillet = body.newObject("PartDesign::Fillet", "Fillet")
    fillet.Base = (pad, [edge_name])
    for rad_prop in ("Radius", "FilletRadius"):
        if hasattr(fillet, rad_prop):
            setattr(fillet, rad_prop, radius)
            break
    fillet.Suppressed = True  # introduce it later to break the direct references
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
            "Unknown or unsupported solver type: {}. No solver object was created.\n".format(solvertype)
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

    doc.recompute()
    return doc


# Executed via the FreeCAD Macro menu (runs in a copy of the __main__ namespace)
# or via exec(open(...).read()) from the Python console: build the example.
# A plain 'import' of this file does NOT trigger setup().
if __name__ == "__main__":
    setup()
