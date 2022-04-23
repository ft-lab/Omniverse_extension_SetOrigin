# -----------------------------------------------------.
# Replaces the center of the Mesh.
# -----------------------------------------------------.
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Tf

class ReplaceMeshCenter:
    def __init__(self):
        pass

    def replaceMeshVertices (self, targetPrim : Usd.Prim, centerPos : Gf.Vec3f):
        if targetPrim.IsA(UsdGeom.Mesh) == False:
            return
        
        meshGeom = UsdGeom.Mesh(targetPrim)

        tV = targetPrim.GetAttribute("xformOp:translate").Get()
        if tV == None:
            tV = Gf.Vec3f(0, 0, 0)

        vers = meshGeom.GetPointsAttr().Get()
        for i in range(len(vers)):
            v = vers[i]
            v = v + Gf.Vec3f(tV) - centerPos
            vers[i] = v

        meshGeom.CreatePointsAttr(vers)

        # Set position.
        UsdGeom.XformCommonAPI(meshGeom).SetTranslate((centerPos[0], centerPos[1], centerPos[2]))


