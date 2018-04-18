import bpy
import sys
from bpy.props import StringProperty, BoolProperty, EnumProperty

from .operatorsList import operatorList
from .operatorHelpers import resetTriggerSettings, simpleCube, setTrigger
from .managers import ModelManager
from .SearchOperator import SearchOperator
from .AddOperator import AddOperator
from .TriggerSetOperator import TriggerSetOperator

operators = []
idnamePrefix = "radix"

class WallSetBase(bpy.types.Operator):
  """Base for wall set operators"""
  bl_idname = "radix.wall"
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
        if object.radixTypes != "model":
          resetTriggerSettings(object)
          object.radixTypes = "wall"

        object.radixMaterial = self.material
      else:
        self.report(
          {'ERROR'}, "Object of type '%s' can't be converted to the wall." % (object.type)
        )
    return {'FINISHED'}


class VolumeSetBase(bpy.types.Operator):
  """Base for volume set operators"""
  bl_idname = "radix.volume"
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
        if object.radixTypes != "model":
          resetTriggerSettings(object)
          object.radixTypes = "volume"
          object.radixVolumeTypes = self.volumeType

        object.radixMaterial = self.material
      else:
        self.report(
          {'ERROR'}, "Object of type '%s' can't be converted to the volume." % (object.type)
        )
    return {'FINISHED'}

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
  global operators

  for operator in operators:
    bpy.utils.unregister_class(operator)

  del operators[:]
