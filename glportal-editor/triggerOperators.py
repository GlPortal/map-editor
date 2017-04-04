import bpy

from .operatorHelpers import setTrigger, simpleCube

class setMap(bpy.types.Operator):
  bl_idname = "glp.set_map"
  bl_label = "Map"
  bl_description = "Mark the selection as map trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    objects = bpy.context.selected_objects
    for object in objects:
      if object.type == 'MESH':
        if object.glpTypes not in {"door", "model"}:
          setTrigger(object, "map")
        else:
          self.report({'ERROR'}, "Door and models can't be converted to the map trigger.")
      else:
        self.report({'ERROR'}, "Object of type '%s' can't be converted to the map trigger." % (object.type))
    return {'FINISHED'}

class setAudio(bpy.types.Operator):
  bl_idname = "glp.set_audio"
  bl_label = "Audio"
  bl_description = "Mark the selection as audio trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    objects = bpy.context.selected_objects
    for object in objects:
      if object.type == 'MESH':
        if object.glpTypes not in {"door", "model"}:
          setTrigger(object, "audio")
        else:
          self.report({'ERROR'}, "Door and models can't be converted to the audio trigger.")
      else:
        self.report({'ERROR'}, "Object of type '%s' can't be converted to the audio trigger." % (object.type))
    return {'FINISHED'}

class setWin(bpy.types.Operator):
  bl_idname = "glp.set_win"
  bl_label = "Win"
  bl_description = "Mark the selection as win trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    objects = bpy.context.selected_objects
    for object in objects:
      if object.type == 'MESH':
        if object.glpTypes not in {"door", "model"}:
          setTrigger(object, "win")
        else:
          self.report({'ERROR'}, "Door and models can't be converted to the win trigger.")
      else:
        self.report({'ERROR'}, "Object of type '%s' can't be converted to the win trigger." % (object.type))
    return {'FINISHED'}

class addWin(bpy.types.Operator):
  bl_idname = "glp.add_win"
  bl_label = "Win"
  bl_description = "Add a win trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    if simpleCube():
      bpy.ops.glp.set_win()
    return {'FINISHED'}

class setDeath(bpy.types.Operator):
  bl_idname = "glp.set_death"
  bl_label = "Death"
  bl_description = "Mark the selection as death trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    objects = bpy.context.selected_objects
    for object in objects:
      if object.type == 'MESH':
        if object.glpTypes not in {"door", "model"}:
          setTrigger(object, "death")
        else:
          self.report({'ERROR'}, "Door and models can't be converted to the death trigger.")
      else:
        self.report({'ERROR'}, "Object of type '%s' can't be converted to the death trigger." % (object.type))
    return {'FINISHED'}

class addDeath(bpy.types.Operator):
  bl_idname = "glp.add_death"
  bl_label = "Death"
  bl_description = "Add a death trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    if simpleCube():
      bpy.ops.glp.set_death()
    return {'FINISHED'}

class setRadiation(bpy.types.Operator):
  bl_idname = "glp.set_radiation"
  bl_label = "Radiation"
  bl_description = "Mark the selection as radiation trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    objects = bpy.context.selected_objects
    for object in objects:
      if object.type == 'MESH':
        if object.glpTypes not in {"door", "model"}:
          setTrigger(object, "radiation")
        else:
          self.report({'ERROR'}, "Door and models can't be converted to the radiation trigger.")
      else:
        self.report({'ERROR'}, "Object of type '%s' can't be converted to the radiation trigger." % (object.type))
    return {'FINISHED'}

class addRadiation(bpy.types.Operator):
  bl_idname = "glp.add_radiation"
  bl_label = "Radiation"
  bl_description = "Add a radiation trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    if simpleCube():
      bpy.ops.glp.set_radiation()
    return {'FINISHED'}
