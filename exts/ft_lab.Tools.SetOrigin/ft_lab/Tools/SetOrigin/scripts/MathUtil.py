# -----------------------------------------------------.
# Math functions.
# -----------------------------------------------------.
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Tf

# Get local matrix.
def GetLocalMatrix (prim : Usd.Prim):
    xformCache = UsdGeom.XformCache()
    curM = xformCache.GetLocalToWorldTransform(prim)
    parentPrim = prim.GetParent()
    matrix = curM * xformCache.GetLocalToWorldTransform(parentPrim).GetInverse()
    return matrix

# Get world matrix.
def GetWorldMatrix (prim : Usd.Prim):
    xformCache = UsdGeom.XformCache()
    return xformCache.GetLocalToWorldTransform(prim)
