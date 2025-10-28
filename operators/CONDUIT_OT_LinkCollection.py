import bpy  # type: ignore
from ..constants import get_operator
from pathlib import Path
import os
from ..pipeline import get_version_from_filename, get_expected_filename

# Define the operator to snap FK bones to IK bones
class CONDUIT_OT_LinkCollection(bpy.types.Operator):
    bl_idname = get_operator("link")
    bl_description = "Renames selected Object to Hello World"
    bl_label = "Renames selected object to Hello World"
    bl_options = {"REGISTER", "UNDO"}

    path_argument: bpy.props.StringProperty(subtype='FILE_PATH')#type: ignore

    def execute(self, context):
        print(self.path_argument)
        if not self.validate_path():
            return {"CANCELLED"}
        
        file = self.get_master_file(self.path_argument)
        if file:
            print("file")
        

        print(file)


        
        
        return {"FINISHED"}
    
    def validate_path(self) -> Path:
        try: 
            self.path = Path(self.path_argument)

        except Exception as e:
            self.report({"ERROR"}, f"Invalid path: {str(e)}")
            return False
            
        if self.path:
            return True


    def get_master_file(self, directory: Path) -> Path | None:
        for file in directory.iterdir():
            if file.name.startswith("_master"):
                return file
        return None
    
    def import_collection(self, filepath):
        collection_name = "EXPORT"

        # Load the linked collection
        with bpy.data.libraries.load(filepath, link=True, relative=True, create_liboverrides=False) as (data_from, data_to):
            if collection_name in data_from.collections:
                data_to.collections = [collection_name]
            else:
                self.report({'WARNING'}, f"Collection '{collection_name}' not found in {filepath}")
                return
        return
    
