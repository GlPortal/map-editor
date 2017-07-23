import bpy
from bpy.props import EnumProperty, StringProperty, BoolProperty


glpTypes = [
  ("none",    "None",    "No special property"),
  ("wall",    "Wall",    "Wall"),
  ("door",    "Door",    "Door"),# REMOVE this
  ("volume",  "Volume",  "Volume"),
  ("trigger", "Trigger", "Trigger"),
  ("model",   "Model",   "Model")
]
glpVolumeTypes = [
  ("none", "None",      "No special property"),
  ("acid", "Acid Pool", "A pool full of acid, hurts..")
]
glpTriggerTypes = [
  ("none",      "None",      "No special property"),
  ("win",       "Win",       "Area triggers win"),
  ("map",       "Map",       "Area triggers new map"),
  ("audio",     "Audio",     "Area triggers new audio"),
  ("death",     "Death",     "Area triggers death"),
  ("radiation", "Radiation", "Area triggers radiation")
]
glpMaterialTypes = [
  ("none", "None", "No material")
]

def onUpdateGlpTypes(self, context):
  objects = bpy.context.selected_objects
  for object in objects:
    if object.glpTypes != "none" and not object.name.lower().startswith(object.glpTypes):
      object.name = object.glpTypes

def setProperties():
  bpy.types.Object.glpTypes = EnumProperty (
    items = glpTypes,
    name = "Type",
    default = "none",
    update = onUpdateGlpTypes
  )
  bpy.types.Object.glpVolumeTypes = EnumProperty (
    items = glpVolumeTypes,
    name = "Volume Type",
    default = "none"
  )
  bpy.types.Object.glpTriggerTypes = EnumProperty (
    items = glpTriggerTypes,
    name = "Trigger Type",
    default = "none"
  )
  bpy.types.Object.glpTriggerFilepath = StringProperty (
    name = "Filepath",
    default = "none"
  )
  bpy.types.Object.glpTriggerAudioLoop = BoolProperty (
    name = "AudioLoop",
    default = False
  )
  bpy.types.Object.glpModel = StringProperty (
    name = "Model",
    default = "none"
  )
  bpy.types.WindowManager.importedFilepath = StringProperty (
    name = "Imported filepath",
    default = "none"
  )

def delProperties():
  del bpy.types.Object.glpTypes
  del bpy.types.Object.glpVolumeTypes
  del bpy.types.Object.glpTriggerTypes
  del bpy.types.Object.glpTriggerFilepath
  del bpy.types.Object.glpTriggerAudioLoop
  del bpy.types.Object.glpModel
  del bpy.types.WindowManager.importedFilepath
  del bpy.types.Object.glpMaterial
