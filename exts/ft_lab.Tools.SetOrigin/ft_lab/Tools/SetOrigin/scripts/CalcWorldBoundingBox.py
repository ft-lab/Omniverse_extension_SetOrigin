# -----------------------------------------------------.
# # Calculate bounding box in world coordinates.
# -----------------------------------------------------.
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Tf

def CalcWorldBoundingBox (prim : Usd.Prim):
    # Calc world boundingBox.
    bboxCache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), ["default"])
    bboxD = bboxCache.ComputeWorldBound(prim).ComputeAlignedRange()
    bb_min = Gf.Vec3f(bboxD.GetMin())
    bb_max = Gf.Vec3f(bboxD.GetMax())
    
    return bb_min, bb_max

