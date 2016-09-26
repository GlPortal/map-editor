import bpy
import os
import xml.etree.cElementTree as ET
from bpy.props import EnumProperty

from ..updateTextures import updateTexture
from .. import types

materials = {}
colors = {
  "metal/tiles00x3" : (0.2, 0.2, 0.2),
  "concrete/wall00" : (1, 1, 1),
  "fluid/acid00"    : (0.2, 1, 0.2),
  "boxes/dev00"     : (0.8, 0.31, 0),
  "door/door"       : (1, 1, 1),
  "models/light-fixture" : (1, 1, 0),
  "crate/crate"     : (0, 1, 0),
  "none"            : (1, 0, 0)
}
blacklist = [
  "none"
]


def glpMaterialSet():
  bpy.types.Object.glpMaterial = EnumProperty (
    items = types.glpMaterialTypes,
    name = "Material",
    description = "Active material",
    default = "none",
    update = glpMaterialUpdate
  )

def glpMaterialReset():
  del types.glpMaterialTypes[:]
  types.glpMaterialTypes.append(("none", "None", "No material"))

def glpMaterialUpdate(self, context):
  objects = bpy.context.selected_objects
  for object in objects:
    if object.type == 'MESH' and object.glpTypes != "none":
      setMaterial(object)


def extractData(path, dir, name):
  mat = {"data": {"portalable": False}}

  filepath = os.path.join(path, dir, name)
  tree = ET.parse(filepath)
  root = tree.getroot()

  mat["name"] = root.attrib["name"]
  mat["data"]["fancyname"] = root.attrib["fancyname"]

  for child in root:
    if child.tag == "kind":
      mat["data"]["kind"] = child.text
    elif child.tag == "surface":
      if child.attrib["portalable"] == "true":
        mat["data"]["portalable"] = True
    elif child.tag == "diffuse":
      mat["data"]["texture"] = os.path.join(dir, child.attrib["path"])
    elif child.tag == "normal":
      mat["data"]["normaltex"] = os.path.join(dir, child.attrib["path"])

  return mat

def reload():
  materials.clear()
  glpMaterialReset()
  preload()

def preload():
  prefs = bpy.context.user_preferences.addons[__package__.rpartition('.')[0]].preferences
  dataDir = os.path.expanduser(prefs.dataDir)
  path = os.path.join(dataDir, "textures")

  materials["none"] = {"portalable": False, "kind": "None", "fancyname": "None"}

  if os.path.isdir(dataDir):
    dirs = [ name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) ]

    for dir in dirs:
      files = [ name for name in os.listdir(os.path.join(path, dir)) if os.path.isfile(os.path.join(path, dir, name)) and name.endswith(".gmd") ]

      for file in files:
        mat = extractData(path, dir, file)
        materials[mat["name"]] = mat["data"]
        types.glpMaterialTypes.append((mat["name"], mat["data"]["fancyname"], mat["data"]["fancyname"]))
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

def create(name = ""):
  global colors, materials

  if name == "":
    print("Material name is empty.")
    return False
  elif name == "none":
    material = materials[name]
    fancyname = material["fancyname"]

    if fancyname in bpy.data.materials:
      mat = bpy.data.materials[fancyname]
    else:
      mat = bpy.data.materials.new(fancyname)

      if name in colors:
        mat.diffuse_color = colors[name]
      else:
        mat.diffuse_color = colors["none"]

    return mat
  elif name in materials:
    prefs = bpy.context.user_preferences.addons[__package__.rpartition(".")[0]].preferences
    dataDir = os.path.expanduser(prefs.dataDir)
    material = materials[name]
    fancyname = material["fancyname"]
    path = os.path.join(dataDir, "textures",  material["texture"])

    if fancyname in bpy.data.materials:
      mat = bpy.data.materials[fancyname]
      mtex = mat.texture_slots[0]
    else:
      mat = bpy.data.materials.new(fancyname)

      if name in colors:
        mat.diffuse_color = colors[name]
      else:
        mat.diffuse_color = colors["none"]

      texture = createTexture(path, fancyname)
      if not texture:
        return False

      if "normaltex" in material:
        pathn = os.path.join(dataDir, "textures",  material["normaltex"])
        textureNormal = createTexture(pathn, fancyname + "_normal")
        if not textureNormal:
          return False
        else:
          mtex = mat.texture_slots.add()
          mtex.texture = texture
          mtex.use_map_normal = True
          mtex.normal_factor = 0.2
          mtex.use_map_color_diffuse = False
          mtex.use_map_color_emission = False
          mtex.use_map_density = False
          mtex.texture_coords = 'UV'
          mtex.mapping = 'FLAT'

      mtex = mat.texture_slots.add()
      mtex.texture = texture
      mtex.use_map_color_diffuse = True
      mtex.use_map_color_emission = True
      mtex.emission_color_factor = 0.5
      mtex.use_map_density = True
      mtex.use_map_emit = True
      mtex.emit_factor = 0.3
      mtex.texture_coords = 'UV'
      mtex.mapping = 'FLAT'

    return mat
  else:
    print("Material '", name, "' does not exist.")
    return False

def setMaterial(object):
  if object:
    mat = create(object.glpMaterial)
    data = object.data

    if (len(data.materials) == 0):
      data.materials.append(mat)
    else:
      data.materials[0] = mat

    if object.glpTypes in {"wall", "volume"}:
      updateTexture(object)
  else:
    return False

def reset(object):
  if object.glpTypes != "none" and object.glpMaterial != "none":
    object.glpMaterial = "none"

    if (len(object.data.materials) == 1):
      bpy.context.scene.objects.active = object
      bpy.ops.object.material_slot_remove()

def prepareExport(oldMaterials = {}):
  id = 1
  usedMaterials = {}
  objects = bpy.context.scene.objects
  prefs = bpy.context.user_preferences.addons[__package__.rpartition('.')[0]].preferences
  addDefault = False

  if len(oldMaterials) > 0:
    for key, name in oldMaterials.items():
      usedMaterials[name] = int(key)
      id += 1

  for object in objects:
    if (object.glpMaterial not in usedMaterials and
        object.type == 'MESH' and
        object.glpTypes != "trigger"):
      if (object.glpMaterial in materials and
          object.glpMaterial not in blacklist):
        usedMaterials[object.glpMaterial] = id
        id += 1
      else:
        addDefault = True

  if prefs.defaultMaterial not in usedMaterials and addDefault:
    usedMaterials[prefs.defaultMaterial] = id

  return usedMaterials
