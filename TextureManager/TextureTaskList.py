import bpy #type: ignore

class UI_UL_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        display_name = item.name[:-4]
        layout.label(text = display_name)
        layout.label(text = item.version)

class TaskListItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty() #type: ignore
    version: bpy.props.StringProperty() #type: ignore
    path: bpy.props.StringProperty() #type: ignore

class TaskProperties(bpy.types.PropertyGroup):
    Task_Items: bpy.props.CollectionProperty(type=TaskListItem)#type: ignore
    Task_Index: bpy.props.IntProperty()#type: ignore
