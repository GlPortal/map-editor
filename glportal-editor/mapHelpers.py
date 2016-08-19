import bpy
import math
from bpy.props import IntProperty

def fixObjects():
  objects = bpy.context.scene.objects
  bpy.ops.object.select_all(action='DESELECT')

  for object in objects:
    if object.type == 'MESH':
      type = object.glpTypes

      if type in {"wall", "trigger", "volume"}:
        bpy.context.scene.objects.active = object
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

def isOverObject(position, object):
  pMin = object.location[0] - abs(object.dimensions[0]) / 2
  pMax = object.location[0] + abs(object.dimensions[0]) / 2

  if position[0] > pMin and position[0] < pMax:
    pMin = object.location[1] - abs(object.dimensions[1]) / 2
    pMax = object.location[1] + abs(object.dimensions[1]) / 2

    if position[1] > pMin and position[1] < pMax:
      pMax = object.location[2] + abs(object.dimensions[2]) / 2

      if position[2] >= pMax + 1:
        return 1
      elif position[2] >= pMax:
        return 2
  return 0

def checkSpawnPosition(objects):
  for object in objects:
    if object.type == 'CAMERA':
      cameraPosition = object.location
      break
  for object in objects:
    if object.type == 'MESH' and object.glpTypes == "wall":
      isOver = isOverObject(cameraPosition, object)
      if isOver != 0:
        return isOver
  return 0

def countObjects(objects):
  result = {
    "camera":       0,
    "wall":         0,
    "acid":         0,
    "triggerDeath": 0,
    "light":        0,
    "exitDoor":     0,
    "objectNoMat":  0 # Objects Without Material
  }

  for object in objects:
    if object.glpTypes:
      type = object.glpTypes
    else:
      type = "None"

    if object.type == 'LAMP':
      result["light"] += 1
    elif object.type == 'CAMERA':
      result["camera"] += 1
    elif object.type == 'MESH':
      if type == "door":
        result["exitDoor"] += 1
      if type == "trigger":
        if object.glpTriggerTypes == "death":
          result["triggerDeath"] += 1
      if type == "wall":
        result["wall"] += 1
      if type == "volume":
        if object.glpVolumeTypes == "acid":
          result["acid"] += 1
      if type in {"model", "wall"}:
        if not object.glpMaterial or object.glpMaterial == "none":
          result["objectNoMat"] += 1
  return result

class checkMapDialog(bpy.types.Operator):
  bl_idname = "object.map_check_dialog"
  bl_label = "Check map results"

  camera = bpy.props.IntProperty (name="Number of cameras")
  light = bpy.props.IntProperty (name="Number of lights")
  wall = bpy.props.IntProperty (name="Number of walls")
  exitDoor = bpy.props.IntProperty (name="Number of exit doors")
  modelsNoMat = bpy.props.IntProperty (name="Number of models without material")

  def execute(self, context):
    return {'FINISHED'}

  def invoke(self, context, event):
    return context.window_manager.invoke_props_dialog(self, 400)

  def draw(self, context):
    objects = context.scene.objects
    result = countObjects(objects)
    layout = self.layout
    error = False

    if result["exitDoor"] != 1:
      self.exitDoor = result["exitDoor"]
      error = True

      layout.prop(self, "exitDoor")

      if result["exitDoor"] == 0:
        layout.label(text = "There is no exit door, use it exactly once.", icon='CANCEL')
      else:
        layout.label(text = "There are too many exit doors, use it exactly once.", icon='ERROR')
      layout.separator()
    if result["camera"] != 1:
      self.camera = result["camera"]
      error = True

      layout.prop(self, "camera")

      if result["camera"] == 0:
        layout.label(text = "There is no camera.", icon='CANCEL')
      else:
        layout.label(text = "There are too many cameras.", icon='ERROR')

      layout.label(text = "The camera object is used for determining the spawn position.",icon='INFO')
      layout.label(text = "Use it exactly once.",icon='INFO')
      layout.separator()
    if result["light"] == 0:
      error = True

      layout.label(text = "There is no light in the map you need at least one light.", icon='CANCEL')
      layout.separator()
    elif result["light"] > 5:
      self.light = result["light"]
      error = True

      layout.prop(self, "light")
      layout.label(text = "There are too many lights.", icon='INFO')
      layout.label(text = "This is a performance issue and has to be fixed..", icon='INFO')
      layout.separator()
    if result["wall"] == 0:
      self.wall = result["wall"]
      error = True

      layout.prop(self, "wall")
      layout.label(text = "There isn't a wall.", icon='ERROR')
      layout.separator()
    if result['triggerDeath'] < result['acid']:
      error = True

      layout.label(text = "Acid without death trigger.", icon='ERROR')
      layout.label(text = "Use death trigger for each volume of acid.", icon='INFO')
      layout.separator()
    if result["camera"] == 1:
      isOver = checkSpawnPosition(objects)

      if isOver == 0 or isOver == 2:
        if isOver == 0:
          error = True

          layout.label(text = "Camera is in the air.", icon='CANCEL')
        else:
          error = True

          layout.label(text = "Camera is very close to the floor.", icon='ERROR')
          layout.label(text = "Player can get stuck in the floor or unable to go through portal.", icon='INFO')

        layout.label(text = "Remember, we are using camera as spawn position.", icon='INFO')
        layout.separator()
    if result["objectNoMat"] != 0:
      error = True
      self.modelsNoMat = result["objectNoMat"]

      layout.prop(self, "modelsNoMat")

      row = layout.split(0.75)
      row.label(text = "There are objects without assigned material.", icon='ERROR')
      row.operator("glp.fix_materials")

      layout.separator()

    if not error:
      layout.label(text = "Nice work. There are no errors or warnings.", icon='FILE_TICK')
