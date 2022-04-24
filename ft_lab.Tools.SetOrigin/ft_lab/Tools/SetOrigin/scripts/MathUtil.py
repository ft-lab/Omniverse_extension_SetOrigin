# -----------------------------------------------------.
# Math functions.
# -----------------------------------------------------.
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Tf

# Get local matrix.
def GetLocalMatrix (prim : Usd.Prim):
    xformCache = UsdGeom.XformCache(0)
    curM = xformCache.GetLocalToWorldTransform(prim)
    parentPrim = prim.GetParent()
    matrix = curM * xformCache.GetLocalToWorldTransform(parentPrim).GetInverse()
    return matrix
