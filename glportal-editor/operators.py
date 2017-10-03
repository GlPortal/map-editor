import bpy
import sys
from bpy.props import StringProperty, BoolProperty, EnumProperty

from .operatorsList import operatorList
from .operatorHelpers import resetTriggerSettings, simpleCube, setTrigger
from .managers import ModelManager


operators = []
idnamePrefix = "glp"


# we are using this for <end> (exit door)
class AddDoor(bpy.types.Operator):
  bl_idname = "glp.add_door"
  bl_label = "Add a door"
  bl_description = "Add an exit door (use only once)"
  bl_options = {'UNDO'}

  def execute(self, context):
    if ModelManager.create("Door.obj", "door/door"):
      object = bpy.context.selected_objects[0]

      if object:
        object.glpTypes = "door"

    return {'FINISHED'}


class SearchBase(bpy.types.Operator):
  bl_idname = "glp.search"
  bl_label = "Add search"
  bl_description = 'Base for search operator'
  bl_property = "items"
  bl_options = {'INTERNAL'}

  action = None
  kwargs = None
  items = EnumProperty(items=[("none", "none", "none")])

  def execute(self, context):
    if self.items and self.items != "none":
      if self.action:
        if isinstance(self.action, str):
          self.action = getattr(getattr(bpy.ops, idnamePrefix), self.action)

        if self.kwargs and isinstance(self.kwargs, dict):
          args = self.kwargs.copy()
          args[self.kwargs["items"]] = self.items
          del args["items"]

          self.action(**args)
        else:
          self.action(self.items)
        return {'FINISHED'}
    return {'CANCELLED'}

  def invoke(self, context, event):
    context.window_manager.invoke_search_popup(self)
    return {'FINISHED'}


class TriggerSetBase(bpy.types.Operator):
  """Base for trigger set operators"""
  bl_idname = 'gpl.trigger_set'
  bl_label = 'Trigger'
  bl_description = 'Base for set trigger operator'
  bl_options = {'INTERNAL'}

  type = StringProperty(default="")
  filePath = StringProperty(default="")
  loop = BoolProperty(default=False)

  def execute(self, context):
    objects = bpy.context.selected_objects

    if not (objects and self.type):
      return {'CANCELLED'}

    for object in objects:
      if object.type == 'MESH':
        if object.glpTypes not in {"door", "model"}:
          setTrigger(object, self.type, self.filePath, self.loop)
        else:
          self.report(
            {'ERROR'}, "Door and models can't be converted to the %s trigger." % (self.type)
          )
      else:
        self.report(
          {'ERROR'},
          "Object of type '%s' can't be converted to the %s trigger." % (object.type, self.type)
        )
    return {'FINISHED'}


class WallSetBase(bpy.types.Operator):
  """Base for wall set operators"""
  bl_idname = "glp.wall"
  bl_label = "Wall"
  bl_description = "Mark the selection as wall."
  bl_options = {'INTERNAL'}

  material = StringProperty(default="")

  def execute(self, context):
    objects = bpy.context.selected_objects

    if not (objects and self.material):
      return {'CANCELLED'}

    for object in objects:
      if object.type == 'MESH':
        if object.glpTypes != "door":
          if object.glpTypes != "model":
            resetTriggerSettings(object)
            object.glpTypes = "wall"

          object.glpMaterial = self.material
        else:
          self.report({'ERROR'}, "Door can't be converted to the wall.")
      else:
        self.report(
          {'ERROR'}, "Object of type '%s' can't be converted to the wall." % (object.type)
        )
    return {'FINISHED'}


class VolumeSetBase(bpy.types.Operator):
  """Base for volume set operators"""
  bl_idname = "glp.volume"
  bl_label = "Volume"
  bl_description = "Mark the selection as volume."
  bl_options = {'INTERNAL'}

  material = StringProperty(default="")
  volumeType = StringProperty(default="")

  def execute(self, context):
    objects = bpy.context.selected_objects

    if not (objects and self.material and self.volumeType):
      return {'CANCELLED'}

    for object in objects:
      if object.type == 'MESH':
        if object.glpTypes != "door":
          if object.glpTypes != "model":
            resetTriggerSettings(object)
            object.glpTypes = "volume"
            object.glpVolumeTypes = self.volumeType

          object.glpMaterial = self.material
        else:
          self.report({'ERROR'}, "Door can't be converted to the volume.")
      else:
        self.report(
          {'ERROR'}, "Object of type '%s' can't be converted to the volume." % (object.type)
        )
    return {'FINISHED'}


class AddBase(bpy.types.Operator):
  """Base for add operator"""
  bl_idname = 'gpl.add'
  bl_label = 'Add'
  bl_description = 'Base for add operator'
  bl_options = {'INTERNAL'}

  action = None
  kwargs = None

  def execute(self, context):
    if self.action:
      if isinstance(self.action, str):
        self.action = getattr(getattr(bpy.ops, idnamePrefix), self.action)

      if simpleCube():
        if self.kwargs:
          if isinstance(self.kwargs, dict):
            self.action(**self.kwargs)
          elif isinstance(self.kwargs, list):
            self.action(*self.kwargs)
        else:
          self.action()
        return {'FINISHED'}
    return {'CANCELLED'}


def addOperators():
  for opData in operatorList:
    if "action" in opData["properties"] and not isinstance(opData["properties"]["action"], str):
      opData["properties"]["action"] = staticmethod(opData["properties"]["action"])

    if "bl_idname" in opData["properties"] \
       and not opData["properties"]["bl_idname"].startswith(idnamePrefix):
      opData["properties"]["bl_idname"] = idnamePrefix + "." + opData["properties"]["bl_idname"]

    base = getattr(sys.modules[__name__], opData["base"])

    operator = type(
      opData["className"],
      (base, ),
      opData["properties"]
    )
    operators.append(operator)
    bpy.utils.register_class(operator)


def removeOperators():
  for operator in operators:
    bpy.utils.unregister_class(operator)

  del operators[:]
