# -----------------------------------------------------.
# Change the center.
# -----------------------------------------------------.
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Tf
import omni.usd
import omni.kit.commands
import omni.kit.undo

from .CalcBoundingBox import CalcBoundingBox
from .MathUtil import *

# ------------------------------------------------------------------------.
# Move a Mesh verteices to change its center.
# ------------------------------------------------------------------------.
class ToolReplaceMeshVertices (omni.kit.commands.Command):
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
        
        localM = GetLocalMatrix(self._prim)
        localInvM = localM.GetInverse()
        self._centerPosL = localInvM.Transform(self._centerPos)

        if self._prim.IsA(UsdGeom.Mesh):
            meshGeom = UsdGeom.Mesh(self._prim)

            vers = meshGeom.GetPointsAttr().Get()
            for i in range(len(vers)):
                v = vers[i]
                vers[i] = v - self._centerPosL

            meshGeom.CreatePointsAttr(vers)

            # Set position.
            UsdGeom.XformCommonAPI(meshGeom).SetTranslate((self._centerPos[0], self._centerPos[1], self._centerPos[2]))

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
        
        # Calculate center from bounding box.
        bbox = CalcBoundingBox(prim)
        bbMin, bbMax = bbox.calcBoundingBox()
        print("bbMin : " + str(bbMin))
        print("bbMax : " + str(bbMax))

        bbCenter = (bbMin + bbMax) * 0.5
        print(bbCenter)

        # Register a Class and run it.
        omni.kit.commands.register(ToolReplaceMeshVertices)
        omni.kit.commands.execute("ToolReplaceMeshVertices", prim=prim, centerPos=bbCenter)
        




