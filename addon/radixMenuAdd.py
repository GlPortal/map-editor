from bpy.types import Menu

class MenuMain(Menu):
  bl_idname = "radixMenu.main"
  bl_label = "Radix"

  def draw(self, context):
    layout = self.layout

    layout.menu("radixMenu.walls", icon='MOD_BUILD')
    layout.menu("radixMenu.volumes", icon='MOD_FLUIDSIM')
    layout.menu("radixMenu.triggers", icon='MOD_SCREW')
    layout.menu("radixMenu.lights", icon='LAMP_POINT')

    layout.operator("object.camera_add", text="Spawn (Camera)", icon='OUTLINER_OB_CAMERA')


class MenuWalls(Menu):
  bl_idname = "radixMenu.walls"
  bl_label = "Walls"

  def draw(self, context):
    layout = self.layout

    layout.operator("radix.wall_add_portalable", icon='MESH_PLANE', text="Portalable")
    layout.operator("radix.wall_add_metal", icon='META_PLANE', text="Metal")
