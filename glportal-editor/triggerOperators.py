import bpy

from .operatorHelpers import setTrigger

class setWin(bpy.types.Operator):
  bl_idname = "glp.set_win"
  bl_label = "Win"
  bl_description = "Mark the selection as win trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    object = bpy.context.active_object
    if object:
      if object.type == 'MESH':
        if object.glpTypes != "door":
          setTrigger(object, "win")
        else:
          self.report({'ERROR'}, "Door can't be converted to the win trigger.")
      else:
        self.report({'ERROR'}, "Object of type '%s' can't be converted to the win trigger." % (object.type))
    return {'FINISHED'}

class addWin(bpy.types.Operator):
  bl_idname = "glp.add_win"
  bl_label = "Win"
  bl_description = "Add a win trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    bpy.ops.mesh.primitive_cube_add()
    bpy.ops.glp.set_win()
    return {'FINISHED'}

class setDeath(bpy.types.Operator):
  bl_idname = "glp.set_death"
  bl_label = "Death"
  bl_description = "Mark the selection as death trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    object = bpy.context.active_object
    if object:
      if object.type == 'MESH':
        if object.glpTypes != "door":
          setTrigger(object, "death")
        else:
          self.report({'ERROR'}, "Door can't be converted to the death trigger.")
      else:
        self.report({'ERROR'}, "Object of type '%s' can't be converted to the death trigger." % (object.type))
    return {'FINISHED'}

class addDeath(bpy.types.Operator):
  bl_idname = "glp.add_death"
  bl_label = "Death"
  bl_description = "Add a death trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    bpy.ops.mesh.primitive_cube_add()
    bpy.ops.glp.set_death()
    return {'FINISHED'}

class setRadiation(bpy.types.Operator):
  bl_idname = "glp.set_radiation"
  bl_label = "Radiation"
  bl_description = "Mark the selection as radiation trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    object = bpy.context.active_object
    if object:
      if object.type == 'MESH':
        if object.glpTypes != "door":
          setTrigger(object, "radiation")
        else:
          self.report({'ERROR'}, "Door can't be converted to the radiation trigger.")
      else:
        self.report({'ERROR'}, "Object of type '%s' can't be converted to the radiation trigger." % (object.type))
    return {'FINISHED'}

class addRadiation(bpy.types.Operator):
  bl_idname = "glp.add_radiation"
  bl_label = "Radiation"
  bl_description = "Add a radiation trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    bpy.ops.mesh.primitive_cube_add()
    bpy.ops.glp.add_radiation()
    return {'FINISHED'}
