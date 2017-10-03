import bpy
import os
import subprocess
import sys
import unittest

import toGlPortalXml


class OperatorsTest(unittest.TestCase):
  operatorsAdd = [
    {
      "action": bpy.ops.glp.trigger_add_win,
      "type": "trigger",
      "trigger": "win"
    },
    {
      "action": bpy.ops.glp.trigger_add_death,
      "type": "trigger",
      "trigger": "death"
    },
    {
      "action": bpy.ops.glp.trigger_add_radiation,
      "type": "trigger",
      "trigger": "radiation"
    },
    {
      "action": bpy.ops.glp.wall_add_metal,
      "type": "wall",
      "material": "metal/tiles00x3"
    },
    {
      "action": bpy.ops.glp.wall_add_portalable,
      "type": "wall",
      "material": "concrete/wall00"
    },
    {
      "action": bpy.ops.glp.volume_add_acid,
      "type": "volume",
      "volume": "acid"
    }
  ]
  operatorsSet = [
    {
      "action": bpy.ops.glp.trigger_set_audio,
      "type": "trigger",
      "trigger": "audio"
    },
    {
      "action": bpy.ops.glp.trigger_set_map,
      "type": "trigger",
      "trigger": "map"
    },
    {
      "action": bpy.ops.glp.trigger_set_win,
      "type": "trigger",
      "trigger": "win"
    },
    {
      "action": bpy.ops.glp.trigger_set_death,
      "type": "trigger",
      "trigger": "death"
    },
    {
      "action": bpy.ops.glp.trigger_set_radiation,
      "type": "trigger",
      "trigger": "radiation"
    },
    {
      "action": bpy.ops.glp.wall_set_metal,
      "type": "wall",
      "material": "metal/tiles00x3"
    },
    {
      "action": bpy.ops.glp.wall_set_portalable,
      "type": "wall",
      "material": "concrete/wall00"
    },
    {
      "action": bpy.ops.glp.volume_set_acid,
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
    self.assertEqual(obj.glpTypes, operator["type"], "Object type is not correct.\n")

    if (operator["type"] == "trigger"):
      self.assertEqual(obj.glpTriggerTypes, operator["trigger"], "Trigger type is not correct.\n")
    elif (operator["type"] == "volume"):
      self.assertEqual(obj.glpVolumeTypes, operator["volume"], "Volume type is not correct.\n")
    elif (operator["type"] == "wall"):
      self.assertEqual(obj.glpMaterial, operator["material"], "Material is not correct.\n")

  def testDynamicOperators(self):
    for operator in self.operatorsAdd:
      operator["action"]()
      self.checkObject(operator)

    self.clearScene()

    toGlPortalXml.operatorHelpers.simpleCube()
    for operator in self.operatorsSet:
      operator["action"]()
      self.checkObject(operator)

  def testDynamicOperatorsRegistered(self):
    """ Test if operators are registered """
    for operator in toGlPortalXml.operators.operatorList:
      print("Checking:", operator["properties"]["bl_idname"])
      self.assertTrue(
        hasattr(bpy.types, "GLP_OT_" + operator["properties"]["bl_idname"].lstrip("glp.")),
        "Operator 'bpy.ops." + operator["properties"]["bl_idname"] + "' does not exist"
      )


if __name__ == '__main__':
  unittest.main(
    argv=[sys.argv[0]]
  )
