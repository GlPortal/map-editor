from bpy.types import Menu


def glportal_add_menu(self, context):
  layout = self.layout

  layout.menu("glpMenu.main", icon='WORLD')
  layout.separator()


class MenuMain(Menu):
  bl_idname = "glpMenu.main"
  bl_label = "GlPortal"

  def draw(self, context):
    layout = self.layout

    layout.menu("glpMenu.walls", icon='MOD_BUILD')
    layout.menu("glpMenu.volumes", icon='MOD_FLUIDSIM')
    layout.menu("glpMenu.triggers", icon='MOD_SCREW')
    layout.menu("glpMenu.lights", icon='LAMP_POINT')

    layout.operator("object.camera_add", text="Spawn (Camera)", icon='OUTLINER_OB_CAMERA')
    layout.operator("glp.add_door", text="Exit", icon='MESH_CUBE')


class MenuWalls(Menu):
  bl_idname = "glpMenu.walls"
  bl_label = "Walls"

  def draw(self, context):
    layout = self.layout

    layout.operator("glp.add_portalable", icon='MESH_PLANE')
    layout.operator("glp.add_wall", icon='META_PLANE')


class MenuTriggers(Menu):
  bl_idname = "glpMenu.triggers"
  bl_label = "Triggers"

  def draw(self, context):
    layout = self.layout

    layout.operator("glp.add_death", icon='MESH_CUBE')
    layout.operator("glp.add_radiation", icon='RADIO')
    layout.operator("glp.add_win", icon='MESH_CUBE')
    layout.operator("glp.add_map_trigger", icon='MESH_CUBE')
    layout.operator("glp.add_audio_trigger", icon='MESH_CUBE')


class MenuVolumes(Menu):
  bl_idname = "glpMenu.volumes"
  bl_label = "Volumes"

  def draw(self, context):
    layout = self.layout

    layout.operator("glp.add_acid", icon='MESH_CUBE')


class MenuLights(Menu):
  bl_idname = "glpMenu.lights"
  bl_label = "Lights"

  def draw(self, context):
    layout = self.layout

    layout.operator("glp.add_light_common", icon='LAMP_POINT')
    layout.operator("glp.add_light_end", icon='LAMP_POINT')
