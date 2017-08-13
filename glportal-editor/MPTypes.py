import bpy

from bpy.props import BoolProperty, IntProperty, StringProperty

from .managers import MaterialManager as MM


def initProperties():
  """Register material panel properties for Blender"""
  bpy.types.WindowManager.MPItemId = IntProperty(
    default=0,
    update=MPItemIdUpdate
  )
  bpy.types.WindowManager.glpMatName = StringProperty(
    name="Name",
    default=""
  )
  bpy.types.WindowManager.glpMatFancyName = StringProperty(
    name="FancyName",
    default=""
  )
  bpy.types.WindowManager.glpMatPortalable = BoolProperty(
    name="Portalable",
    default=False
  )
  bpy.types.WindowManager.glpMatKind = StringProperty(
    name="Kind",
    default=""
  )
  bpy.types.WindowManager.glpMatTags = StringProperty(
    name="Tags",
    default=""
  )
  bpy.types.WindowManager.glpMatEdit = BoolProperty(
    default=False
  )


def delProperties():
  """Unregister material panel properties from Blender"""
  del bpy.types.WindowManager.MPItemId
  del bpy.types.WindowManager.glpMatName
  del bpy.types.WindowManager.glpMatFancyName
  del bpy.types.WindowManager.glpMatPortalable
  del bpy.types.WindowManager.glpMatKind
  del bpy.types.WindowManager.glpMatTags
  del bpy.types.WindowManager.glpMatEdit


class Row(bpy.types.PropertyGroup):
  name = StringProperty()
  label = StringProperty()
  description = StringProperty()
  matName = StringProperty()


def MPItemIdUpdate(self, context):
  wm = bpy.context.window_manager

  name = wm.MPMaterials[wm.MPItemId].matName
  material = MM.MATERIALS[name]

  if name != "none":
    if wm.glpMatEdit:
      wm.glpMatName = name
      wm.glpMatFancyName = material["fancyname"]
      wm.glpMatKind = material["kind"]
      wm.glpMatPortalable = material["portalable"]

      if "tags" in material:
        wm.glpMatTags = material["tags"]

    #prefs = bpy.context.user_preferences.addons[__package__].preferences
    #path = os.path.expanduser(prefs.dataDir + "textures/" +  material["texture"])
    #MM.createTexture(path, material["fancyname"])

  #for area in bpy.context.screen.areas:
  #  if area.type in ['PROPERTIES']:
  #    area.tag_redraw()
