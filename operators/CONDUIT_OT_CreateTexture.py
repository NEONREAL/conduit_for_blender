import bpy  # type: ignore
from ..constants import get_operator
from ..pipeline import get_expected_filename, add_texture_to_shader, get_latest_version, update_task_list
import os
from pathlib import Path

# Define the operator to snap FK bones to IK bones
class CONDUIT_OT_CreateTexture(bpy.types.Operator):
    bl_idname = get_operator("create_new_texture")
    bl_description = "Creates a new Texture"
    bl_label = "Creates a new Texture of selected size"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # getting image properties
        self.conduit_properties = context.scene.conduit_texture_properties
        resolution = int(self.conduit_properties.TextureSizes)
        _, asset_name = get_expected_filename(Path(bpy.data.filepath))
        
        # adding image to properties
        task_name = Path(self.conduit_properties.Tasks).name
        task_path = Path(self.conduit_properties.Tasks)
        name = f"{asset_name}_{task_name}"

        # creating image
        images = bpy.data.images
        image = None
        if name in images:
            image = images[name]
            
            # get next version path
            _, path = get_latest_version(task = task_path, next_version=True)

            # save copy to new version
            print(f"saving texture as {path}")
            image.save(filepath = str(path), save_copy = True)

            # load new version
            image.filepath_raw = str(path)

            # (add to shader)
            return {'CANCELLED'}
        else:
            bpy.ops.image.new(
                name = name,
                width = resolution,
                height = resolution,
            )

            image = bpy.data.images[name]
            version = get_latest_version(task_path)
            image.save(filepath = str(task_path / f"{name}_{version}.png")),
        add_texture_to_shader(image, context.object.active_material)
        update_task_list(context)
        context.area.tag_redraw()

        return {'FINISHED'}