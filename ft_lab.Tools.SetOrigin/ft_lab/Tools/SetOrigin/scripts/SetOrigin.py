# -----------------------------------------------------.
# Change the center.
# -----------------------------------------------------.
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Tf
import omni.usd
import omni.kit.commands
import omni.kit.undo

from .CalcWorldBoundingBox import CalcWorldBoundingBox
from .MathUtil import *

# ------------------------------------------------------------------------.
# Change Mesh Center
# ------------------------------------------------------------------------.
class ToolReplaceCenter (omni.kit.commands.Command):
    _prim = None
    _centerPos = None
    _prevTranslate = None
    _centerPosL = None

    def __init__ (self, prim : Usd.Prim, centerPos : Gf.Vec3f):
        self._prim      = prim
        self._centerPos = centerPos

    def do (self):
        self._prevTranslate = self._prim.GetAttribute("xformOp:translate").Get()
        if self._prevTranslate == None:
            self._prevTranslate = Gf.Vec3f(0, 0, 0)
        
        localM = GetWorldMatrix(self._prim).GetInverse()
        self._centerPosL = localM.Transform(self._centerPos)

        if self._prim.IsA(UsdGeom.Mesh):
            meshGeom = UsdGeom.Mesh(self._prim)

            vers = meshGeom.GetPointsAttr().Get()
            for i in range(len(vers)):
                v = vers[i]
                vers[i] = v - self._centerPosL

            meshGeom.CreatePointsAttr(vers)

            parentLocalM = GetWorldMatrix(self._prim.GetParent()).GetInverse()
            p = parentLocalM.Transform(self._centerPos)

            # Set position.
            UsdGeom.XformCommonAPI(meshGeom).SetTranslate((p[0], p[1], p[2]))

    def undo (self):
        if self._prim.IsA(UsdGeom.Mesh):
            meshGeom = UsdGeom.Mesh(self._prim)

            vers = meshGeom.GetPointsAttr().Get()
            for i in range(len(vers)):
                v = vers[i]
                vers[i] = v + self._centerPosL

            meshGeom.CreatePointsAttr(vers)

            # Set position.
            UsdGeom.XformCommonAPI(meshGeom).SetTranslate((self._prevTranslate[0], self._prevTranslate[1], self._prevTranslate[2]))

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
        omni.kit.commands.execute("ToolReplaceCenter", prim=prim, centerPos=bbCenter)
        




