import bpy
from bpy.props import *
import os
import xml.etree.cElementTree as tree
import xml.dom.minidom as minidom
import math
import re

from . import mapHelpers

class Exporter():
  def __init__(self, filePath, d_p = 5):
    self.__filePath = filePath
    self.__d_p = d_p

  def storePosition(self, element, object):
    element.set("x", str(round(object.location[0], self.__d_p)))
    element.set("y", str(round(object.location[2], self.__d_p)))
    element.set("z", str(-round(object.location[1], self.__d_p)))

  # prepare rotation before exporting
  def prepareRot(self, degree):
    return str(round(degree % 360, self.__d_p))

  def checkRotation(self, object):
    x = math.degrees(object.rotation_euler[0])
    y = math.degrees(object.rotation_euler[2])
    z = math.degrees(-object.rotation_euler[1])

    if self.prepareRot(x) == "0.0" and self.prepareRot(y) == "0.0" and self.prepareRot(z) == "0.0":
      return False
    else:
      return True

  def storeRotation(self, element, object):
    element.set("x", self.prepareRot(math.degrees(object.rotation_euler[0])))
    element.set("y", self.prepareRot(math.degrees(object.rotation_euler[2])))
    element.set("z", self.prepareRot(math.degrees(-object.rotation_euler[1])))

  def storeScale(self, element, object):
    element.set("x", str(round(object.dimensions[0], self.__d_p)))
    element.set("y", str(round(object.dimensions[2], self.__d_p)))
    element.set("z", str(round(object.dimensions[1], self.__d_p)))

  def writeLampToTree(self, object, targetTree):
    lamp = object.data

    colorArray = lamp.color
    lightDistance = lamp.distance
    lightEnergy = lamp.energy

    lightElement = tree.SubElement(targetTree, "light")
    self.storePosition(lightElement, object);

    lightElement.set("r", str(round(colorArray[0], self.__d_p)))
    lightElement.set("g", str(round(colorArray[1], self.__d_p)))
    lightElement.set("b", str(round(colorArray[2], self.__d_p)))

    lightElement.set("distance", str(round(lightDistance, self.__d_p)))
    lightElement.set("energy", str(round(lightEnergy, self.__d_p)))

    if lamp.use_specular:
      lightElement.set("specular", "1")

  def execute(self, context):
    mapHelpers.fixObjects()

    dir = os.path.dirname(self.__filePath)
    objects = context.scene.objects
    root = tree.Element("map")

    # Materials
    materialElement = tree.SubElement(root, "materials")
    material1 = tree.SubElement(materialElement, "mat")
    material2 = tree.SubElement(materialElement, "mat")

    material1.set("mid", "1")
    material1.set("name", "concrete/wall00")
    material2.set("mid", "2")
    material2.set("name", "metal/tiles00x3")

    # Exporting
    for object in objects:
      object.select = False
    for object in reversed(objects):
      if object.glpTypes:
        type = object.glpTypes
      else:
        type = "None"

      if object.type == "LAMP":
        self.writeLampToTree(object, root)
      elif object.type == "CAMERA":
        boxElement = tree.SubElement(root, "spawn")

        positionElement = tree.SubElement(boxElement, "position")
        self.storePosition(positionElement, object)

        rotationElement = tree.SubElement(boxElement, "rotation")
        rotationElement.set("x", self.prepareRot(math.degrees(object.rotation_euler[0]) - 90))
        rotationElement.set("y", self.prepareRot(math.degrees(object.rotation_euler[2])))
        rotationElement.set("z", "0")
      elif object.type == "MESH" and type == "door":
        # tempotary add <end> instead of <door>
        boxElement = tree.SubElement(root, "end")

        positionElement = tree.SubElement(boxElement, "position")
        self.storePosition(positionElement, object)

        rotationElement = tree.SubElement(boxElement, "rotation")
        self.storeRotation(rotationElement, object)
      elif object.type == "MESH":
        boxElement = None

        if type == "trigger":
          boxElement = tree.SubElement(root, "trigger")
          if object.glpTriggerTypes:
            boxElement.set("type", object.glpTriggerTypes)
        elif type == "wall":
          boxElement = tree.SubElement(root, "wall")
          if object.glpWallTypes == "portalable":
            boxElement.set("mid", "1")
          else:
            boxElement.set("mid", "2")
        elif type == "volume":
          if object.glpVolumeTypes == "acid":
            boxElement = tree.SubElement(root, "acid")
        # disabled, will be enabled in the future
        # else:
        # boxElement = tree.SubElement(root, "door")
        if boxElement != None:
          object.select = True

          positionElement = tree.SubElement(boxElement, "position")
          self.storePosition(positionElement, object);

          if self.checkRotation(object):
            rotationElement = tree.SubElement(boxElement, "rotation")
            self.storeRotation(rotationElement, object);

          scaleElement = tree.SubElement(boxElement, "scale")
          self.storeScale(scaleElement, object);

          object.select = False

    xml = minidom.parseString(tree.tostring(root))

    file = open(self.__filePath, "w")
    fix = re.compile(r'((?<=>)(\n[\t]*)(?=[^<\t]))|(?<=[^>\t])(\n[\t]*)(?=<)')
    fixed_output = re.sub(fix, '', xml.toprettyxml())
    file.write(fixed_output)
    file.close()

    return {'FINISHED'}
