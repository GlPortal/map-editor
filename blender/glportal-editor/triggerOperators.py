import bpy
import os
import string
import re

from .operatorHelpers import *

class setWin(bpy.types.Operator):
    bl_idname = "wm.set_win"
    bl_label = "Mark as win trigger."
    bl_description = "Mark the selection as win trigger. (Not implemented)"
    bl_options = {"UNDO"}
    
    def execute(self, context):
        object = bpy.context.active_object
        if object:
            if object.type == "MESH":
                setTrigger(object, "win")
            else:
                self.report({'ERROR'}, "Object of type '%s' can't be converted to the win trigger." % (object.type))
        return {'FINISHED'}

class addWin(bpy.types.Operator):
    bl_idname = "wm.add_win"
    bl_label = "Add win trigger"
    bl_description = "Add a win trigger. (Not implemented)"
    bl_options = {"UNDO"}
    
    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        setWin.execute(self, context)
        return {'FINISHED'}

class setDeath(bpy.types.Operator):
    bl_idname = "wm.set_death"
    bl_label = "Mark as death trigger"
    bl_description = "Mark the selection as death trigger."
    bl_options = {"UNDO"}
    
    def execute(self, context):
        object = bpy.context.active_object
        if object:
            if object.type == "MESH":
                setTrigger(object, "death")
            else:
                self.report({'ERROR'}, "Object of type '%s' can't be converted to the death trigger." % (object.type))
        return {'FINISHED'}

class addDeath(bpy.types.Operator):
    bl_idname = "wm.add_death"
    bl_label = "Add a death trigger"
    bl_description = "Add a death trigger."
    bl_options = {"UNDO"}
    
    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        setDeath.execute(self, context)
        return {'FINISHED'}

class setRadiation(bpy.types.Operator):
    bl_idname = "wm.set_radiation"
    bl_label = "Mark as radiation trigger"
    bl_description = "Mark the selection as radiation trigger."
    bl_options = {"UNDO"}
    
    def execute(self, context):
        object = bpy.context.active_object
        if object:
            if object.type == "MESH":
                setTrigger(object, "radiation")
            else:
                self.report({'ERROR'}, "Object of type '%s' can't be converted to the radiation trigger." % (object.type))
        return {'FINISHED'}

class addRadiation(bpy.types.Operator):
    bl_idname = "wm.add_radiation"
    bl_label = "Add a radiation trigger"
    bl_description = "Add a radiation trigger."
    bl_options = {"UNDO"}
    
    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        setRadiation.execute(self, context)
        return {'FINISHED'}
