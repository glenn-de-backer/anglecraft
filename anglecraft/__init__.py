import bpy

from .operators import AngleCraftCreateCamerasOperator, AngleCraftDeleteCamerasOperator, anglecraft_hdri_handler
from .panels import AngleCraftObjectSettingsPanel, AngleCraftCameraSphereSettingsPanel, AngleCraftEnvironmentSettingsPanel, AngleCraftActionsButtonPanel
from .settings import AngleCraftCameraSphereSettings, AngleCraftRenderSettings, AngleCraftRenderButtonSettings, AngleCraftObjectSettings

# Register and unregister the classes
def register():
    """
    Registers all the Blender classes, properties, and handlers used by the addon.
    """
    bpy.utils.register_class(AngleCraftCreateCamerasOperator)
    bpy.utils.register_class(AngleCraftDeleteCamerasOperator)
    
    bpy.utils.register_class(AngleCraftCameraSphereSettings)
    bpy.utils.register_class(AngleCraftRenderSettings)
    bpy.utils.register_class(AngleCraftRenderButtonSettings)
    bpy.utils.register_class(AngleCraftObjectSettings)
    
    bpy.utils.register_class(AngleCraftObjectSettingsPanel)
    bpy.utils.register_class(AngleCraftCameraSphereSettingsPanel)
    bpy.utils.register_class(AngleCraftEnvironmentSettingsPanel)
    bpy.utils.register_class(AngleCraftActionsButtonPanel)

    bpy.types.Scene.lora_camera_sphere_settings = bpy.props.PointerProperty(type=AngleCraftCameraSphereSettings)
    bpy.types.Scene.lora_render_settings = bpy.props.PointerProperty(type=AngleCraftRenderSettings)
    bpy.types.Scene.lora_object_settings = bpy.props.PointerProperty(type=AngleCraftObjectSettings)
    bpy.types.Scene.lora_render_button_settings = bpy.props.PointerProperty(type=AngleCraftRenderButtonSettings)

    # Register the HDRI swap handler
    if anglecraft_hdri_handler not in bpy.app.handlers.frame_change_pre:
        bpy.app.handlers.frame_change_pre.append(anglecraft_hdri_handler)


def unregister():
    """
    Unregisters all the Blender classes, properties, and handlers used by the addon.
    """
    # Remove the HDRI swap handler
    if anglecraft_hdri_handler in bpy.app.handlers.frame_change_pre:
        bpy.app.handlers.frame_change_pre.remove(anglecraft_hdri_handler)

    bpy.utils.unregister_class(AngleCraftCreateCamerasOperator)
    bpy.utils.unregister_class(AngleCraftDeleteCamerasOperator)
    
    bpy.utils.unregister_class(AngleCraftCameraSphereSettings)
    bpy.utils.unregister_class(AngleCraftRenderSettings)
    bpy.utils.unregister_class(AngleCraftRenderButtonSettings)
    bpy.utils.unregister_class(AngleCraftObjectSettings)
    
    bpy.utils.unregister_class(AngleCraftObjectSettingsPanel)
    bpy.utils.unregister_class(AngleCraftCameraSphereSettingsPanel)
    bpy.utils.unregister_class(AngleCraftEnvironmentSettingsPanel)
    bpy.utils.unregister_class(AngleCraftActionsButtonPanel)

    del bpy.types.Scene.lora_camera_sphere_settings
    del bpy.types.Scene.lora_render_settings
    del bpy.types.Scene.lora_object_settings
    del bpy.types.Scene.lora_render_button_settings 

if __name__ == "__main__":
    register()