import bpy  # type: ignore
from ..constants import get_operator
from ..pipeline import get_expected_filename
from pathlib import Path
import os
from ..ConduitClient import log


# Define the operator to snap FK bones to IK bones
class CONDUIT_OT_SaveMasterVersion(bpy.types.Operator):
    bl_idname = get_operator("save_to_master")
    bl_description = "Pushes Current version to Master"
    bl_label = "Pushes Current version to Master"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        blend_path = Path(bpy.data.filepath)
        directory = os.path.dirname(bpy.data.filepath)
        filename = f"_master_{get_expected_filename(blend_path)}.blend"
        filepath = os.path.join(directory, filename)

        # renaming the collection for masterfile
        collection = bpy.data.collections["EXPORT"]
        collection.name = get_expected_filename(blend_path)

        # store master file
        bpy.ops.wm.save_as_mainfile(filepath=filepath, copy=True)

        collection = bpy.data.collections[get_expected_filename(blend_path)]
        collection.name = "EXPORT"

        # refresh version list
        log(f"saved {filename} as master file!")

        return {"FINISHED"}

