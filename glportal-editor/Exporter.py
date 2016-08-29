import bpy
import os
import xml.etree.cElementTree as tree
import xml.dom.minidom as minidom
import math
import re

from .mapHelpers import fixObjects
from .managers import MaterialManager
from .importer import Importer

class Exporter():
  mapFormatRadix = False

  def __init__(self, filePath, d_p = 4):
    self.__filePath = filePath
    self.__d_p = d_p
    bpy.context.window_manager.importedFilepath = filePath

  def writeMaterials(self, root, mats):
    materials = ((k, mats[k]) for k in sorted(mats, key=mats.get))
    materialElement = tree.SubElement(root, "materials")

    for name, index in materials:
      if self.mapFormatRadix:
        element = tree.SubElement(materialElement, "material")
        element.set("id", str(index))
      else:
        element = tree.SubElement(materialElement, "mat")
        element.set("mid", str(index))
      element.set("name", name)

  def storePosition(self, element, object):
    element.set("x", str(round(object.location[0], self.__d_p)))
    element.set("y", str(round(object.location[2], self.__d_p)))
    element.set("z", str(-round(object.location[1], self.__d_p)))

  def prepareRot(self, degree):
    return str(round(degree % 360, self.__d_p))

  def checkRotation(self, object):
    x = math.degrees(object.rotation_euler[0])
    y = math.degrees(object.rotation_euler[2])
    z = math.degrees(-object.rotation_euler[1])

    if self.prepareRot(x) == "0.0" and self.prepareRot(y) == "0.0" and self.prepareRot(z) == "0.0":
      return False
    return True

  def storeRotation(self, element, object):
    element.set("x", self.prepareRot(math.degrees(object.rotation_euler[0])))
    element.set("y", self.prepareRot(math.degrees(object.rotation_euler[2])))
    element.set("z", self.prepareRot(math.degrees(-object.rotation_euler[1])))

  def storeScale(self, element, object):
    element.set("x", str(round(object.dimensions[0], self.__d_p)))
    element.set("y", str(round(object.dimensions[2], self.__d_p)))
    element.set("z", str(round(object.dimensions[1], self.__d_p)))

  def storeColor(self, element, color):
    element.set("r", str(round(color[0], self.__d_p)))
    element.set("g", str(round(color[1], self.__d_p)))
    element.set("b", str(round(color[2], self.__d_p)))

  def writeLampToTree(self, object, targetTree):
    lamp = object.data

    colorArray = lamp.color
    lightDistance = lamp.distance
    lightEnergy = lamp.energy

    lightElement = tree.SubElement(targetTree, "light")

    if self.mapFormatRadix:
      positionElement = tree.SubElement(lightElement, "position")
      self.storePosition(positionElement, object)

      colorElement = tree.SubElement(lightElement, "color")
      self.storeColor(colorElement, colorArray)
    else:
      self.storePosition(lightElement, object)
      self.storeColor(lightElement, colorArray)

    lightElement.set("distance", str(round(lightDistance, self.__d_p)))
    lightElement.set("energy", str(round(lightEnergy, self.__d_p)))

    if lamp.use_specular:
      lightElement.set("specular", "1")

  def execute(self, context):
    fixObjects()

    prefs = bpy.context.user_preferences.addons[__package__].preferences
    dir = os.path.dirname(self.__filePath)
    objects = context.scene.objects
    root = tree.Element("map")

    if self.mapFormatRadix:
      matAttr = "material"
    else:
      matAttr = "mid"

    if os.path.isfile(self.__filePath):
      oldMap = Importer(self.__filePath)
      oldMap.mapFormatRadix = self.mapFormatRadix
      oldMaterials = oldMap.getMaterials()
    else:
      oldMaterials = {}

    materials = MaterialManager.prepareExport(oldMaterials)
    self.writeMaterials(root, materials)

    for object in reversed(objects):
      if object.glpTypes:
        type = object.glpTypes
      else:
        type = "None"

      if object.type == 'LAMP':
        self.writeLampToTree(object, root)
      elif object.type == 'CAMERA':
        boxElement = tree.SubElement(root, "spawn")

        positionElement = tree.SubElement(boxElement, "position")
        self.storePosition(positionElement, object)

        rotationElement = tree.SubElement(boxElement, "rotation")
        rotationElement.set("x", self.prepareRot(math.degrees(object.rotation_euler[0]) - 90))
        rotationElement.set("y", self.prepareRot(math.degrees(object.rotation_euler[2])))
        rotationElement.set("z", "0")
      elif object.type == 'MESH' and type == "door":
        # tempotary add <end> instead of <door>
        boxElement = tree.SubElement(root, "end")

        positionElement = tree.SubElement(boxElement, "position")
        self.storePosition(positionElement, object)

        rotationElement = tree.SubElement(boxElement, "rotation")
        self.storeRotation(rotationElement, object)
      elif object.type == 'MESH':
        boxElement = None

        if type == "model":
          if self.mapFormatRadix:
            boxElement = tree.SubElement(root, "model")
          else:
            boxElement = tree.SubElement(root, "object")
          boxElement.set("mesh", object.glpModel)

          if object.glpMaterial in materials and object.glpMaterial not in MaterialManager.blacklist:
            boxElement.set(matAttr, str(materials[object.glpMaterial]))
          else:
            boxElement.set(matAttr, str(materials[prefs.defaultMaterial]))
        elif type == "trigger":
          boxElement = tree.SubElement(root, "trigger")
          if object.glpTriggerTypes:
            boxElement.set("type", object.glpTriggerTypes)
        elif type == "wall":
          boxElement = tree.SubElement(root, "wall")

          if object.glpMaterial in materials and object.glpMaterial not in MaterialManager.blacklist:
            boxElement.set(matAttr, str(materials[object.glpMaterial]))
          else:
            boxElement.set(matAttr, str(materials[prefs.defaultMaterial]))
        elif type == "volume":
          if object.glpVolumeTypes == "acid":
            boxElement = tree.SubElement(root, "acid")
        if boxElement != None:
          positionElement = tree.SubElement(boxElement, "position")
          self.storePosition(positionElement, object)

          if self.checkRotation(object):
            rotationElement = tree.SubElement(boxElement, "rotation")
            self.storeRotation(rotationElement, object)

          scaleElement = tree.SubElement(boxElement, "scale")
          self.storeScale(scaleElement, object)

    xml = minidom.parseString(tree.tostring(root))

    file = open(self.__filePath, "w")
    fix = re.compile(r"((?<=>)(\n[\t]*)(?=[^<\t]))|(?<=[^>\t])(\n[\t]*)(?=<)")
    fixed_output = re.sub(fix, "", xml.toprettyxml())
    file.write(fixed_output)
    file.close()
    return {'FINISHED'}
