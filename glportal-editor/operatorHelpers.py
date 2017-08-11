import bpy

from .managers import MapManager, MaterialManager, ModelManager
from . import types


def resetTriggerSettings(object):
  if object.glpTypes == "trigger":
    object.glpTriggerTypes = "none"
    object.draw_type = 'TEXTURED'
    object.show_x_ray = False
    object.show_bounds = False
    object.draw_bounds_type = 'BOX'
    object.glpTriggerFilepath = 'none'
    object.glpTriggerAudioLoop = False


def setTrigger(object, type, filePath='', loop=False):
  prefs = bpy.context.user_preferences.addons[__package__].preferences
  clearGlpProperties(object)

  object.glpTypes = "trigger"
  object.glpTriggerTypes = type
  object.draw_type = 'WIRE'
  object.show_x_ray = prefs.triggerXrays
  object.show_bounds = True
  object.draw_bounds_type = 'CAPSULE'
  object.glpTriggerAudioLoop = loop

  if filePath:
    object.glpTriggerFilepath = filePath


def clearGlpProperties(object):
  MaterialManager.reset(object)

  if object.glpTypes != "none":
    object.glpTypes = "none"
  if object.glpVolumeTypes != "none":
    object.glpVolumeTypes = "none"
  if object.glpTriggerTypes != "none":
    object.glpTriggerTypes = "none"
  if object.glpTriggerFilepath != "none":
    object.glpTriggerFilepath = "none"
  if object.glpTriggerAudioLoop:
    object.glpTriggerAudioLoop = False


def itemsMaterial(self, context):
  return [(name, fancyName, tooltip) for name, fancyName, tooltip in types.GLP_MATERIAL_TYPES]


def itemsModel(self, centext):
  return [(file, fancyName, fancyName) for file, fancyName in ModelManager.MODELS.items()]


def itemsMap(self, centext):
  return [(key, name, name) for key, name in MapManager.MAPS.items()]


def simpleCube():
  if ModelManager.create("Cube.obj"):
    object = bpy.context.selected_objects[0]
    object.glpTypes = "none"
    object.dimensions = [2.0, 2.0, 2.0]
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return True
  return False
