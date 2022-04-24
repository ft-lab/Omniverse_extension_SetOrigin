# -----------------------------------------------------.
# Replaces the center of the Mesh.
# -----------------------------------------------------.
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Tf

from .MathUtil import *

class ReplaceMeshCenter:
    def __init__(self):
        pass

    def replaceMeshVertices (self, targetPrim : Usd.Prim, centerPos : Gf.Vec3f):
        tV = targetPrim.GetAttribute("xformOp:translate").Get()
        if tV == None:
            tV = Gf.Vec3f(0, 0, 0)
        
        localM = GetLocalMatrix(targetPrim)
        localInvM = localM.GetInverse()
        centerPosL = localInvM.Transform(centerPos)

        if targetPrim.IsA(UsdGeom.Mesh):
            meshGeom = UsdGeom.Mesh(targetPrim)

            vers = meshGeom.GetPointsAttr().Get()
            for i in range(len(vers)):
                v = vers[i]
                vers[i] = v - centerPosL

            meshGeom.CreatePointsAttr(vers)

            # Set position.
            UsdGeom.XformCommonAPI(meshGeom).SetTranslate((centerPos[0], centerPos[1], centerPos[2]))
        else:
            p = tV - centerPos
            UsdGeom.XformCommonAPI(meshGeom).SetTranslate((p[0], p[1], p[2]))

