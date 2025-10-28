import bpy  # type: ignore
from ..constants import get_operator
from ..pipeline import get_expected_filename, get_version_from_filename, create_json_info
import os
from pathlib import Path

# Define the operator to snap FK bones to IK bones
class CONDUIT_OT_SaveNewVersion(bpy.types.Operator):
    bl_idname = get_operator("save_new_version")
    bl_description = "Saves a new version of File"
    bl_label = "Saves a new version of File"
    bl_options = {"REGISTER", "UNDO"}

    comment: bpy.props.StringProperty()#type: ignore
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        blend_path = Path(bpy.data.filepath)
        directory = os.path.dirname(bpy.data.filepath)
        version = get_version_from_filename(Path(bpy.data.filepath).name, True, True)
        print(version)
        if not version:
            return {'CANCELLED'}
        filename = f"{get_expected_filename(blend_path)}_{version}.blend"
        filepath = os.path.join(directory, filename)

        #store master file
        bpy.ops.wm.save_as_mainfile(filepath=filepath)
        create_json_info(comment=self.comment)

        #refresh version list
        return{'FINISHED'}