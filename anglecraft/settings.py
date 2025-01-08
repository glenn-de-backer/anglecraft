import bpy

# Properties to control object settings
class AngleCraftObjectSettings(bpy.types.PropertyGroup):
    """
    Property group to manage settings related to the object being used for camera placement.
    Includes dynamic generation of camera target and floor object lists.
    """
    def update_object_list(self, context):
        """Update object list for EnumProperty dynamically."""
        self["object_name"] = self.object_name

    def update_floor_list(self, context):
        """Update floor object list for EnumProperty dynamically."""
        self["floor_object_name"] = self.floor_object_name

    def object_enum_items(self, context):
        """
        Generate items for object_name dynamically by selecting objects of type 'EMPTY'.
        """
        return [(obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == 'EMPTY']

    def floor_enum_items(self, context):
        """
        Generate items for floor_object_name dynamically by selecting objects of type 'MESH'.
        Includes a 'None' option for optional selection.
        """
        items = [(obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == 'MESH']
        items.insert(0, ('NONE', 'None', 'No object selected'))
        return items
    
    object_name: bpy.props.EnumProperty(
        name="Camera target",
        description="Select the target empty for camera placement",
        items=object_enum_items,
        update=update_object_list
    )
    
    floor_object_name: bpy.props.EnumProperty(
        name="Floor Mesh",
        description="Select the floor mesh object",
        items=floor_enum_items,
        update=update_floor_list
    )


# Properties to control object settings
class AngleCraftCameraSettings(bpy.types.PropertyGroup):
    def object_enum_cameras(self, context):
        """
        Generate items for camera_base dynamically by selecting objects of type 'CAMERA'.
        """
        items = [(obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == 'CAMERA']
        items.insert(0, ("None", "None", "Do not clone any camera"))  # Add the 'None' option at the beginning
        return items
    
    camera_base: bpy.props.EnumProperty(
        name="Camera Base",
        description="Select the camera that will function as the one to clone",
        items=object_enum_cameras
    )
    

# Properties to control camera sphere settings
class AngleCraftCameraSphereSettings(bpy.types.PropertyGroup):
    """
    Property group for controlling the camera sphere settings such as radius, 
    number of cameras, and distribution type.
    """
    min_radius: bpy.props.FloatProperty(
        name="Min Radius",
        default=10.0,
        min=0.1,
        description="Minimum distance of cameras from the object"
    )
    
    max_radius: bpy.props.FloatProperty(
        name="Max Radius",
        default=10.0,
        min=0.1,
        description="Maximum distance of cameras from the object"
    )
    
    radius: bpy.props.FloatProperty(
        name="Radius",
        default=10.0,
        min=0.1,
        description="Distance of cameras from the object"
    )
    
    num_cameras_horizontal: bpy.props.IntProperty(
        name="Horizontal Cameras",
        default=16,
        min=1,
        description="Number of cameras in the horizontal circle"
    )
    
    num_cameras_vertical: bpy.props.IntProperty(
        name="Vertical Cameras",
        default=8,
        min=1,
        description="Number of vertical levels of cameras"
    )
    
    half_sphere: bpy.props.BoolProperty(
        name="Half Sphere",
        default=False,
        description="If checked, create only the upper half of the cameras"
    )
    
    sphere_type: bpy.props.EnumProperty(
        name="Sphere Type",
        description="Select the type of sphere generation",
        items=[
            ('linear', 'Linear', 'Linear distribution of cameras'),
            ('uniform', 'Uniform', 'Uniform distribution of cameras'),
            ('fibonacci', 'Fibonacci', 'Fibonacci sphere distribution'),
            ('equator_dense', 'Equator Dense', 'Denser distribution of cameras at the equator'),
            ('weighted', 'Weighted (Top 80%, Bottom 20%)', '80% cameras on the top hemisphere, 20% on the bottom hemisphere'),
        ],
        default='weighted'
    )

    remove_overlapping: bpy.props.BoolProperty(
        name="Remove Overlapping",
        default=False,
        description="Remove overlapping cameras"
    )
    overlap_threshold: bpy.props.FloatProperty(
        name="Overlap Threshold",
        default=0.1,
        min=0.0,
        description="Minimum distance between cameras to avoid overlap"
    )


# Properties for render settings
class AngleCraftRenderSettings(bpy.types.PropertyGroup):
    """
    Property group for controlling the render settings such as output directory, 
    render samples, denoiser, and resolution.
    """
    output_directory: bpy.props.StringProperty(
        name="Output Directory",
        default="//output",
        description="Directory to save rendered images",
        subtype='DIR_PATH'  # Use folder selection dialog
    )
    
    render_samples: bpy.props.IntProperty(
        name="Render Samples",
        default=128,
        min=1,
        description="Number of render samples"
    )
    
    denoise_enabled: bpy.props.BoolProperty(
        name="Enable Denoising",
        default=True,
        description="Enable or disable denoising for the rendered image"
    )
    
    denoiser: bpy.props.EnumProperty(
        name="Denoiser",
        description="Choose the denoiser to use",
        items=[
            ('OPTIX', 'OPTIX', 'Use NVIDIA OptiX denoiser'),
            ('OPENIMAGEDENOISE', 'Open Image Denoise', 'Use Intel Open Image Denoise'),
            ('NONE', 'None', 'No denoising applied')
        ],
        default='OPTIX'  # Default to OPTIX if no choice is made
    )
    
    render_resolution: bpy.props.IntVectorProperty(
        name="Resolution",
        default=(512, 512),
        size=2,
        min=1,
        description="Resolution for rendering"
    )
    
    hdri_folder: bpy.props.StringProperty(
        name="HDRI Folder",
        default="",
        description="Folder containing HDRI images",
        subtype='DIR_PATH'  # Use folder selection dialog
    )
    
    override_world: bpy.props.BoolProperty(
        name="Override World",
        default=False,
        description="Override the current world settings with a new HDRI"
    )


    render_depth_maps: bpy.props.BoolProperty(
        name="Render Depth Maps",
        default=False,
        description="Enable or disable rendering of depth maps"
    )

# Properties to control object settings
class AngleCraftRenderButtonSettings(bpy.types.PropertyGroup):
    info_num_cameras: bpy.props.IntProperty(
        name="Number of Cameras",
        default=0,
        description="Number of cameras/renders that will be produced",
        options={'HIDDEN'}  # Hide this property from the UI
    )

