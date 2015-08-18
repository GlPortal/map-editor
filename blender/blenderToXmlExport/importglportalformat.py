import bpy
from bpy.props import *
from bpy_extras.io_utils import ImportHelper
import os
import xml.etree.cElementTree as ET
import mathutils
import math
import string
from mathutils import Vector
import re
from .operators import *
from .triggerOperators import *
from .volumeOperators import *

def deleteWorld():
    scene = bpy.context.scene
    
    for ob in scene.objects:
        ob.select = True
        bpy.ops.object.delete()

def isPortalAble(root):
    for child in root:
        if child.tag == "materials":
            for param in child:
                if param.get("name") == "concrete/wall00":
                    return param.get("mid")

def extrackPosition(param):
    x = float(param.get("x"))
    y = float(param.get("y"))
    z = float(param.get("z"))
    
    return [x, -z, y]

def extrackDimensions(param):
    x = float(param.get("x"))
    y = float(param.get("y"))
    z = float(param.get("z"))
    
    return [x, z, y]

def extrackRotation(param, o_x = 0, o_y = 0, o_z = 0):
    x = math.radians(float(param.get("x")) + o_x)
    y = math.radians(float(param.get("y")) + o_y)
    z = math.radians(float(param.get("z")) + o_z)
    
    return [x, z, y]

class ImportGlPortalFormat(bpy.types.Operator, ImportHelper):
    bl_idname = "import_glportal_xml.xml"
    bl_label = "Import GlPortal XML"
    bl_description = "Import GlPortal XML file (.xml)"
    bl_options = {'PRESET'}
    filename_ext = ".xml"
    filter_glob = StringProperty(default="*.xml", options={'HIDDEN'})
    
    def execute(self, context):
        # Delete world berore importing
        deleteWorld()
        
        realpath = os.path.realpath(os.path.expanduser(self.filepath))
        tree = ET.parse(realpath)
        root = tree.getroot()
        
        portalAble = isPortalAble(root)
        
        for child in root:
            if child.tag == "wall":
                mid = child.get("mid")
                
                bpy.ops.mesh.primitive_cube_add()
                object = bpy.context.active_object
                if object:
                    for param in child:
                        if param.tag == "position":
                            object.location = extrackPosition(param)
                        elif param.tag == "rotation":
                            object.rotation_euler = extrackRotation(param);
                        elif param.tag == "scale":
                            object.dimensions = extrackDimensions(param)
                
                if mid == portalAble:
                    setPortalable.execute(self, context)
                else:
                    setWall.execute(self, context)
            elif child.tag == "acid":
                bpy.ops.mesh.primitive_cube_add()
                
                object = bpy.context.active_object
                if object:
                    for param in child:
                        if param.tag == "position":
                            object.location = extrackPosition(param)
                        elif param.tag == "rotation":
                            object.rotation_euler = extrackRotation(param)
                        elif param.tag == "scale":
                            object.dimensions = extrackDimensions(param)
                setAcid.execute(self, context)
            elif child.tag == "spawn":
                bpy.ops.object.camera_add()
                
                object = bpy.context.active_object
                if object:
                    for param in child:
                        if param.tag == "position":
                            object.location = extrackPosition(param)
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
                    
                    object.location = extrackPosition(child)
                    
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
                        location = extrackPosition(param)
                    elif param.tag == "rotation":
                        rotation = extrackRotation(param, 90);
                
                addDoor.execute(self, context)
                
                object = bpy.context.active_object
                object.location = location
                object.rotation_euler = rotation
            elif child.tag == "trigger":
                bpy.ops.mesh.primitive_cube_add()
                object = bpy.context.active_object
                if object:
                    for param in child:
                        if param.tag == "position":
                            object.location = extrackPosition(param)
                        elif param.tag == "rotation":
                            object.rotation_euler = extrackRotation(param)
                        elif param.tag == "scale":
                            object.dimensions = extrackDimensions(param)
                    
                    if child.get("type") == "death":
                        setDeath.execute(self, context)
                    elif child.get("type") == "radiation":
                        setRadiation.execute(self, context)
                    else:
                        object.delete()
        return {'FINISHED'}
