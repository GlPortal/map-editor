import bpy
import os
import xml.etree.cElementTree as ET

from ..updateTextures import *
from .. import types

materials = {}
colors = {
  "metal/tiles00x3" : (0.2, 0.2, 0.2),
  "concrete/wall00" : (1, 1, 1),
  "fluid/acid00"    : (0.2, 1, 0.2),
  "none"            : (1, 0, 0)
}

def extractData(path, dir, name):
  mat = {'data': {'portalable': False}}

  tree = ET.parse(os.path.expanduser(path + dir + '/' + name))
  root = tree.getroot()

  mat['name'] = root.attrib['name']
  mat['data']['fancyname'] = root.attrib['fancyname']

  for child in root:
    if child.tag == "kind":
      mat['data']["kind"] = child.text
    elif child.tag == "surface":
      if child.attrib["portalable"] == 'true':
        mat['data']['portalable'] = True
    elif child.tag == "diffuse":
      mat['data']['texture'] = dir + '/' + child.attrib["path"]

  return mat

def preload():
  prefs = bpy.context.user_preferences.addons[__package__.rpartition('.')[0]].preferences
  path = prefs.dataDir + 'textures'

  if os.path.isdir(os.path.expanduser(prefs.dataDir)) == True:
    dirs = [ name for name in os.listdir(os.path.expanduser(path)) if os.path.isdir(os.path.join(os.path.expanduser(path), name)) ]

    for dir in dirs:
      files = [ name for name in os.listdir(os.path.expanduser(path + '/' + dir)) if os.path.isfile(os.path.join(os.path.expanduser(path + '/' + dir), name)) and name.endswith(".gmd") ]

      for file in files:
        mat = extractData(path + '/', dir, file)
        materials[mat['name']] = mat['data']
        types.glpMaterialTypes.append((mat['name'], mat['data']['fancyname'], mat['data']['fancyname']))
    types.glpMaterialSet()

    return True
  return False

def create(name = '', color = (-1, -1, -1), model = False):
  global colors, materials

  if name == '':
    print("Material name is empty.")
    return False

  if name in materials:
    prefs = bpy.context.user_preferences.addons[__package__.rpartition('.')[0]].preferences
    material = materials[name]
    fancyname = material['fancyname']
    path = os.path.expanduser(prefs.dataDir + 'textures/' +  material['texture'])

    try:
      image = bpy.data.images.load(path)
    except:
      raise NameError("Cannot load image %s" % path)

    if fancyname in bpy.data.textures:
      texture = bpy.data.textures[fancyname]
    else:
      texture = bpy.data.textures.new(name=fancyname, type='IMAGE')
      texture.image = image

    if fancyname in bpy.data.materials:
      mat = bpy.data.materials[fancyname]
      mtex = mat.texture_slots[0]
    else:
      mat = bpy.data.materials.new(fancyname)

      if color == (-1, -1, -1):
        if name in colors:
          mat.diffuse_color = colors[name]
        else:
          mat.diffuse_color = colors['none']
      else:
        mat.diffuse_color = color

      mtex = mat.texture_slots.add()
      mtex.texture = texture
      mtex.use_map_color_diffuse = True
      mtex.use_map_color_emission = True
      mtex.emission_color_factor = 0.5
      mtex.use_map_density = True
      mtex.use_map_emit = True
      mtex.emit_factor = 0.3

    if prefs.smartTexturesMapping or model:
      mtex.texture_coords = 'UV'
      mtex.mapping = 'FLAT'
    else:
      mtex.texture_coords = 'GLOBAL'
      mtex.mapping = 'CUBE'

    return mat
  else:
    print("Material '", name, "' does not exist.")
    return False

def set(object, material, color = (-1, -1, -1), model = False):
  if object:
    mat = create(material, color, model)
    data = object.data

    if (len(data.materials) == 0):
      data.materials.append(mat)
    else:
      data.materials[0] = mat

    object.glpMaterial = material

    if (object.glpTypes == "wall" or object.glpTypes == "volume"):
      updateTexture(object)
  else:
    return False

def reset(object):
  if object:
    object.glpMaterial = "none"

    if (len(object.data.materials) == 1):
      bpy.context.scene.objects.active = object
      bpy.ops.object.material_slot_remove()

def prepareExport():
  id = 1
  usedMaterials = {}
  objects = bpy.context.scene.objects

  for object in objects:
    if object.glpMaterial in materials and object.glpMaterial not in usedMaterials:
      usedMaterials[object.glpMaterial] = id
      id += 1
  return usedMaterials
