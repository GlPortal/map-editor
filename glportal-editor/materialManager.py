import bpy
import os
import xml.etree.cElementTree as ET

class materialManager():
  materials = {}

  def __init__(self):
    pass

  def extractData(self, path, dir, name):
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

  def load(self):
    addon_prefs = bpy.context.user_preferences.addons[__package__].preferences
    path = addon_prefs.dataDir + 'textures'

    if os.path.exists(os.path.expanduser(addon_prefs.dataDir)) == True and os.path.isdir(os.path.expanduser(addon_prefs.dataDir)) == True:
      dirs = [ name for name in os.listdir(os.path.expanduser(path)) if os.path.isdir(os.path.join(os.path.expanduser(path), name)) ]

      for dir in dirs:
        files = [ name for name in os.listdir(os.path.expanduser(path + '/' + dir)) if os.path.isfile(os.path.join(os.path.expanduser(path + '/' + dir), name)) and name.endswith(".gmd") ]

        for file in files:
          mat = self.extractData(path + '/', dir, file)
          materialManager.materials[mat['name']] = mat['data']

      return True
    else:
      return False
