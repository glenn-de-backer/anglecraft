import bpy

# Panel for Object Settings
class AngleCraftObjectSettingsPanel(bpy.types.Panel):
    """
    Panel in the 3D View for setting the object and floor mesh for camera placement.
    """
    bl_label = "Object Settings"
    bl_idname = "VIEW3D_PT_lora_object_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AngleCraft'

    def draw(self, context):
        """Draw the Object Settings panel in the UI."""
        layout = self.layout
        scene = context.scene
        params = scene.lora_object_settings

        box = layout.box()
        box.prop(params, "object_name")
        box.prop(params, "floor_object_name")

        
# Panel for Camera settings
class AngleCraftCameraSettingsPanel(bpy.types.Panel):
    """
    Panel in the 3D View that contains the button to trigger the rendering process.
    """
    bl_label = "Camera settings"
    bl_idname = "VIEW3D_PT_lora_camera_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AngleCraft'

    def draw(self, context):
        """Draw the Render Button panel in the UI."""
        layout = self.layout
        scene = context.scene
        params = scene.lora_camera_settings
                
        box = layout.box()
        box.prop(params, "camera_base")


# Panel for Camera Sphere Settings
class AngleCraftCameraSphereSettingsPanel(bpy.types.Panel):
    """
    Panel in the 3D View for setting the camera sphere parameters such as radius, 
    number of cameras, and distribution type.
    """
    bl_label = "Camera Sphere Settings"
    bl_idname = "VIEW3D_PT_lora_camera_sphere_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AngleCraft'

    def draw(self, context):
        """Draw the Camera Sphere Settings panel in the UI."""
        layout = self.layout
        scene = context.scene
        params = scene.lora_camera_sphere_settings

        box = layout.box()
        
        box.prop(params, "min_radius")
        box.prop(params, "max_radius")
        box.prop(params, "num_cameras_horizontal")
        box.prop(params, "num_cameras_vertical")
        box.prop(params, "sphere_type")  # Add sphere type dropdown
        box.prop(params, "half_sphere")  # Add half sphere option
        box.prop(params, "remove_overlapping")
        box.prop(params, "overlap_threshold")
        
# Panel for Environment Settings
class AngleCraftEnvironmentSettingsPanel(bpy.types.Panel):
    """
    Panel in the 3D View for setting environment-related settings such as HDRI.
    """
    bl_label = "Environment Settifffngs"
    bl_idname = "VIEW3D_PT_lora_environment_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AngleCraft'  # Custom tab name    
    
    def draw(self, context):
        """Draw the Environment Settings panel in the UI."""
        layout = self.layout
        scene = context.scene
        params = scene.lora_render_settings

        box = layout.box()
        
        # Add toggle for overriding world
        box.prop(params, "override_world")
                
        # HDRI folder selection
        box.prop(params, "hdri_folder")

# Main Render Settings Panel
class AngleCraftRenderSettingsPanel(bpy.types.Panel):
    bl_label = "Render Settings"
    bl_idname = "VIEW3D_PT_lora_render_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AngleCraft'

    def draw(self, context):
        layout = self.layout

# Subpanel for General Render Settings
class AngleCraftGeneralRenderSettingsPanel(bpy.types.Panel):
    bl_label = "General Settings"
    bl_idname = "VIEW3D_PT_lora_general_render_settings"
    bl_parent_id = "VIEW3D_PT_lora_render_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AngleCraft'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        params = scene.lora_render_settings

        box = layout.box()
        box.prop(params, "output_directory")
        box.prop(params, "render_samples")
        box.prop(params, "render_resolution")

# Subpanel for Denoising Settings
class AngleCraftDenoiseSettingsPanel(bpy.types.Panel):
    bl_label = "Denoise Settings"
    bl_idname = "VIEW3D_PT_lora_denoise_settings"
    bl_parent_id = "VIEW3D_PT_lora_render_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AngleCraft'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        params = scene.lora_render_settings

        box = layout.box()
        box.prop(params, "denoise_enabled")
        box.prop(params, "denoiser")

        
# Panel for Render Button
class AngleCraftRenderButtonPanel(bpy.types.Panel):
    """
    Panel in the 3D View that contains the button to trigger the rendering process.
    """
    bl_label = "Render"
    bl_idname = "VIEW3D_PT_lora_render_button"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AngleCraft'

    def draw(self, context):
        """Draw the Render Button panel in the UI."""
        layout = self.layout
        scene = context.scene
        params = scene.lora_render_button_settings

        box = layout.box()
    
        box.operator("object.create_lora_cameras")
        box.operator("object.delete_lora_cameras")       
        box.operator("object.render_lora_cameras")

        # Add another box for the label to avoid overlap
        info_box = layout.box()
        info_box.label(text=f"Number of cameras: {params.info_num_cameras}", icon='INFO')