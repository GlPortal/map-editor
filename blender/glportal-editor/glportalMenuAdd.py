import bpy

def glportal_add_menu(self, context):
    layout = self.layout
    
    layout.menu("OBJECT_MT_glportal_add_menu_main", icon = "WORLD")
    
    layout.separator()

class GlPortalAddMenuMain(bpy.types.Menu):
    bl_idname = "OBJECT_MT_glportal_add_menu_main"
    bl_label = "GlPortal"
    
    def draw(self, context):
        layout = self.layout
        
        layout.menu("OBJECT_MT_glportal_add_menu_walls", icon = 'MOD_BUILD')
        layout.menu("OBJECT_MT_glportal_add_menu_volumes", icon = 'MOD_FLUIDSIM')
        layout.menu("OBJECT_MT_glportal_add_menu_triggers", icon = 'MOD_SCREW')
        
        layout.operator("object.lamp_add", text = "Light", icon = 'LAMP_POINT').type = 'POINT'
        layout.operator("object.camera_add", text = "Spawn (Camera)", icon = 'OUTLINER_OB_CAMERA')
        layout.operator("wm.add_door", text = "Exit", icon = 'MESH_CUBE')

class GlPortalAddMenuWalls(bpy.types.Menu):
    bl_idname = "OBJECT_MT_glportal_add_menu_walls"
    bl_label = "Walls"
    
    def draw(self, context):
        layout = self.layout
        
        layout.operator("wm.add_portalable", text = "Portalable", icon = 'MESH_PLANE')
        layout.operator("wm.add_wall", text = "Metal", icon = 'META_PLANE')

class GlPortalAddMenuTriggers(bpy.types.Menu):
    bl_idname = "OBJECT_MT_glportal_add_menu_triggers"
    bl_label = "Triggers"
    
    def draw(self, context):
        layout = self.layout
        
        layout.operator("wm.add_death", text = "Death", icon = 'MESH_CUBE')
        layout.operator("wm.add_radiation", text = "Radiation", icon = 'RADIO')
        layout.operator("wm.add_win", text = "Win", icon = 'MESH_CUBE')

class GlPortalAddMenuVolumes(bpy.types.Menu):
    bl_idname = "OBJECT_MT_glportal_add_menu_volumes"
    bl_label = "Volumes"
    
    def draw(self, context):
        layout = self.layout
        
        layout.operator("wm.add_acid", text = "Acid", icon = 'MESH_CUBE')
