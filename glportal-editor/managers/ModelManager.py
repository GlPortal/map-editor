import bpy
import os

from . import MaterialManager

models = {}
blacklist = [
  "GUIElement",
  "Plane",
  "Portal",
  "PortalStencil"
]

def preload():
  prefs = bpy.context.user_preferences.addons[__package__.rpartition(".")[0]].preferences
  path = prefs.dataDir + "meshes"

  if os.path.isdir(os.path.expanduser(prefs.dataDir)) == True:
    for file in os.listdir(os.path.expanduser(path)):
      if os.path.isfile(os.path.join(os.path.expanduser(path), file)) and file.endswith(".obj"):
        name = file.rstrip(".obj")

        if name not in blacklist:
          models[name] = file
    return True
  return False

def create(name = "", materialName = "", color = (1, 1, 1)):
  if name == "":
    print("Model name is empty.")
    return False

  if name in models:
    prefs = bpy.context.user_preferences.addons[__package__.rpartition(".")[0]].preferences
    path = os.path.expanduser(prefs.dataDir + "meshes/" +  models[name])

    if os.path.isfile(path):
      bpy.ops.import_scene.obj(filepath = path)

      if materialName != "":
        object = bpy.context.selected_objects[0]
        if object:
          object.location = bpy.context.scene.cursor_location
          object.glpTypes = "model"
          object.glpModel = name
          object.glpMaterial = materialName

          bpy.context.scene.objects.active = object
          bpy.ops.object.transform_apply(rotation=True)

          MaterialManager.set(object, color, True)
      return True
    return False

  print("Model '", name, "' does not exist.")
  return False
