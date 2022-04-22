from pxr import Usd, UsdGeom, UsdSkel, UsdPhysics, UsdShade, UsdSkel, Sdf, Gf, Tf
import omni.ext
import carb.events
import omni.usd

# ----------------------------------------------------.
class SetOriginExtension (omni.ext.IExt):
    # ------------------------------------------.
    # Update event.
    # ------------------------------------------.
    def on_update (self, e: carb.events.IEvent):
        pass

    # ------------------------------------------.
    # Extension startup.
    # ------------------------------------------.
    def on_startup (self, ext_id):
        print("[ft_lab.Tools.SetOrigin] startup")

    # ------------------------------------------.
    # Extension shutdown.
    # ------------------------------------------.
    def on_shutdown(self):
        print("[ft_lab.Tools.SetOrigin] shutdown")


