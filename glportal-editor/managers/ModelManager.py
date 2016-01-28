import bpy
import os
import string

models = {}
blacklist = [
  "GUIElement.obj",
  "Plane.obj",
  "Portal.obj",
  "PortalStencil.obj"
]

def preload():
  prefs = bpy.context.user_preferences.addons[__package__.rpartition('.')[0]].preferences
  path = prefs.dataDir + 'meshes'

  if os.path.isdir(os.path.expanduser(prefs.dataDir)) == True:
    for name in os.listdir(os.path.expanduser(path)):
      if os.path.isfile(os.path.join(os.path.expanduser(path), name)) and name.endswith(".obj"):
        if name not in blacklist:
          models[name] = name.rstrip(".obj")

    return True
  return False
