# AngleCraft

**AngleCraft** is a powerful Blender add-on designed to simplify the generation of multi-view synthetic data for AI training, 3D modeling, and various other applications. With AngleCraft, you can create sophisticated camera spheres to capture objects from multiple angles, customize render settings, and easily manage environments for seamless data creation.

This tool is ideal for generating datasets for LoRAs (Low-Rank Adaptations) in AI training but is also highly versatile, making it suitable for both AI-related and non-AI applications, such as 3D asset creation, animation, and visual effects.

## Features

### Camera Sphere Generation
Automatically create camera spheres with customizable parameters, including:
- Adjustable radius.
- Horizontal and vertical camera counts.
- Sphere distribution types (e.g., linear, uniform, Fibonacci, weighted).
- Half-sphere support for targeted angle captures.

### Dynamic Object Selection
- **Camera Target:** The camera target is of the type **empty**. Cameras will be created around this empty object, with customizable settings for distance and positioning.
- **Floor Mesh:** This is optional. You can specify a floor mesh to aid in the positioning of cameras, but it is not required.

### Camera Settings
- You can select an existing camera to use as a base for the cameras in your sphere. The selected camera will define properties such as the lens and other settings for all cameras created around the sphere.

### Environment Setup
- HDRI-based lighting with override options. If not overridden, the current world settings will be used.
- Control over HDRI folders and world settings.

### Customizable Render Settings
- Set output directories, resolution, and render samples.
- Denoising options with support for OptiX and Open Image Denoise.

### Streamlined Workflow
Simple UI panels organized for ease of use:
- Object Settings
- Camera Settings
- Camera Sphere Settings
- Environment Settings
- Render Settings

### Batch Rendering
- Automatically render multiple views with a single click.

### Sphere Distribution Types
AngleCraft supports multiple sphere distribution types, tailored for various use cases:
- **Linear:** Cameras are spaced evenly along horizontal and vertical axes.
- **Uniform:** Cameras are distributed evenly across the entire sphere.
- **Fibonacci:** Uses a Fibonacci sequence to create a natural, evenly spaced distribution. Ideal for generating a more organic spread of cameras, avoiding clustering at the poles.
- **80/20 Weighted:** 80% of the cameras are concentrated in the upper hemisphere, and 20% are in the lower hemisphere. This setup is perfect for scenarios where the top view of an object is more critical than the bottom.
- **Equator Dense:** A denser concentration of cameras around the equator, suitable for capturing objects with significant details along the horizontal plane.

## Applications
AngleCraft is versatile and can be used for a wide range of purposes:

### AI Training
- Generate datasets for training LoRAs or other machine learning models.
- Create synthetic data with controlled lighting and camera angles.

### 3D Modeling
- Capture assets from multiple perspectives for presentation or texture baking.

### Animation and Visual Effects
- Design complex camera setups for animations or visual effects production.

### Non-AI Applications
- Generate custom assets for game development, film, and product visualization.

## Installation

1. Go to the [Releases page](https://github.com/glenn-de-backer/anglecraft/releases) and download the latest version of the add-on.
2. Open Blender and navigate to **Edit > Preferences > Add-ons**.
3. Click **Install from Disk** and select the `.zip` file you downloaded from the releases page.
4. Enable the "AngleCraft" add-on in the preferences.
5. The "AngleCraft" tab will appear in the 3D View sidebar (press `N`).

## Usage

1. Open the **AngleCraft** tab in the 3D View sidebar.
2. Set your **Camera Target** (of type **empty**) and optionally, set your **Floor Mesh** in the **Object Settings** panel.
3. Configure your **Camera Sphere Settings**, including the radius, camera count, and distribution type.
4. In the **Camera Settings** panel, you can select an existing camera to use as a base for the cameras in your sphere. The base camera will define properties such as the lens and other settings for the cameras created around the sphere.
5. Adjust **Environment Settings**, such as HDRI lighting. If HDRI is not overridden, the current world settings will be used.
6. **Fine-tune Render Settings**:
    - Set your **output folder** where the rendered images will be stored.
    - Adjust other settings such as resolution and render samples.
7. Use the **Render Panel** to:
    - Create cameras.
    - Delete existing cameras.
    - Start rendering your multi-view data.
8. Check the output directory for rendered images.

## Training is Not Part of This Add-on

It's important to know that **AngleCraft** contains **no AI training logic**. The add-on's primary focus is on generating high-quality multi-view datasets by capturing 3D models from various angles and lighting conditions. 

The images created using AngleCraft are typically used with other tools for AI model training. One such tool I use is **[FluxGym](https://github.com/cocktailpeanut/fluxgym)**, which is designed for managing and processing datasets for AI training. **FluxGym** allows you to efficiently train models using the images generated by AngleCraft.


### Fluxgym example
Below is an example of a dataset processed with **FluxGym** using images created with AngleCraft:

![Flux example](images/flux_example.jpg)

![Flux example2](images/flux_example2.jpg)

For more information on how to use these datasets for training, please check out the [FluxGym repository](https://github.com/cocktailpeanut/fluxgym).

## I'd Love to Know If You're Using AngleCraft!

If you're using **AngleCraft** in your projects, I would absolutely love to hear from you! Whether you're generating data for AI, creating 3D assets, or working on animations, your feedback is invaluable. It also helps me improve the tool.

Feel free to reach out via GitHub issues, or drop me a message with your use case. If you'd like to share examples or tell me how you're using AngleCraft, that would be fantastic!

## License
This project is licensed under the **GNU General Public License v3.0 (GPLv3)**.  
You are free to use, modify, and distribute this software under the terms of the GPLv3 license. For more details, refer to the LICENSE file.

## Contributing
We welcome contributions to AngleCraft!  
Feel free to submit issues, feature requests, or pull requests to help improve this project.

## Acknowledgments
Special thanks to the Blender community for their support and inspiration.

## Donations
I am not seeking monetary compensation for this project. However, if you find AngleCraft useful, I highly encourage you to consider donating to the [Blender Foundation](https://fund.blender.org/). Your support helps ensure the continued development and improvement of Blender, a vital tool for creators worldwide.

## Contact
If you have any questions or suggestions, feel free to reach out via GitHub issues.
