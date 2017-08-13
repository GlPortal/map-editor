import bpy
from bpy.props import EnumProperty, StringProperty, BoolProperty


GLP_TYPES = [
  ("none", "None", "No special property"),
  ("wall", "Wall", "Wall"),
  ("door", "Door", "Door"),  # REMOVE this
  ("volume", "Volume", "Volume"),
  ("trigger", "Trigger", "Trigger"),
  ("model", "Model", "Model")
]
GLP_VOLUME_TYPES = [
  ("none", "None", "No special property"),
  ("acid", "Acid Pool", "A pool full of acid, hurts..")
]
GLP_TRIGGER_TYPES = [
  ("none", "None", "No special property"),
  ("win", "Win", "Area triggers win"),
  ("map", "Map", "Area triggers new map"),
  ("audio", "Audio", "Area triggers new audio"),
  ("death", "Death", "Area triggers death"),
  ("radiation", "Radiation", "Area triggers radiation")
]
GLP_MATERIAL_TYPES = [
  ("none", "None", "No material")
]


def onUpdateGlpTypes(self, context):
  """Update object name based on object's game function"""
  objects = context.selected_objects
  for object in objects:
    type = object.glpTypes
    name = type

    if type == "trigger":
      name = type + "." + object.glpTriggerTypes
    elif type == "volume":
      name = type + "." + object.glpVolumeTypes
    elif type == "model":
      name = type + "." + object.glpModel
    else:
      name = type + "." + object.glpMaterial

    if object.glpTypes != "none":
      object.name = name


def setProperties():
  """Register properties for Blender"""
  bpy.types.Object.glpTypes = EnumProperty(
    items=GLP_TYPES,
    name="Type",
    description="GlPortal type",
    default="none",
    update=onUpdateGlpTypes
  )
  bpy.types.Object.glpVolumeTypes = EnumProperty(
    items=GLP_VOLUME_TYPES,
    name="Volume Type",
    default="none",
    update=onUpdateGlpTypes
  )
  bpy.types.Object.glpTriggerTypes = EnumProperty(
    items=GLP_TRIGGER_TYPES,
    name="Trigger Type",
    default="none",
    update=onUpdateGlpTypes
  )
  bpy.types.Object.glpTriggerFilepath = StringProperty(
    name="Filepath",
    description="Relative path to the file for trigger",
    default="none"
  )
  bpy.types.Object.glpTriggerAudioLoop = BoolProperty(
    name="Enable loop",
    description="Play audio file in loop",
    default=False
  )
  bpy.types.Object.glpModel = StringProperty(
    name="Model",
    description="Relative path to the model",
    default="none",
    update=onUpdateGlpTypes
  )
  bpy.types.WindowManager.importedFilepath = StringProperty(
    name="Imported filepath",
    default="none"
  )


def delProperties():
  """Unregister properties from Blender"""
  del bpy.types.Object.glpTypes
  del bpy.types.Object.glpVolumeTypes
  del bpy.types.Object.glpTriggerTypes
  del bpy.types.Object.glpTriggerFilepath
  del bpy.types.Object.glpTriggerAudioLoop
  del bpy.types.Object.glpModel
  del bpy.types.WindowManager.importedFilepath
  del bpy.types.Object.glpMaterial
