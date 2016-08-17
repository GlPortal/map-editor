import bpy
import math
import os
import xml.etree.cElementTree as ET

from .managers import ModelManager

class Importer():
  def __init__(self, filePath, deleteWorld = True):
    self.__filePath = filePath
    self.__deleteWorld = deleteWorld
    bpy.context.window_manager.importedFilepath = filePath

  def deleteWorld(self):
    scene = bpy.context.scene

    for ob in scene.objects:
      ob.select = True
      bpy.ops.object.delete()

  def extractMaterials(self, root):
    materials = {}

    for child in root:
      if child.tag == "materials":
        for mat in child:
          mid = mat.get("mid")
          name = mat.get("name")

          materials[mid] = name
    return materials

  def extractPosition(self, param):
    x = float(param.get("x"))
    y = float(param.get("y"))
    z = float(param.get("z"))
    return [x, -z, y]

  def extractDimensions(self, param):
    x = float(param.get("x"))
    y = float(param.get("y"))
    z = float(param.get("z"))
    return [x, z, y]

  def extractRotation(self, param):
    x = math.radians(float(param.get("x")))
    y = math.radians(float(param.get("y")))
    z = math.radians(-float(param.get("z")))
    return [x, z, y]

  def createCube(self, child):
    bpy.ops.mesh.primitive_cube_add()

    object = bpy.context.active_object
    if object:
      for param in child:
        if param.tag == "position":
          object.location = self.extractPosition(param)
        elif param.tag == "rotation":
          object.rotation_euler = self.extractRotation(param)
        elif param.tag == "scale":
          object.dimensions = self.extractDimensions(param)

      return True
    return False

  def getMaterials(self):
    realpath = os.path.realpath(os.path.expanduser(self.__filePath))
    tree = ET.parse(realpath)
    root = tree.getroot()

    return self.extractMaterials(root)

  def execute(self, context):
    if self.__deleteWorld:
      self.deleteWorld()

    prefs = bpy.context.user_preferences.addons[__package__].preferences
    realpath = os.path.realpath(os.path.expanduser(self.__filePath))
    tree = ET.parse(realpath)
    root = tree.getroot()
    materials = self.extractMaterials(root)

    for child in root:
      if child.tag == "wall":
        if self.createCube(child):
          object = bpy.context.active_object
          object.glpTypes = "wall"

          if "mid" in child.attrib:
            mid = child.get("mid")
            object.glpMaterial = materials[mid]
          else:
            object.glpMaterial = prefs.defaultMaterial
      elif child.tag == "acid":
        if self.createCube(child):
          bpy.ops.glp.set_acid()
      elif child.tag == "spawn":
        bpy.ops.object.camera_add()

        object = bpy.context.active_object
        if object:
          for param in child:
            if param.tag == "position":
              object.location = self.extractPosition(param)
            elif param.tag == "rotation":
              rotation = [math.radians(float(param.get("x")) + 90),
                          math.radians(0),
                          math.radians(float(param.get("y")))]
              object.rotation_euler = rotation
      elif child.tag == "light":
        bpy.ops.object.lamp_add(type='POINT')

        object = bpy.context.active_object
        if object:
          lamp = object.data

          object.location = self.extractPosition(child)

          lamp.color = [float(child.get("r")), float(child.get("g")), float(child.get("b"))]
          lamp.distance = float(child.get("distance"))
          lamp.energy = float(child.get("energy"))

          lamp.use_specular = False
          if "specular" in child.attrib and child.get("specular") == "1":
            lamp.use_specular = True
      # REMOVE this
      elif child.tag == "end":
        for param in child:
          if param.tag == "position":
            location = self.extractPosition(param)
          elif param.tag == "rotation":
            rotation = self.extractRotation(param)

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
      elif child.tag == "object":
        mesh = child.get("mesh")

        if "mid" in child.attrib:
          mid = child.get("mid")
          ModelManager.create(mesh, materials[mid])
        else:
           ModelManager.create(mesh)

        object = bpy.context.selected_objects[0]
        if object:
          for param in child:
            if param.tag == "position":
              object.location = self.extractPosition(param)
            elif param.tag == "rotation":
              object.rotation_euler = self.extractRotation(param)
            elif param.tag == "scale":
              object.dimensions = self.extractDimensions(param)
    return {'FINISHED'}
