import bpy
from ..pipeline import get_tasks

class CONDUIT_TexturePG(bpy.types.PropertyGroup):
    
    Tasks: bpy.props.EnumProperty(
        name = "tasks",
        items = []
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
    