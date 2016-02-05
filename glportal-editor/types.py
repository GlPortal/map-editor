import bpy
from bpy.props import EnumProperty, StringProperty

from .managers import MaterialManager

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
  ("death",     "Death",     "Area triggers death"),
  ("radiation", "Radiation", "Area triggers radiation")
]

glpMaterialTypes = [
  ("none", "None", "No special property")
]

def glpMaterialSet():
  bpy.types.Object.glpMaterial = EnumProperty (
    items = glpMaterialTypes,
    name = "Material",
    default = "none"
  )

def glpMaterialReset():
  del glpMaterialTypes[:]
  glpMaterialTypes.append(("none", "None", "No special property"))

def setProperties():
  bpy.types.Object.glpTypes = EnumProperty (
    items = glpTypes,
    name = "Type"
  )
  bpy.types.Object.glpVolumeTypes = EnumProperty (
    items = glpVolumeTypes,
    name = "Volume Type"
  )
  bpy.types.Object.glpTriggerTypes = EnumProperty (
    items = glpTriggerTypes,
    name = "Trigger Type"
  )
  bpy.types.Object.glpModel = StringProperty (
    name = "Model",
    default = "none",
  )

setProperties()
glpMaterialSet()