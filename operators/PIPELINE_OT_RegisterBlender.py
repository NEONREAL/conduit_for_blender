import bpy  # type: ignore
from ..constants import get_operator
from ..ConduitClient import register


class PIPELINE_OT_RegisterBlender(bpy.types.Operator):
    bl_idname = get_operator("register_blender")
    bl_description = "Registers Blender as Executable for Conduit"
    bl_label = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        register()
        return {"FINISHED"}
