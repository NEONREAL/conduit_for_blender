import bpy  # type: ignore
from ..constants import get_operator
from pathlib import Path

# Define the operator to snap FK bones to IK bones
class CONDUIT_OT_SaveNewVersion(bpy.types.Operator):
    bl_idname = get_operator("save_new_version")
    bl_description = "Saves a new version of File"
    bl_label = "Saves a new version of File"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
         
        return {"FINISHED"}
    

