import bpy


class CreationPanel(bpy.types.Panel):
  bl_label = "GlPortal"
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'TOOLS'
  bl_context = "objectmode"
  bl_category = "Create"

  def draw(self, context):
    layout = self.layout

    layout.label("Objects:")
    layout.operator("glp.add_door", icon='MESH_CUBE', text="Exit")
    layout.operator("glp.manager_search_add_model", icon='MESH_CUBE')
    layout.operator("glp.manager_search_set_material", icon='MATERIAL')

    layout.label("Walls:")
    layout.operator("glp.wall_add_portalable", icon='MESH_PLANE', text="Portalable")
    layout.operator("glp.wall_add_metal", icon='META_PLANE', text="Wall")

    layout.label("Volumes:")
    layout.operator("glp.volume_add_acid", icon='MESH_CUBE', text="Acid")

    layout.label("Triggers:")
    layout.operator("glp.trigger_add_death", icon='MESH_CUBE', text="Death")
    layout.operator("glp.trigger_add_radiation", icon='RADIO', text="Radiation")
    layout.operator("glp.trigger_add_win", icon='MESH_CUBE', text="Win")
    layout.operator("glp.trigger_add_map", icon='MESH_CUBE', text="Map")
    layout.operator("glp.trigger_add_audio", icon='MESH_CUBE', text="Audio")

    layout.label("Lights:")
    layout.operator("glp.add_light_common", icon='LAMP_POINT')
    layout.operator("glp.add_light_end", icon='LAMP_POINT')
