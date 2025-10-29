import bpy  # type: ignore
from ..constants import AddonProperties
from .. import BlenderServer
from ..ConduitClient import get_heartbeat

class VIEW3D_PT_UI_ServerStatus(bpy.types.Panel):
    bl_label = "Server Status"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = AddonProperties.panel_category
    
    def draw(self, context):
        layout = self.layout

        hb = get_heartbeat()
        hb_box = layout.box()
        if hb:
            hb_box.label(text="Conduit: Connected", icon="CHECKMARK")
        else:
            hb_box.label(text="Conduit: Offline", icon="ERROR")

        # show current connector status
        server_box = layout.box()
        conn = BlenderServer.get_global_connector()
        if conn and conn.is_running():
            server_box.label(text="Blender: Running", icon="CHECKMARK")
        else:
            server_box.label(text="Blender: Running", icon="ERROR")