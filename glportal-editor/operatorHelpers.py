import bpy

from .managers import MaterialManager, ModelManager
from . import types

def resetTriggerSettings(object):
  if object.glpTypes and object.glpTypes == "trigger":
    object.glpTriggerTypes = "none"
    object.draw_type = 'TEXTURED'
    object.show_x_ray = False
    object.show_bounds = False
    object.draw_bounds_type = 'BOX'

def setTrigger(object, type):
  prefs = bpy.context.user_preferences.addons[__package__].preferences
  clearGlpProperties(object)

  object.glpTypes = "trigger"
  object.glpTriggerTypes = type
  object.draw_type = 'WIRE'
  object.show_x_ray = prefs.triggerXrays
  object.show_bounds = True
  object.draw_bounds_type = 'CAPSULE'

def clearGlpProperties(object):
  MaterialManager.reset(object)

  if object.glpTypes != "none":
    object.glpTypes = "none"
  if object.glpVolumeTypes != "none":
    object.glpVolumeTypes = "none"
  if object.glpTriggerTypes != "none":
    object.glpTriggerTypes = "none"

def itemsMaterial(self, context):
  return [(name, fancyName, tooltip) for name, fancyName, tooltip in types.glpMaterialTypes]

def itemsModel(self, centext):
  return [(file, fancyName, fancyName) for file, fancyName in ModelManager.models.items()]
