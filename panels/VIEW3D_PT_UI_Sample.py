import bpy  # type: ignore
from ..constants import AddonProperties
from ..constants import get_operator
from ..ConduitConnect import Connector
from ..Mock import Asset
import time

class VIEW3D_PT_UI_Sample(bpy.types.Panel):
    _cached_asset: Asset | None = None
    _last_fetch: float = 0
    bl_label = "Asset Manager"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = AddonProperties.panel_category
    
    def draw(self, context):
        now = time.time()
        # Refresh every 2 seconds
        if now - self._last_fetch > 2.0:
            connector = Connector()
            self._cached_asset = connector.get_asset()
            self._last_fetch = now

        asset = self._cached_asset
        layout = self.layout
        box = layout.box()

        if asset:
            box.label(text=asset.name)
            if len(asset.tasks) == 0:
                row = box.row()
                row.enabled = False
                row.label(text="no tasks found")
            for task in asset.tasks:
                box.operator(get_operator("operator"), text=f"link {task.name}", icon="BLENDER")

