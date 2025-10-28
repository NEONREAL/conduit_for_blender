import bpy  # type: ignore
from ..constants import get_operator
from pathlib import Path
import os

# Define the operator to snap FK bones to IK bones
class CONDUIT_OT_SaveMasterVersion(bpy.types.Operator):
    bl_idname = get_operator("save_to_master")
    bl_description = "Pushes Current version to Master"
    bl_label = "Pushes Current version to Master"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        blend_path = Path(bpy.data.filepath)
        directory = os.path.dirname(bpy.data.filepath)
        filename = f"_master_{blend_path.name}"
        filepath = os.path.join(directory, filename)

        #store master file
        bpy.ops.wm.save_as_mainfile(filepath=filepath, copy = True)

        #refresh version list
        return{'FINISHED'}