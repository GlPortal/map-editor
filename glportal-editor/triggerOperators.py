import bpy
from bpy.props import StringProperty, BoolProperty

from .operatorHelpers import setTrigger, simpleCube


class SetMap(bpy.types.Operator):
  bl_idname = "glp.set_map"
  bl_label = "Map"
  bl_description = "Mark the selection as map trigger."
  bl_options = {'UNDO'}
  filePath = StringProperty(default="")

  def execute(self, context):
    objects = bpy.context.selected_objects
    for object in objects:
      if object.type == 'MESH':
        if object.glpTypes not in {"door", "model"}:
          setTrigger(object, "map", self.filePath)
        else:
          self.report({'ERROR'}, "Door and models can't be converted to the map trigger.")
      else:
        self.report(
          {'ERROR'},
          "Object of type '%s' can't be converted to the map trigger." % (object.type)
        )
    return {'FINISHED'}


class SetAudio(bpy.types.Operator):
  bl_idname = "glp.set_audio"
  bl_label = "Audio"
  bl_description = "Mark the selection as audio trigger."
  bl_options = {'UNDO'}
  filePath = StringProperty(default="")
  loop = BoolProperty(default=False)

  def execute(self, context):
    objects = bpy.context.selected_objects
    for object in objects:
      if object.type == 'MESH':
        if object.glpTypes not in {"door", "model"}:
          setTrigger(object, "audio", self.filePath, self.loop)
        else:
          self.report({'ERROR'}, "Door and models can't be converted to the audio trigger.")
      else:
        self.report(
          {'ERROR'},
          "Object of type '%s' can't be converted to the audio trigger." % (object.type)
        )
    return {'FINISHED'}


class SetWin(bpy.types.Operator):
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
        self.report(
          {'ERROR'},
          "Object of type '%s' can't be converted to the win trigger." % (object.type)
        )
    return {'FINISHED'}


class AddWin(bpy.types.Operator):
  bl_idname = "glp.add_win"
  bl_label = "Win"
  bl_description = "Add a win trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    if simpleCube():
      bpy.ops.glp.set_win()
    return {'FINISHED'}


class SetDeath(bpy.types.Operator):
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
        self.report(
          {'ERROR'},
          "Object of type '%s' can't be converted to the death trigger." % (object.type)
        )
    return {'FINISHED'}


class AddDeath(bpy.types.Operator):
  bl_idname = "glp.add_death"
  bl_label = "Death"
  bl_description = "Add a death trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    if simpleCube():
      bpy.ops.glp.set_death()
    return {'FINISHED'}


class SetRadiation(bpy.types.Operator):
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
        self.report(
          {'ERROR'},
          "Object of type '%s' can't be converted to the radiation trigger." % (object.type)
        )
    return {'FINISHED'}


class AddRadiation(bpy.types.Operator):
  bl_idname = "glp.add_radiation"
  bl_label = "Radiation"
  bl_description = "Add a radiation trigger."
  bl_options = {'UNDO'}

  def execute(self, context):
    if simpleCube():
      bpy.ops.glp.set_radiation()
    return {'FINISHED'}
