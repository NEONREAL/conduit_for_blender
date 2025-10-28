import bpy  # type: ignore
from ..ConduitConnect import Connector
from ..constants import get_operator

# Define the operator to snap FK bones to IK bones
class FILE_OT_LinkTask(bpy.types.Operator):
    bl_idname = get_operator("operator")
    bl_description = "Renames selected Object to Hello World"
    bl_label = "Renames selected object to Hello World"
    bl_options = {"REGISTER", "UNDO"}

    string: bpy.props.StringProperty(name = "String") #type: ignore

    def execute(self, context):
        connector = Connector()
        connector.get_asset()
        return {"FINISHED"}
    
