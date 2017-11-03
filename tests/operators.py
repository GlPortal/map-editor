import bpy
import os
import subprocess
import sys
import unittest

try:
  import RadixMapEditor
except ImportError:
  import toGlPortalXml as RadixMapEditor


class OperatorsTest(unittest.TestCase):
  operatorsAdd = [
    {
      "action": bpy.ops.radix.trigger_add_win,
      "type": "trigger",
      "trigger": "win"
    },
    {
      "action": bpy.ops.radix.trigger_add_death,
      "type": "trigger",
      "trigger": "death"
    },
    {
      "action": bpy.ops.radix.trigger_add_radiation,
      "type": "trigger",
      "trigger": "radiation"
    },
    {
      "action": bpy.ops.radix.wall_add_metal,
      "type": "wall",
      "material": "metal/tiles00x3"
    },
    {
      "action": bpy.ops.radix.wall_add_portalable,
      "type": "wall",
      "material": "concrete/wall00"
    },
    {
      "action": bpy.ops.radix.volume_add_acid,
      "type": "volume",
      "volume": "acid"
    }
  ]
  operatorsSet = [
    {
      "action": bpy.ops.radix.trigger_set_audio,
      "type": "trigger",
      "trigger": "audio"
    },
    {
      "action": bpy.ops.radix.trigger_set_map,
      "type": "trigger",
      "trigger": "map"
    },
    {
      "action": bpy.ops.radix.trigger_set_win,
      "type": "trigger",
      "trigger": "win"
    },
    {
      "action": bpy.ops.radix.trigger_set_death,
      "type": "trigger",
      "trigger": "death"
    },
    {
      "action": bpy.ops.radix.trigger_set_radiation,
      "type": "trigger",
      "trigger": "radiation"
    },
    {
      "action": bpy.ops.radix.wall_set_metal,
      "type": "wall",
      "material": "metal/tiles00x3"
    },
    {
      "action": bpy.ops.radix.wall_set_portalable,
      "type": "wall",
      "material": "concrete/wall00"
    },
    {
      "action": bpy.ops.radix.volume_set_acid,
      "type": "volume",
      "volume": "acid"
    }
  ]

  def setUp(self):
    print(self.id())

  def clearScene(self):
    """Clear current scene"""
    scene = bpy.context.scene

    for ob in scene.objects:
      ob.select = True
      bpy.ops.object.delete()

  def checkObject(self, operator):
    objects = bpy.context.selected_objects
    self.assertEqual(len(objects), 1, "More than 1 object is selected.\n")

    obj = objects[0]
    self.assertEqual(obj.radixTypes, operator["type"], "Object type is not correct.\n")

    if (operator["type"] == "trigger"):
      self.assertEqual(obj.radixTriggerTypes, operator["trigger"], "Trigger type is not correct.\n")
    elif (operator["type"] == "volume"):
      self.assertEqual(obj.radixVolumeTypes, operator["volume"], "Volume type is not correct.\n")
    elif (operator["type"] == "wall"):
      self.assertEqual(obj.radixMaterial, operator["material"], "Material is not correct.\n")

  def testDynamicOperators(self):
    for operator in self.operatorsAdd:
      operator["action"]()
      self.checkObject(operator)

    self.clearScene()

    RadixMapEditor.operatorHelpers.simpleCube()
    for operator in self.operatorsSet:
      operator["action"]()
      self.checkObject(operator)

  def testDynamicOperatorsRegistered(self):
    """ Test if operators are registered """
    for operator in RadixMapEditor.operators.operatorList:
      print("Checking:", operator["properties"]["bl_idname"])
      self.assertTrue(
        hasattr(bpy.types, "RADIX_OT_" + operator["properties"]["bl_idname"].lstrip("radix.")),
        "Operator 'bpy.ops." + operator["properties"]["bl_idname"] + "' does not exist"
      )


if __name__ == '__main__':
  unittest.main(
    argv=[sys.argv[0]]
  )
