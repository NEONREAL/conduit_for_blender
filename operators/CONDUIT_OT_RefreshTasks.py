import bpy  # type: ignore
from ..constants import get_operator
from ..pipeline import update_task_list, get_tasks
import os
from pathlib import Path

# Define the operator to snap FK bones to IK bones
class CONDUIT_OT_RefreshTasks(bpy.types.Operator):
    bl_idname = get_operator("refresh_tasks")
    bl_label = "Refresh Tasks"

    def execute(self, context):

        update_task_list(context)

        context.area.tag_redraw()
        return {'FINISHED'}
