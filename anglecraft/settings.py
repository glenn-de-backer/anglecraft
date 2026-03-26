import bpy

# Properties to control object settings
class AngleCraftObjectSettings(bpy.types.PropertyGroup):
    """
    Property group for object settings related to camera placement.

    Attributes:
        object_name (EnumProperty): The name of the target empty object for camera placement.
        floor_object_name (EnumProperty): The name of the floor mesh object.
    """
    def update_object_list(self, context):
        """
        Update method for the object list property.
        """
        self["object_name"] = self.object_name

    def update_floor_list(self, context):
        """
        Update method for the floor list property.
        """
        self["floor_object_name"] = self.floor_object_name

    def object_enum_items(self, context):
        """
        Generate a list of available empty objects in the scene.
        """
        return [(obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == 'EMPTY']

    def floor_enum_items(self, context):
        """
        Generate a list of available mesh objects in the scene.
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
    
    random_seed: bpy.props.IntProperty(
        name="Random Seed",
        default=42,
        description="Seed for Fibonacci offsets and radius randomization"
    )


# Properties for render settings (Now purely Environment/HDRI settings)
class AngleCraftRenderSettings(bpy.types.PropertyGroup):
    """
    Property group for controlling the HDRI automation environment settings.
    """
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

    frames_per_hdri: bpy.props.IntProperty(
        name="Frames per HDRI",
        default=1,
        min=1,
        description="How many frames to stay on one HDRI before switching"
    )

# Properties to control object settings
class AngleCraftRenderButtonSettings(bpy.types.PropertyGroup):
    info_num_cameras: bpy.props.IntProperty(
        name="Number of Cameras",
        default=0,
        description="Number of cameras/renders that will be produced",
        options={'HIDDEN'}  # Hide this property from the UI
    )