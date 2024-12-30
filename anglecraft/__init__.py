import bpy
from .operators import AngleCraftCreateCamerasOperator, AngleCraftRenderCamerasOperator, AngleCraftDeleteCamerasOperator
from .panels import AngleCraftObjectSettingsPanel, AngleCraftCameraSettingsPanel, AngleCraftCameraSphereSettingsPanel, AngleCraftEnvironmentSettingsPanel, AngleCraftRenderSettingsPanel, AngleCraftGeneralRenderSettingsPanel, AngleCraftDenoiseSettingsPanel, AngleCraftRenderButtonPanel
from .settings import AngleCraftCameraSettings, AngleCraftCameraSphereSettings, AngleCraftRenderSettings, AngleCraftRenderButtonSettings, AngleCraftObjectSettings

# Register and unregister the classes
def register():
    """
    Registers all the Blender classes and properties used by the addon.

    This function is called when the addon is enabled in Blender. It registers the 
    operators, property groups, and panels necessary for the functionality of the addon.
    """
    bpy.utils.register_class(AngleCraftCreateCamerasOperator)
    bpy.utils.register_class(AngleCraftRenderCamerasOperator)
    bpy.utils.register_class(AngleCraftDeleteCamerasOperator)
    bpy.utils.register_class(AngleCraftCameraSettings)
    bpy.utils.register_class(AngleCraftCameraSphereSettings)
    bpy.utils.register_class(AngleCraftRenderSettings)
    bpy.utils.register_class(AngleCraftRenderButtonSettings)
    bpy.utils.register_class(AngleCraftObjectSettings)
    bpy.utils.register_class(AngleCraftObjectSettingsPanel)
    bpy.utils.register_class(AngleCraftCameraSettingsPanel)
    bpy.utils.register_class(AngleCraftCameraSphereSettingsPanel)
    bpy.utils.register_class(AngleCraftEnvironmentSettingsPanel)
    bpy.utils.register_class(AngleCraftRenderSettingsPanel)
    bpy.utils.register_class(AngleCraftGeneralRenderSettingsPanel)
    bpy.utils.register_class(AngleCraftDenoiseSettingsPanel)

    bpy.utils.register_class(AngleCraftRenderButtonPanel)

    bpy.types.Scene.lora_camera_settings = bpy.props.PointerProperty(type=AngleCraftCameraSettings)
    bpy.types.Scene.lora_camera_sphere_settings = bpy.props.PointerProperty(type=AngleCraftCameraSphereSettings)
    bpy.types.Scene.lora_render_settings = bpy.props.PointerProperty(type=AngleCraftRenderSettings)
    bpy.types.Scene.lora_object_settings = bpy.props.PointerProperty(type=AngleCraftObjectSettings)
    bpy.types.Scene.lora_render_button_settings = bpy.props.PointerProperty(type=AngleCraftRenderButtonSettings)

def unregister():
    """
    Unregisters all the Blender classes and properties used by the addon.

    This function is called when the addon is disabled in Blender. It ensures that 
    all the classes, properties, and UI elements are properly removed.
    """
    bpy.utils.unregister_class(AngleCraftCreateCamerasOperator)
    bpy.utils.unregister_class(AngleCraftRenderCamerasOperator)
    bpy.utils.unregister_class(AngleCraftDeleteCamerasOperator)
    bpy.utils.register_class(AngleCraftCameraSettings)
    bpy.utils.unregister_class(AngleCraftCameraSphereSettings)
    bpy.utils.unregister_class(AngleCraftRenderSettings)
    bpy.utils.unregister_class(AngleCraftRenderButtonSettings)
    bpy.utils.unregister_class(AngleCraftObjectSettings)
    bpy.utils.unregister_class(AngleCraftObjectSettingsPanel)
    bpy.utils.unregister_class(AngleCraftCameraSettingsPanel)
    bpy.utils.unregister_class(AngleCraftCameraSphereSettingsPanel)
    bpy.utils.unregister_class(AngleCraftEnvironmentSettingsPanel)    
    bpy.utils.unregister_class(AngleCraftRenderSettingsPanel)
    bpy.utils.unregister_class(AngleCraftGeneralRenderSettingsPanel)
    bpy.utils.unregister_class(AngleCraftDenoiseSettingsPanel)

    bpy.utils.unregister_class(AngleCraftRenderButtonPanel)


    del bpy.types.Scene.lora_camera_settings
    del bpy.types.Scene.lora_camera_sphere_settings
    del bpy.types.Scene.lora_render_settings
    del bpy.types.Scene.lora_object_settings
    del bpy.types.Scene.lora_render_button_settings 

if __name__ == "__main__":
    """
    Main entry point for running the addon.

    Calls the `register()` function to enable the addon in Blender.
    """
    register()