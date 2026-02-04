import bpy  # type: ignore
from ..constants import get_operator
from ..ConduitClient import register
from ..pipeline import send_command
from pathlib import Path
import json

class PIPELINE_OT_RegisterBlender(bpy.types.Operator):
    bl_idname = get_operator("register_blender")
    bl_description = "Registers Blender as Executable for Conduit"
    bl_label = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        path = bpy.app.binary_path
        version = bpy.app.version_string

        # get json data from roaming conduit folder
        json_path = Path.home() / "AppData" / "Roaming" / "Conduit" / "settings.json"
        with open(json_path, "r") as f:
            data = json.load(f)
        
        existing_blender_versions_dict = data.get("blender_versions", [])
        
        #print(existing_blender_versions_dict)
        for entry in existing_blender_versions_dict:
            if existing_blender_versions_dict[entry] == path:
                self.report({'INFO'}, f"This Blender executable is already registered as Version {version}")
                return {"CANCELLED"}


        existing_blender_versions_dict[version] = path
        data["blender_versions"] = existing_blender_versions_dict
        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)
        return {"FINISHED"}
