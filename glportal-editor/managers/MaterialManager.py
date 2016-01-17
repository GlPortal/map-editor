import bpy
import os
import xml.etree.cElementTree as ET

from ..updateTextures import *


materials = {}


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

    return True
  else:
    return False

def create(name = '', color = (1, 0, 0)):
  if name == '':
    print("Material name is empty.")
    return False

  if name in materials:
    prefs = bpy.context.user_preferences.addons[__package__.rpartition('.')[0]].preferences
    material = materials[name]
    path = os.path.expanduser(prefs.dataDir + 'textures/' +  material['texture'])

    try:
      image = bpy.data.images.load(path)
    except:
      raise NameError("Cannot load image %s" % path)

    texture = bpy.data.textures.new(name=material['fancyname'], type='IMAGE')
    texture.image = image

    mat = bpy.data.materials.new(material['fancyname'])
    mat.diffuse_color = color

    mtex = mat.texture_slots.add()
    mtex.texture = texture
    mtex.use_map_color_diffuse = True
    mtex.use_map_color_emission = True
    mtex.emission_color_factor = 0.5
    mtex.use_map_density = True
    mtex.use_map_emit = True
    mtex.emit_factor = 0.3

    if prefs.smartTexturesMapping:
      mtex.texture_coords = 'UV'
      mtex.mapping = 'FLAT'
    else:
      mtex.texture_coords = 'GLOBAL'
      mtex.mapping = 'CUBE'

    return mat
  else:
    print("Material '{0}' does not exist.", name)
    return False

def set(object, material, color = (1, 0, 0)):
  if object:
    mat = create(material, color)
    data = object.data

    if (len(data.materials) == 0):
      data.materials.append(mat)
    else:
      data.materials[0] = mat

    object.glpMaterial = material

    UpdateTexture.updateTexture(object)
  else:
    return False
