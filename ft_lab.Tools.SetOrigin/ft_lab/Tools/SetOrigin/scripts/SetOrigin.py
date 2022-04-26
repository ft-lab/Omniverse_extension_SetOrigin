# -----------------------------------------------------.
# Change the center.
# -----------------------------------------------------.
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Tf
import omni.usd
import omni.kit.commands
import omni.kit.undo

from .CalcWorldBoundingBox import CalcWorldBoundingBox
from .MathUtil import *
from .TransformUtil import *

# ------------------------------------------------------------------------.
# Change Mesh Center
# ------------------------------------------------------------------------.
class ToolReplaceCenter (omni.kit.commands.Command):
    _prim          = None
    _centerPos     = None
    _pivot         = False
    _prevTranslate = None
    _prevPivot     = None
    _centerPosL    = None

    # prim            : Target prim.
    # center_position : Position of the center in world coordinates.
    # use_pivot       : True if adjusting using Pivot.
    def __init__ (self, prim : Usd.Prim, center_position : Gf.Vec3f, use_pivot : bool = False):
        self._prim      = prim
        self._centerPos = center_position
        self._pivot     = use_pivot

    # Execute process.
    def do (self):
        self._prevTranslate = self._prim.GetAttribute("xformOp:translate").Get()
        if self._prevTranslate == None:
            self._prevTranslate = Gf.Vec3f(0, 0, 0)

        self._prevPivot = self._prim.GetAttribute("xformOp:translate:pivot").Get()

        localM = GetWorldMatrix(self._prim).GetInverse()
        self._centerPosL = localM.Transform(self._centerPos)

        if self._prim.IsA(UsdGeom.Mesh):
            parentLocalM = GetWorldMatrix(self._prim.GetParent()).GetInverse()

            if self._pivot == False:
                meshGeom = UsdGeom.Mesh(self._prim)

                vers = meshGeom.GetPointsAttr().Get()
                for i in range(len(vers)):
                    v = vers[i]
                    vers[i] = v - self._centerPosL
                meshGeom.CreatePointsAttr(vers)

                # Set position.
                p = parentLocalM.Transform(self._centerPos)
                TUtil_SetTranslate(self._prim, Gf.Vec3f(p))

                # Set pivot(0, 0, 0).
                if self._prevPivot != None:
                    TUtil_SetPivot(self._prim, Gf.Vec3f(0, 0, 0))
            else:
                p = parentLocalM.Transform(self._centerPos)
                m2 = GetLocalMatrix(self._prim).GetInverse()
                p = m2.Transform(p)
                self._prim.CreateAttribute("xformOp:translate:pivot", Sdf.ValueTypeNames.Float3, False).Set(Gf.Vec3f(p))

    # Undo process.
    def undo (self):
        if self._prim.IsA(UsdGeom.Mesh):
            if self._pivot == False:
                meshGeom = UsdGeom.Mesh(self._prim)

                vers = meshGeom.GetPointsAttr().Get()
                for i in range(len(vers)):
                    v = vers[i]
                    vers[i] = v + self._centerPosL

                meshGeom.CreatePointsAttr(vers)

                # Set position.
                TUtil_SetTranslate(self._prim, Gf.Vec3f(self._prevTranslate))

                # Set pivot.
                if self._prevPivot != None:
                    TUtil_SetPivot(self._prim, Gf.Vec3f(self._prevPivot))
            else:
                if self._prevPivot != None:
                    TUtil_SetPivot(self._prim, Gf.Vec3f(self._prevPivot))
                else:
                    TUtil_SetPivot(self._prim, Gf.Vec3f(0, 0, 0))

# ------------------------------------------------------------------------.
class SetOrigin:
    def __init__(self):
        pass

    # Get selected Prim.
    def _getSelectedPrim (self):
        # Get stage.
        stage = omni.usd.get_context().get_stage()

        # Get selection.
        selection = omni.usd.get_context().get_selection()
        paths = selection.get_selected_prim_paths()

        prim = None
        for path in paths:
            prim = stage.GetPrimAtPath(path)
            break
        return prim

    def doCenterOfGeometry (self):
        prim = self._getSelectedPrim()
        if prim == None:
            return
        
        # Calculate world center from bounding box.
        bbox = CalcWorldBoundingBox(prim)
        bbMin, bbMax = bbox.calcBoundingBox()
        bbCenter = (bbMin + bbMax) * 0.5

        # Register a Class and run it.
        omni.kit.commands.register(ToolReplaceCenter)
        omni.kit.commands.execute("ToolReplaceCenter", prim=prim, center_position=bbCenter)
        
    def doCenterOfGeometry_pivot (self):
        prim = self._getSelectedPrim()
        if prim == None:
            return
        
        # Calculate world center from bounding box.
        bbox = CalcWorldBoundingBox(prim)
        bbMin, bbMax = bbox.calcBoundingBox()
        bbCenter = (bbMin + bbMax) * 0.5

        # Register a Class and run it.
        omni.kit.commands.register(ToolReplaceCenter)
        omni.kit.commands.execute("ToolReplaceCenter", prim=prim, center_position=bbCenter, use_pivot=True)

