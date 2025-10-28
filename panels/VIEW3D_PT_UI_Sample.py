import bpy  # type: ignore
from ..constants import AddonProperties
from ..constants import get_operator
from .. import conduit_connector

class VIEW3D_PT_UI_Sample(bpy.types.Panel):
    bl_label = "Asset Manager"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = AddonProperties.panel_category
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()

        # show current connector status
        conn = conduit_connector.get_global_connector()
        status = "Running" if (conn and conn.is_running()) else "Stopped"
        box.label(text=f"Server: {status}")

        # save new version
        box = layout.box()
        box.label(text="someText")
        box.operator(get_operator("save_to_master"))
        