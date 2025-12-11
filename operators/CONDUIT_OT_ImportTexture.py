import bpy  # type: ignore
from ..constants import get_operator
from ..pipeline import add_texture_to_shader
import os
from pathlib import Path

# Define the operator to snap FK bones to IK bones
class CONDUIT_OT_ImportTexture(bpy.types.Operator):
    bl_idname = get_operator("import_texture")
    bl_description = "Creates a new Texture"
    bl_label = "Creates a new Texture of selected size"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.TaskProperties
        if props.Task_Items and 0 <= props.Task_Index < len(props.Task_Items):
            selected_item = props.Task_Items[props.Task_Index]
            path = selected_item.path
        else:
            selected_item = None
            self.report({'ERROR'}, "No texture task selected.")
            return{'CANCELLED'}
        
        material = context.object.active_material
        if not material:
            self.report({'ERROR'}, "No active material on the selected object.")
            return{'CANCELLED'}
        
        # getting name
        stem = Path(path).stem
        name = stem[:-4]
        
        # loading image
        if name in bpy.data.images:
            image = bpy.data.images[name]
        else:
            image = bpy.data.images.load(path)
        image.name = name
        image.filepath_raw = path
        image.reload()
        
        material = context.object.active_material
        add_texture_to_shader(image, material)
        # import texture

        return{'FINISHED'}