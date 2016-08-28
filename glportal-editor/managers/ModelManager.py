import bpy
import os

models = {}
blacklist = [
  "GUIElement.obj",
  "Plane.obj",
  "Portal.obj",
  "PortalStencil.obj"
]

def reload():
  models.clear()
  preload()

def preload():
  prefs = bpy.context.user_preferences.addons[__package__.rpartition(".")[0]].preferences
  dataDir = os.path.expanduser(prefs.dataDir)
  path = os.path.join(dataDir, "meshes")

  if os.path.isdir(dataDir):
    for file in os.listdir(path):
      if os.path.isfile(os.path.join(path, file)) and file.endswith(".obj"):
        if file not in blacklist:
          models[file] = file.rstrip(".obj")
    return True
  return False

def create(file = "", materialName = ""):
  if file == "":
    print("Model file is empty.")
    return False

  if file in models:
    prefs = bpy.context.user_preferences.addons[__package__.rpartition(".")[0]].preferences
    dataDir = os.path.expanduser(prefs.dataDir)
    path = os.path.join(dataDir, "meshes", file)

    if os.path.isfile(path):
      bpy.ops.import_scene.obj(filepath = path)

      object = bpy.context.selected_objects[0]
      if object:
        object.location = bpy.context.scene.cursor_location
        object.glpTypes = "model"
        object.glpModel = file

        bpy.context.scene.objects.active = object
        bpy.ops.object.transform_apply(rotation=True)

        if materialName != "":
          object.glpMaterial = materialName
        else:
          object.glpMaterial = prefs.defaultMaterial
      return True
    return False

  print("Model '", file, "' does not exist.")
  return False
