import bpy  # type: ignore
from ..constants import get_operator
from ..pipeline import get_Asset_info
import os
from pathlib import Path

# Define the operator to snap FK bones to IK bones
class CONDUIT_OT_CreateTexture(bpy.types.Operator):
    bl_idname = get_operator("create_new_texture")
    bl_description = "Creates a new Texture"
    bl_label = "Creates a new Texture of selected size"
    bl_options = {"REGISTER", "UNDO"}
    
    #def invoke(self, context, event):
        #return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        self.conduit_properties = context.scene.conduit_texture_properties
        print(self.conduit_properties.TextureSizes)
        return{'FINISHED'}