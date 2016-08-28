import bpy
import os

from .updateTextures import updateTexture
from .managers import MaterialManager, ModelManager

def updateTriggerXrays(self, context):
  prefs = context.user_preferences.addons[__package__].preferences
  triggerXrays = prefs.triggerXrays
  objects = context.scene.objects

  for object in objects:
    if object.glpTypes == "trigger":
      object.show_x_ray = prefs.triggerXrays

def updateSmartTexturesMapping(self, context):
  prefs = context.user_preferences.addons[__package__].preferences
  SmartTextures = prefs.smartTexturesMapping
  objects = context.scene.objects

  for object in objects:
    if object.glpTypes in {"wall", "volume"}:
      me = object.data

      if SmartTextures:
        me.materials[0].texture_slots[0].texture_coords = 'UV'
        me.materials[0].texture_slots[0].mapping = 'FLAT'

        updateTexture(object)
      else:
        me.materials[0].texture_slots[0].texture_coords = 'GLOBAL'
        me.materials[0].texture_slots[0].mapping = 'CUBE'

def updateDefaultMaterial(self, context):
  prefs = context.user_preferences.addons[__package__].preferences

  if prefs.materials != "none":
    prefs.defaultMaterial = prefs.materials

def updateDataDir(self, context):
  prefs = context.user_preferences.addons[__package__].preferences

  if os.path.isdir(os.path.expanduser(prefs.dataDir)):
    MaterialManager.reload()
    ModelManager.reload()
