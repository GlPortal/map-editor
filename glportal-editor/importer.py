import bpy
import math
import os
import xml.etree.cElementTree as ET

class Importer():
  def __init__(self, filePath, deleteWorld = True):
    self.__filePath = filePath
    self.__deleteWorld = deleteWorld

  def deleteWorld(self):
    scene = bpy.context.scene

    for ob in scene.objects:
      ob.select = True
      bpy.ops.object.delete()

  def isPortalAble(self, root):
    for child in root:
      if child.tag == "materials":
        for param in child:
          if param.get("name") == "concrete/wall00":
            return param.get("mid")

  def extrackPosition(self, param):
    x = float(param.get("x"))
    y = float(param.get("y"))
    z = float(param.get("z"))

    return [x, -z, y]

  def extrackDimensions(self, param):
    x = float(param.get("x"))
    y = float(param.get("y"))
    z = float(param.get("z"))

    return [x, z, y]

  def extrackRotation(self, param, o_x = 0, o_y = 0, o_z = 0):
    x = math.radians(float(param.get("x")) + o_x)
    y = math.radians(float(param.get("y")) + o_y)
    z = math.radians(-float(param.get("z")) + o_z)

    return [x, z, y]

  def createCube(self, child):
    bpy.ops.mesh.primitive_cube_add()

    object = bpy.context.active_object
    if object:
      for param in child:
        if param.tag == "position":
          object.location = self.extrackPosition(param)
        elif param.tag == "rotation":
          object.rotation_euler = self.extrackRotation(param)
        elif param.tag == "scale":
          object.dimensions = self.extrackDimensions(param)

      return True
    return False

  def execute(self, context):
    if self.__deleteWorld:
      self.deleteWorld()

    realpath = os.path.realpath(os.path.expanduser(self.__filePath))
    tree = ET.parse(realpath)
    root = tree.getroot()

    portalAble = self.isPortalAble(root)


    for child in root:
      if child.tag == "wall":
        mid = child.get("mid")

        if self.createCube(child):
          if mid == portalAble:
            bpy.ops.glp.set_portalable()
          else:
            bpy.ops.glp.set_wall()
      elif child.tag == "acid":
        if self.createCube(child):
          bpy.ops.glp.set_acid()
      elif child.tag == "spawn":
        bpy.ops.object.camera_add()

        object = bpy.context.active_object
        if object:
          for param in child:
            if param.tag == "position":
              object.location = self.extrackPosition(param)
            elif param.tag == "rotation":
              rotation = [math.radians(float(param.get("x")) + 90),
                          math.radians(0),
                          math.radians(float(param.get("y")))]
              object.rotation_euler = rotation
      elif child.tag == "light":
        bpy.ops.object.lamp_add(type="POINT")

        object = bpy.context.active_object
        if object:
          lamp = object.data

          object.location = self.extrackPosition(child)

          lamp.color = [float(child.get("r")), float(child.get("g")), float(child.get("b"))]
          lamp.distance = float(child.get("distance"))
          lamp.energy = float(child.get("energy"))

          lamp.use_specular = False
          if "specular" in child.attrib and child.get("specular") == "1":
            lamp.use_specular = True
      # in futore we will change this for door and separate trigger for win
      elif child.tag == "end":
        for param in child:
          if param.tag == "position":
            location = self.extrackPosition(param)
          elif param.tag == "rotation":
            rotation = self.extrackRotation(param)

        bpy.ops.glp.add_door()

        object = bpy.context.active_object
        object.location = location

        object.rotation_euler = rotation
      elif child.tag == "trigger":
        if self.createCube(child):
          if child.get("type") == "death":
            bpy.ops.glp.set_death()
          elif child.get("type") == "radiation":
            bpy.ops.glp.set_radiation()
          else:
            object = bpy.context.active_object
            object.delete()

    return {'FINISHED'}
