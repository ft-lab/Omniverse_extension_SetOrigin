from pxr import Usd, UsdGeom, UsdSkel, UsdPhysics, UsdShade, UsdSkel, Sdf, Gf, Tf
import omni.ext
import omni.usd
import omni.kit.menu.utils
import omni.kit.undo
import omni.kit.commands
from omni.kit.menu.utils import MenuItemDescription
import asyncio

from .scripts.SetOrigin import SetOrigin

# ----------------------------------------------------.
class SetOriginExtension (omni.ext.IExt):
    # Menu list.
    _menu_list = None
    _sub_menu_list = None

    # Menu name.
    _menu_name = "Tools"

    # ------------------------------------------.
    # Initialize menu.
    # ------------------------------------------.
    def init_menu (self):
        async def _rebuild_menus():
            await omni.kit.app.get_app().next_update_async()
            omni.kit.menu.utils.rebuild_menus()

        def menu_select (mode):
            if mode == 0:
                setOrigin = SetOrigin()
                setOrigin.doCenterOfGeometry()

        self._sub_menu_list = [
            MenuItemDescription(name="Center of Geometry", onclick_fn=lambda: menu_select(0)),
        ]

        self._menu_list = [
            MenuItemDescription(name="Set Origin", sub_menu=self._sub_menu_list),
        ]

        # Rebuild with additional menu items.
        omni.kit.menu.utils.add_menu_items(self._menu_list, self._menu_name)
        asyncio.ensure_future(_rebuild_menus())

    # ------------------------------------------.
    # Term menu.
    # It seems that the additional items in the top menu will not be removed.
    # ------------------------------------------.
    def term_menu (self):
        async def _rebuild_menus():
            await omni.kit.app.get_app().next_update_async()
            omni.kit.menu.utils.rebuild_menus()

        # Remove and rebuild the added menu items.
        omni.kit.menu.utils.remove_menu_items(self._menu_list, self._menu_name)
        asyncio.ensure_future(_rebuild_menus())

    # ------------------------------------------.

    # ------------------------------------------.
    # Extension startup.
    # ------------------------------------------.
    def on_startup (self, ext_id):
        print("[ft_lab.Tools.SetOrigin] startup")

        # Initialize menu.
        self.init_menu()

    # ------------------------------------------.
    # Extension shutdown.
    # ------------------------------------------.
    def on_shutdown(self):
        print("[ft_lab.Tools.SetOrigin] shutdown")

        # Term menu.
        self.term_menu()

