import bpy  # type: ignore
from ..constants import AddonProperties
from ..constants import get_operator
from ..pipeline import get_version_from_filename, is_conduit_file
from pathlib import Path

class VIEW3D_PT_UI_AssetManager(bpy.types.Panel):
    bl_label = "Asset Manager"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = AddonProperties.panel_category
    
    def draw(self, context):
        layout = self.layout

        # save new version
        box = layout.box()
        box.label(text="Version Control")
        col = box.column()
        col.enabled = is_conduit_file()
        col.operator(get_operator("save_to_master"), text = "Publish", icon = 'EXPORT')
        col.operator(get_operator("save_new_version"), text = "New Version", icon = 'ADD')
        row = box.row()
        row.enabled = False
        row.label(text=f"current Version: {get_version_from_filename(Path(bpy.data.filepath).name)}")


        