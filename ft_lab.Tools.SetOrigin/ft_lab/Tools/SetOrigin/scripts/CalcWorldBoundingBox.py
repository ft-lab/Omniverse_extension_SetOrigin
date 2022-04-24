# -----------------------------------------------------.
# Calculate Bounding Boxes(world coordinate) in Prims.
# -----------------------------------------------------.
from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Tf
from .MathUtil import *

class CalcWorldBoundingBox:
    _target_prim = None
    _target_world_transform = None      # Gf.Matrix4d
    _xformCache = None

    def __init__(self, targetPrim : Usd.Prim):
        self._target_prim = targetPrim

        # Get world Transform.
        self._xformCache = UsdGeom.XformCache()
        self._target_world_transform = self._xformCache.GetLocalToWorldTransform(targetPrim)

    # Get Prims of Mesh.
    def _getMeshPrims (self, prim : Usd.Prim):
        prims = []
        for prim in Usd.PrimRange(self._target_prim):
            if prim.IsA(UsdGeom.Mesh) and prim.IsValid():      # For Mesh.
                # Get visibility.
                primImageable = UsdGeom.Imageable(prim)
                if (primImageable.ComputeVisibility() == 'invisible'):
                    continue
                prims.append(prim)
        return prims

    # Calculate bounding box for one mesh.
    def _calcMeshBoundingBox (self, prim : Usd.Prim):
        # Get world Transform.
        globalM = self._xformCache.GetLocalToWorldTransform(prim)

        meshGeom = UsdGeom.Mesh(prim)
        bb_min = Gf.Vec3f(0.0, 0.0, 0.0)
        bb_max = Gf.Vec3f(0.0, 0.0, 0.0)
        firstF = True
        vers = meshGeom.GetPointsAttr().Get()
        for v in vers:
            v = globalM.Transform(v)     # Convert to world coordinates.
            if firstF:
                firstF = False
                bb_min = Gf.Vec3f(v)
                bb_max = Gf.Vec3f(v)
            bb_min[0] = min(bb_min[0], v[0])
            bb_min[1] = min(bb_min[1], v[1])
            bb_min[2] = min(bb_min[2], v[2])
            bb_max[0] = max(bb_max[0], v[0])
            bb_max[1] = max(bb_max[1], v[1])
            bb_max[2] = max(bb_max[2], v[2])
        
        return bb_min, bb_max

    def calcBoundingBox (self):
        bb_min = Gf.Vec3f(0.0, 0.0, 0.0)
        bb_max = Gf.Vec3f(0.0, 0.0, 0.0)

        # Get Prims of Mesh.
        prims = self._getMeshPrims(self._target_prim)

        firstF = True
        for prim in prims:
            _bbMin, _bbMax = self._calcMeshBoundingBox(prim)
            if firstF:
                firstF = False
                bb_min = _bbMin
                bb_max = _bbMax
            
            bb_min[0] = min(bb_min[0], _bbMin[0])
            bb_min[1] = min(bb_min[1], _bbMin[1])
            bb_min[2] = min(bb_min[2], _bbMin[2])
            bb_max[0] = max(bb_max[0], _bbMax[0])
            bb_max[1] = max(bb_max[1], _bbMax[1])
            bb_max[2] = max(bb_max[2], _bbMax[2])

        return bb_min, bb_max




