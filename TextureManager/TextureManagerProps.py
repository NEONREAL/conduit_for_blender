import bpy
from ..pipeline import update_task_list
class TaskItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty() #type: ignore
    path: bpy.props.StringProperty() #type: ignore

class CONDUIT_TexturePG(bpy.types.PropertyGroup):
    
    task_items: bpy.props.CollectionProperty(type=TaskItem) #type: ignore

    def get_task_items(self, context):
        return [(item.path, item.name, "") for item in self.task_items]

    Tasks: bpy.props.EnumProperty(
        name="tasks",
        items=get_task_items,
        update = lambda self, context: update_task_list(context)
    )#type: ignore

    TextureSizes: bpy.props.EnumProperty(
        name = "sizes",
        items = [
            ("512", "512", ""),
            ("1024", "1K", ""),
            ("2048", "2K", ""),
            ("4096", "4K", ""),
        ]
        )#type: ignore
