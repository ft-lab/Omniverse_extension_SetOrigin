from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.kit.commands

# ---------------------------.
# Set Translate.
# ---------------------------.
def TUtil_SetTranslate (prim : Usd.Prim, tV : Gf.Vec3f):
    trans = prim.GetAttribute("xformOp:translate").Get()

    if trans != None:
        # Specify a value for each type.
        if type(trans) == Gf.Vec3f:
            prim.GetAttribute("xformOp:translate").Set(Gf.Vec3f(tV))
        elif type(trans) == Gf.Vec3d:
            prim.GetAttribute("xformOp:translate").Set(Gf.Vec3d(tV))
    else:
        # xformOpOrder is also updated.
        xformAPI = UsdGeom.XformCommonAPI(prim)
        xformAPI.SetTranslate(Gf.Vec3d(tV))

# ---------------------------.
# Set Scale.
# ---------------------------.
def TUtil_SetScale (prim : Usd.Prim, sV : Gf.Vec3f):
    scale = prim.GetAttribute("xformOp:scale").Get()

    if scale != None:
        # Specify a value for each type.
        if type(scale) == Gf.Vec3f:
            prim.GetAttribute("xformOp:scale").Set(Gf.Vec3f(sV))
        elif type(scale) == Gf.Vec3d:
            prim.GetAttribute("xformOp:scale").Set(Gf.Vec3d(sV))
    else:
        # xformOpOrder is also updated.
        xformAPI = UsdGeom.XformCommonAPI(prim)
        xformAPI.SetScale(Gf.Vec3f(sV))

# ---------------------------.
# Set Rotate.
# ---------------------------.
def TUtil_SetRotate (prim : Usd.Prim, rV : Gf.Vec3f):
    # Get rotOrder.
    # If rotation does not exist, rotOrder = UsdGeom.XformCommonAPI.RotationOrderXYZ.
    xformAPI = UsdGeom.XformCommonAPI(prim)
    time_code = Usd.TimeCode.Default()
    translation, rotation, scale, pivot, rotOrder = xformAPI.GetXformVectors(time_code)

    # Convert rotOrder to "xformOp:rotateXYZ" etc.
    t = xformAPI.ConvertRotationOrderToOpType(rotOrder)
    rotateAttrName = "xformOp:" + UsdGeom.XformOp.GetOpTypeToken(t)

    # Set rotate.
    rotate = prim.GetAttribute(rotateAttrName).Get()
    if rotate != None:
        # Specify a value for each type.
        if type(rotate) == Gf.Vec3f:
            prim.GetAttribute(rotateAttrName).Set(Gf.Vec3f(rV))
        elif type(rotate) == Gf.Vec3d:
            prim.GetAttribute(rotateAttrName).Set(Gf.Vec3d(rV))
    else:
        # xformOpOrder is also updated.
        xformAPI.SetRotate(Gf.Vec3f(rV), rotOrder)

# ---------------------------.
# Set Pivot.
# ---------------------------.
def TUtil_SetPivot (prim : Usd.Prim, pV : Gf.Vec3f):
    pivot = prim.GetAttribute("xformOp:translate:pivot").Get()

    if pivot != None:
        # Specify a value for each type.
        if type(pivot) == Gf.Vec3f:
            prim.GetAttribute("xformOp:translate:pivot").Set(Gf.Vec3f(pV))
        elif type(pivot) == Gf.Vec3d:
            prim.GetAttribute("xformOp:translate:pivot").Set(Gf.Vec3d(pV))
    else:
        # xformOpOrder is also updated.
        # ["xformOp:translate", "xformOp:translate:pivot", "xformOp:rotateXYZ", "xformOp:scale", "!invert!xformOp:translate:pivot"]
        # The following do not work correctly?
        #xformAPI = UsdGeom.XformCommonAPI(prim)
        #xformAPI.SetPivot(Gf.Vec3f(pV))

        prim.CreateAttribute("xformOp:translate:pivot", Sdf.ValueTypeNames.Float3, False).Set(Gf.Vec3f(pV))

        # ["xformOp:translate", "xformOp:rotateXYZ", "xformOp:scale", "xformOp:translate:pivot", "!invert!xformOp:translate:pivot"]
        transformOrder = prim.GetAttribute("xformOpOrder").Get()
        orderList = []
        for sV in transformOrder:
            orderList.append(sV)
        orderList.append("xformOp:translate:pivot")
        orderList.append("!invert!xformOp:translate:pivot")
        prim.GetAttribute("xformOpOrder").Set(orderList)





