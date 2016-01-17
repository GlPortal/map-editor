import bpy
from bpy.props import *

glpTypes = [
  ("none" ,   "None",     "No special property"),
  ("wall" ,   "Wall",     "Wall"),
  ("door" ,   "Door",     "Door"),# temporarily using as <end>
  ("volume",  "Volume",   "Volume"),
  ("trigger", "Trigger",  "trigger")
]

glpWallTypes = [
  ("none" ,       "None" ,        "No special property"),
  ("default" ,    "Default" ,     "Nothing special just a painted concrete wall"),
  ("invisible" ,  "Invisible" ,   "Invisible (Not implemented)"),
  ("glass" ,      "Glass" ,       "Glass (Not implemented)"),
  ("portalable" , "Portalable" ,  "Portalable Wall")
]

glpVolumeTypes = [
  ("none" ,   "None" ,     "No special property"),
  ("acid",    "Acid Pool", "A pool full of acid, hurts..")
]

glpTriggerTypes = [
  ("none" ,       "None" ,                "No special property"),
  ("win" ,        "Trigger Win" ,         "Area triggers win"),
  ("death" ,      "Trigger Death" ,       "Area triggers death"),
  ("radiation" ,  "Trigger Radiation" ,   "Area triggers radiation")
]

def setTypes():
  bpy.types.Object.glpTypes = EnumProperty(
    items = glpTypes,
    name = "Type"
  )

def setVolumeTypes():
  bpy.types.Object.glpVolumeTypes = EnumProperty(
    items = glpVolumeTypes,
    name = "Volume Type"
  )

def setTriggerTypes():
  bpy.types.Object.glpTriggerTypes = EnumProperty(
    items = glpTriggerTypes,
    name = "Trigger Type"
  )

def setWallTypes():
  bpy.types.Object.glpWallTypes = EnumProperty(
    items = glpWallTypes,
    name = "Wall Type"
  )

def setMaterialType():
  bpy.types.Object.glpMaterial = StringProperty(
    name = "Material",
    default = "",
  )

setTypes()
setVolumeTypes()
setTriggerTypes()
setWallTypes()
setMaterialType()
