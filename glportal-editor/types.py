import bpy
from bpy.props import EnumProperty, StringProperty, CollectionProperty, BoolProperty


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
  ("none", "None", "No material")
]


class MPColl(bpy.types.PropertyGroup):
  name = bpy.props.StringProperty()
  label = bpy.props.StringProperty()
  description = bpy.props.StringProperty()
  matName = bpy.props.StringProperty()

def setProperties():
  bpy.types.Object.glpTypes = EnumProperty (
    items = glpTypes,
    name = "Type",
    default = "none"
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
  bpy.types.Object.glpModel = StringProperty (
    name = "Model",
    default = "none"
  )
  bpy.types.WindowManager.importedFilepath = StringProperty (
    name = "Imported filepath",
    default = "none"
  )
  bpy.types.WindowManager.glpMatName = StringProperty (
    name = "Name",
    default = ""
  )
  bpy.types.WindowManager.glpMatFancyName = StringProperty (
    name = "FancyName",
    default = ""
  )
  bpy.types.WindowManager.glpMatPortalable = BoolProperty (
    name = "Portalable",
    default = False
  )
  bpy.types.WindowManager.glpMatKind = StringProperty (
    name = "Kind",
    default = ""
  )
  bpy.types.WindowManager.glpMatEdit = BoolProperty (
    name = "Edit",
    default = False
  )

def delProperties():
  del bpy.types.Object.glpTypes
  del bpy.types.Object.glpVolumeTypes
  del bpy.types.Object.glpTriggerTypes
  del bpy.types.Object.glpModel
  del bpy.types.WindowManager.importedFilepath
  del bpy.types.Object.glpMaterial
  del bpy.types.WindowManager.MPItemId
  del bpy.types.WindowManager.glpMatName
  del bpy.types.WindowManager.glpMatFancyName
  del bpy.types.WindowManager.glpMatPortalable
  del bpy.types.WindowManager.glpMatKind
  del bpy.types.WindowManager.glpMatEdit
