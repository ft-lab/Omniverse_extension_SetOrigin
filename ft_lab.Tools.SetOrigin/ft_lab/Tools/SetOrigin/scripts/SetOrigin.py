# -----------------------------------------------------.
# Change the center.
# -----------------------------------------------------.
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Tf
import omni.usd
import omni.kit.commands
import omni.kit.undo

from .CalcWorldBoundingBox import *
from .MathUtil import *
from .TransformUtil import *

# Check if Prim can handle.
def _checkPrim (prim : Usd.Prim):
    if prim == None:
        return False
    if prim.IsA(UsdGeom.Mesh) == False and prim.IsA(UsdGeom.Xform) == False:
        return False
    
    # Skip for reference.
    #if prim.HasAuthoredReferences():
    #    return False
    return True

# ------------------------------------------------------------------------.
# Change Mesh Center
# ------------------------------------------------------------------------.
class ToolSetOrigin (omni.kit.commands.Command):
    _prim          = None
    _centerWPos    = None
    _targetCenterWPos = None
    _prevTranslate = None
    _prevPivot     = None

    # prim            : Target prim.
    # center_position : Position of the center in world coordinates.
    def __init__ (self, prim : Usd.Prim, center_position : Gf.Vec3f):
        self._prim = prim
        self._targetCenterWPos = center_position

        # Calculate world center from bounding box.
        bbMin, bbMax = CalcWorldBoundingBox(prim)
        self._centerWPos = (bbMin + bbMax) * 0.5

    # Execute process.
    def do (self):
        if _checkPrim(self._prim) == False:
            return

        self._prevTranslate = self._prim.GetAttribute("xformOp:translate").Get()
        if self._prevTranslate == None:
            self._prevTranslate = Gf.Vec3f(0, 0, 0)

        self._prevPivot = self._prim.GetAttribute("xformOp:translate:pivot").Get()

        localM = GetWorldMatrix(self._prim).GetInverse()
        centerPosL = localM.Transform(self._targetCenterWPos)

        TUtil_SetPivot(self._prim, Gf.Vec3f(centerPosL))

        # Calculate world center from bounding box.
        bbMin, bbMax = CalcWorldBoundingBox(self._prim)
        bbCenter = (bbMin + bbMax) * 0.5

        # Recalculate the center position in world coordinates and correct for any misalignment.
        ddV = Gf.Vec3f(bbCenter - self._centerWPos)
        fMin = 1e-6
        if abs(ddV[0]) > fMin or abs(ddV[1]) > fMin or abs(ddV[2]) > fMin:
            parentLocalM = GetWorldMatrix(self._prim.GetParent()).GetInverse()
            p1 = parentLocalM.Transform(self._centerWPos)
            p2 = parentLocalM.Transform(bbCenter)

            transV = self._prim.GetAttribute("xformOp:translate").Get()
            if transV == None:
                transV = Gf.Vec3f(0, 0, 0)
            transV = Gf.Vec3f(transV) + (p1 - p2)
            TUtil_SetTranslate(self._prim, Gf.Vec3f(transV))

    # Undo process.
    def undo (self):
        if _checkPrim(self._prim) == False:
            return

        TUtil_SetTranslate(self._prim, Gf.Vec3f(self._prevTranslate))
        if self._prevPivot != None:
            TUtil_SetPivot(self._prim, Gf.Vec3f(self._prevPivot))
        else:
            TUtil_DeletePivot(self._prim)


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

        if _checkPrim(prim) == False:
            return

        # Calculate world center from bounding box.
        bbMin, bbMax = CalcWorldBoundingBox(prim)
        bbCenter = (bbMin + bbMax) * 0.5

        # Register a Class and run it.
        omni.kit.commands.register(ToolSetOrigin)
        omni.kit.commands.execute("ToolSetOrigin", prim=prim, center_position=bbCenter)
       

    def doLowerCenterOfGeometry (self):
        prim = self._getSelectedPrim()

        if _checkPrim(prim) == False:
            return

        # Calculate world lower center from bounding box.
        bbMin, bbMax = CalcWorldBoundingBox(prim)
        bbCenter = Gf.Vec3f((bbMin[0] + bbMax[0]) * 0.5, bbMin[1], (bbMin[2] + bbMax[2]) * 0.5)

        # Register a Class and run it.
        omni.kit.commands.register(ToolSetOrigin)
        omni.kit.commands.execute("ToolSetOrigin", prim=prim, center_position=bbCenter)
