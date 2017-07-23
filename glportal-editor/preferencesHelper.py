import bpy
import os

from .managers import MaterialManager, ModelManager
from . import MaterialPanel

def updateTriggerXrays(self, context):
  prefs = context.user_preferences.addons[__package__].preferences
  triggerXrays = prefs.triggerXrays
  objects = context.scene.objects

  for object in objects:
    if object.glpTypes == "trigger":
      object.show_x_ray = prefs.triggerXrays

def updateDefaultMaterial(self, context):
  prefs = context.user_preferences.addons[__package__].preferences

  if prefs.materials != "none":
    prefs.defaultMaterial = prefs.materials

def updateDataDir(self, context):
  prefs = context.user_preferences.addons[__package__].preferences

  if os.path.isdir(os.path.expanduser(prefs.dataDir)):
    MaterialManager.reload()
    ModelManager.reload()
    MaterialPanel.initRows()
