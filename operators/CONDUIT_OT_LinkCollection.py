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

    path: bpy.props.StringProperty(subtype='FILE_PATH')#type: ignore

    def execute(self, context):
        if not self.validate_path():
            return {"CANCELLED"}
        
        file = self.get_master_file(self.path)
        if file:
            self.import_collection(file)
        return {"FINISHED"}
    
    def validate_path(self) -> Path | None:
        try: 
            path = Path(self.path)

        except Exception as e:
            self.report({"ERROR"}, f"Invalid path: {str(e)}")
            return None
            
        if self.path:
            return path


    def get_master_file(self, directory: Path) -> Path | None:
        if isinstance(directory, Path):
            pass
        else:
            directory = Path(directory)

        for file in directory.iterdir():
            if file.name.startswith("_master"):
                return file
        return None
    
    def import_collection(self, filepath):

        collection_name = get_expected_filename(Path(filepath))

        if not Path(filepath).exists() or not filepath.name.endswith(".blend"):
            self.report({'ERROR'}, f"Invalid or missing blend file: {filepath}")
            return

        with bpy.data.libraries.load(str(filepath), link=True, relative=True) as (data_from, data_to):
            if collection_name in data_from.collections:
                data_to.collections = [collection_name]
            else:
                self.report({'WARNING'}, f"Collection '{collection_name}' not found in {filepath}")
                return

        linked_col = data_to.collections[0]

        # Create an instance object for the collection
        inst = bpy.data.objects.new(linked_col.name + "_inst", None)
        inst.instance_type = 'COLLECTION'
        inst.instance_collection = linked_col

        linked_col.override_hierarchy_create(
            bpy.context.scene,
            bpy.context.view_layer,
            do_fully_editable = True
        )       
        return
    
