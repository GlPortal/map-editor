import bpy
import os
import xml.etree.cElementTree as ET
from bpy.props import EnumProperty

from .. import types

MATERIALS = {}
COLORS = {
  "metal/tiles00x3" : (0.2, 0.2, 0.2),
  "concrete/wall00" : (1, 1, 1),
  "fluid/acid00"    : (0.2, 1, 0.2),
  "boxes/dev00"     : (0.8, 0.31, 0),
  "door/door"       : (1, 1, 1),
  "models/light-fixture" : (1, 1, 0),
  "crate/crate"     : (0, 1, 0),
  "none"            : (1, 0, 0)
}
BLACKLIST = [
  "none"
]


def glpMaterialSet():
  bpy.types.Object.glpMaterial = EnumProperty(
    items=types.GLP_MATERIAL_TYPES,
    name="Material",
    description="Active material",
    default="none",
    update=glpMaterialUpdate
  )


def glpMaterialReset():
  del types.GLP_MATERIAL_TYPES[:]
  types.GLP_MATERIAL_TYPES.append(("none", "None", "No material"))


def glpMaterialUpdate(self, context):
  objects = bpy.context.selected_objects
  for object in objects:
    if object.type == 'MESH' and object.glpTypes != "none":
      setMaterial(object)
      types.onUpdateGlpTypes(self, context)


def saveMaterial(matName=""):
  if not matName:
    return

  prefs = bpy.context.user_preferences.addons[__package__.rpartition('.')[0]].preferences
  dataDir = os.path.expanduser(prefs.dataDir)

  if not os.path.isdir(dataDir):
    return

  name = matName.split("/")
  directory = name[0]
  gmdFile = name[1] + ".gmd"

  filepath = os.path.join(dataDir, "textures", directory, gmdFile)
  tree = ET.parse(filepath)
  root = tree.getroot()

  if MATERIALS[matName]["fancyname"]:
    root.set("fancyname", MATERIALS[matName]["fancyname"])

  for child in root:
    if child.tag == "kind":
      if MATERIALS[matName]["kind"]:
        child.text = MATERIALS[matName]["kind"]
    elif child.tag == "tags":
      if MATERIALS[matName]["tags"]:
        child.text = MATERIALS[matName]["tags"]
    elif child.tag == "surface":
      if MATERIALS[matName]["portalable"]:
        child.set("portalable", "true")
      else:
        child.set("portalable", "false")

  tree.write(filepath, "UTF-8")


def extractData(path, dir, name):
  mat = {"data": {"portalable": False}}

  filepath = os.path.join(path, dir, name)
  tree = ET.parse(filepath)
  root = tree.getroot()

  mat["name"] = root.attrib["name"]

  if "fancyname" in root.attrib:
    mat["data"]["fancyname"] = root.attrib["fancyname"]
  else:
    mat["data"]["fancyname"] = mat["name"]

  for child in root:
    if child.tag == "kind":
      mat["data"]["kind"] = child.text
    elif child.tag == "tags":
      mat["data"]["tags"] = child.text
    elif child.tag == "surface":
      if child.attrib["portalable"] == "true":
        mat["data"]["portalable"] = True
    elif child.tag == "diffuse":
      mat["data"]["texture"] = os.path.join(dir, child.attrib["path"])
    elif child.tag == "normal":
      mat["data"]["normaltex"] = os.path.join(dir, child.attrib["path"])
    elif child.tag == "specular":
      mat["data"]["speculartex"] = os.path.join(dir, child.attrib["path"])
      mat["data"]["shininess"] = float(child.attrib["shininess"]) / 6

  return mat


def reload():
  MATERIALS.clear()
  glpMaterialReset()
  preload()


def preload():
  MATERIALS["none"] = {"portalable": False, "kind": "None", "fancyname": "None"}

  prefs = bpy.context.user_preferences.addons[__package__.rpartition('.')[0]].preferences
  dataDir = os.path.expanduser(prefs.dataDir)
  path = os.path.join(dataDir, "textures")

  files = os.path.browse(
    directory="textures", extension="gmd", blacklist=BLACKLIST, recursive=True
  )

  if files:
    for dir, entries in files.items():
      for fileName, name in entries.items():
        mat = extractData(path, dir, fileName)
        MATERIALS[mat["name"]] = mat["data"]
        types.GLP_MATERIAL_TYPES.append(
          (mat["name"], mat["data"]["fancyname"], mat["data"]["fancyname"])
        )
    glpMaterialSet()

    return True
  return False


def createTexture(imagePath, textureName):
  if textureName in bpy.data.textures:
    texture = bpy.data.textures[textureName]
  else:
    try:
      image = bpy.data.images.load(imagePath)
    except:
      return False

    texture = bpy.data.textures.new(name=textureName, type='IMAGE')
    texture.image = image

  return texture


def addTexture(mat, texture):
  mtex = mat.texture_slots.add()
  mtex.texture = texture
  mtex.texture_coords = 'UV'
  mtex.mapping = 'FLAT'

  return mtex


def setDiffuseTexture(mtex):
  mtex.use_map_color_diffuse = True
  mtex.use_map_color_emission = True
  mtex.emission_color_factor = 0.5
  mtex.use_map_density = True
  mtex.use_map_emit = True
  mtex.emit_factor = 0.3


def setNormalTexture(mtex):
  mtex.use_map_normal = True
  mtex.normal_factor = 0.2
  mtex.use_map_color_diffuse = False
  mtex.use_map_color_emission = False
  mtex.use_map_density = False
  mtex.use_map_emit = False


def setSpecularTexture(mtex, shininess):
  mtex.use_map_specular = True
  mtex.specular_factor = shininess
  mtex.use_map_color_spec = True
  mtex.use_map_hardness = True
  mtex.use_map_color_diffuse = False
  mtex.use_map_color_emission = False
  mtex.use_map_density = False
  mtex.use_map_emit = False


def create(name=""):
  global COLORS, MATERIALS

  if not name:
    print("Material name is empty.")
    return False
  elif name == "none":
    material = MATERIALS[name]
    fancyname = material["fancyname"]

    if fancyname in bpy.data.materials:
      mat = bpy.data.materials[fancyname]
    else:
      mat = bpy.data.materials.new(fancyname)

      if name in COLORS:
        mat.diffuse_color = COLORS[name]
      else:
        mat.diffuse_color = COLORS["none"]

    return mat
  elif name in MATERIALS:
    prefs = bpy.context.user_preferences.addons[__package__.rpartition(".")[0]].preferences
    dataDir = os.path.expanduser(prefs.dataDir)
    material = MATERIALS[name]
    fancyname = material["fancyname"]

    if fancyname in bpy.data.materials:
      mat = bpy.data.materials[fancyname]
      mtex = mat.texture_slots[0]
    else:
      mat = bpy.data.materials.new(fancyname)

      if name in COLORS:
        mat.diffuse_color = COLORS[name]
      else:
        mat.diffuse_color = COLORS["none"]

      if "texture" in material:
        path = os.path.join(dataDir, "textures", material["texture"])
        texture = createTexture(path, fancyname)
        if texture:
          mtex = addTexture(mat, texture)
          setDiffuseTexture(mtex)
        else:
          return False

      if "normaltex" in material:
        path = os.path.join(dataDir, "textures", material["normaltex"])
        texture = createTexture(path, fancyname + "_normal")
        if texture:
          mtex = addTexture(mat, texture)
          setNormalTexture(mtex)

      if "speculartex" in material:
        path = os.path.join(dataDir, "textures", material["speculartex"])
        texture = createTexture(path, fancyname + "_specular")
        if texture:
          mtex = addTexture(mat, texture)
          setSpecularTexture(mtex, material["shininess"])

    return mat
  else:
    print("Material '", name, "' does not exist.")
    return False


def setMaterial(object):
  if object:
    mat = create(object.glpMaterial)
    data = object.data

    if not data.materials:
      data.materials.append(mat)
    else:
      data.materials[0] = mat

    if object.glpTypes in {"wall", "volume"}:
      object.updateTexture()
  else:
    return False


def reset(object):
  if object.glpTypes != "none" and object.glpMaterial != "none":
    object.glpMaterial = "none"

    if len(object.data.materials) == 1:
      bpy.context.scene.objects.active = object
      bpy.ops.object.material_slot_remove()


def prepareExport(oldMaterials={}):
  id = 1
  usedMaterials = {}
  objects = bpy.context.scene.objects
  prefs = bpy.context.user_preferences.addons[__package__.rpartition('.')[0]].preferences
  addDefault = False

  if oldMaterials:
    for key, name in oldMaterials.items():
      usedMaterials[name] = int(key)
      id += 1

  for object in objects:
    if (
      object.glpMaterial not in usedMaterials and
      object.type == 'MESH' and
      object.glpTypes not in {"door", "trigger", "volume"}
    ):
      if (
        object.glpMaterial in MATERIALS and
        object.glpMaterial not in BLACKLIST
      ):
        usedMaterials[object.glpMaterial] = id
        id += 1
      else:
        addDefault = True

  if prefs.defaultMaterial not in usedMaterials and addDefault:
    usedMaterials[prefs.defaultMaterial] = id

  return usedMaterials
