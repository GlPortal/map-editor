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

    layout.operator("glp.wall_add_portalable", icon='MESH_PLANE', text="Portalable")
    layout.operator("glp.wall_add_metal", icon='META_PLANE', text="Metal")


class MenuTriggers(Menu):
  bl_idname = "glpMenu.triggers"
  bl_label = "Triggers"

  def draw(self, context):
    layout = self.layout

    layout.operator("glp.trigger_add_death", icon='MESH_CUBE', text="Death")
    layout.operator("glp.trigger_add_radiation", icon='RADIO', text="Radiation")
    layout.operator("glp.trigger_add_win", icon='MESH_CUBE', text="Win")
    layout.operator("glp.trigger_add_map", icon='MESH_CUBE', text="Map")
    layout.operator("glp.trigger_add_audio", icon='MESH_CUBE', text="Audio")


class MenuVolumes(Menu):
  bl_idname = "glpMenu.volumes"
  bl_label = "Volumes"

  def draw(self, context):
    layout = self.layout

    layout.operator("glp.volume_add_acid", icon='MESH_CUBE', text="Acid")


class MenuLights(Menu):
  bl_idname = "glpMenu.lights"
  bl_label = "Lights"

  def draw(self, context):
    layout = self.layout

    layout.operator("glp.add_light_common", icon='LAMP_POINT')
    layout.operator("glp.add_light_end", icon='LAMP_POINT')
