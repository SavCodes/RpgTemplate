from PIL import Image, ImageFilter, ImageEnhance

def generate_sway_sheet(file_path, _resize=(32,32)):
    # Load the original image_to_animate image
    image_to_animate = Image.open(file_path)
    image_to_animate = image_to_animate.resize((_resize[0],_resize[1]))
    image_to_animate = image_to_animate.transpose(Image.ROTATE_180)
    # Create a list to store animation frames
    frames = []
    width, height = image_to_animate.size

    # Generate frames with transformations
    for angle in range(-10, 11, 1):  # Sway angles
        # Define a perspective transformation to sway the top
        coeffs = [
            1, angle / 100, 0,  # Top row is skewed => lower denominator = more sway
            0, 1, 0,  # Middle row remains stationary
            0, 0, 1  # Base remains fixed
        ]
        # Apply transformation
        frame = image_to_animate.transform(
            (width, height),
            Image.Transform.PERSPECTIVE,
            coeffs
        )
        frame = frame.transpose(Image.ROTATE_180)
        frames.append(frame)

    # Combine frames into a spritesheet
    spritesheet = Image.new("RGBA", (2 * width * len(frames), height))

    for i, frame in enumerate(frames):
        spritesheet.paste(frame, (i * width, 0))
        spritesheet.paste(frame, ((2* len(frames) - 1  - i) * width, 0))


    # Save the spritesheet
    spritesheet.save(f"{file_path[:file_path.rfind(".", 2)]}_spritesheet_TEST_{2*len(frames)}.png")

def generate_pulsate_sheet(file_path):
    # Load the original image and prepare it
    image_to_animate = Image.open(file_path)
    image_to_animate = image_to_animate.resize((64, 64))  # Resize to standard dimensions
    image_to_animate = image_to_animate.transpose(Image.ROTATE_180)  # Optional transformation

    # Get image dimensions
    width, height = image_to_animate.size

    # Create a list to store animation frames
    frames = []

    # Generate frames with pulsating transformations
    for scale_factor in range(-10, 11, 2):  # Scale factors for pulsation
        scale_factor /= 100  # Convert to a small percentage (e.g., -0.1 to 0.1)
        # Define perspective transformation coefficients for pulsation
        coeffs = [
            1 + scale_factor, 0, -width * scale_factor / 2,  # Horizontal scaling
            0, 1 + scale_factor, -height * scale_factor / 2,  # Vertical scaling
            0, 0, 1  # Perspective remains neutral
        ]
        # Apply transformation
        frame = image_to_animate.transform(
            (width, height),
            Image.Transform.PERSPECTIVE,
            coeffs
        )
        frame = frame.transpose(Image.ROTATE_180)  # Reverse rotation to restore original orientation
        frames.append(frame)

    # Combine frames into a spritesheet
    spritesheet = Image.new("RGBA", (2 * width * len(frames), height))

    for i, frame in enumerate(frames):
        spritesheet.paste(frame, (i * width, 0))
        spritesheet.paste(frame, ((2 * len(frames) - 1 - i) * width, 0))

    # Save the spritesheet
    spritesheet.save(f"{file_path[:file_path.rfind('.', 2)]}_spritesheet_PULSATE_{2 * len(frames)}.png")

def generate_ripple_sheet(file_path):
    # Load the original image and prepare it
    image_to_animate = Image.open(file_path)
    image_to_animate = image_to_animate.resize((64, 64))  # Resize to standard dimensions
    image_to_animate = image_to_animate.transpose(Image.ROTATE_180)  # Optional transformation

    # Get image dimensions
    width, height = image_to_animate.size

    # Create a list to store animation frames
    frames = []

    # Generate frames with pulsating transformations
    for scale_factor in range(-10, 11, 2):  # Scale factors for pulsation
        # Define perspective transformation coefficients for pulsation
        coeffs = [
            1 + scale_factor, 0, 0,  # Stretch horizontally
            0, 1, 0,  # No vertical scaling
            0, 0, 1
        ]
        # Apply transformation
        frame = image_to_animate.transform(
            (width, height),
            Image.Transform.PERSPECTIVE,
            coeffs
        )
        frame = frame.transpose(Image.ROTATE_180)  # Reverse rotation to restore original orientation
        frames.append(frame)

    # Combine frames into a spritesheet
    spritesheet = Image.new("RGBA", (2 * width * len(frames), height))

    for i, frame in enumerate(frames):
        spritesheet.paste(frame, (i * width, 0))
        spritesheet.paste(frame, ((2 * len(frames) - 1 - i) * width, 0))

    # Save the spritesheet
    spritesheet.save(f"{file_path[:file_path.rfind('.', 2)]}_spritesheet_RIPPLE_{2 * len(frames)}.png")

def generate_foggy_aura(file_path, save_name):
    # Load the original image
    original_image = Image.open(file_path).convert("RGBA")

    # Create a blank canvas for the aura effect
    width, height = original_image.size
    aura_canvas = Image.new("RGBA", (width * 3, height * 3), (0, 0, 0, 0))  # Larger canvas for aura spread

    # Place the original image at the center of the canvas
    offset = (width, height)
    aura_canvas.paste(original_image, offset, mask=original_image)

    # Create aura layers
    for i in range(1, 6):  # Increase the number of layers for a thicker aura
        # Blur and scale the image for each layer
        aura_layer = original_image.filter(ImageFilter.GaussianBlur(radius=i * 3))
        scaled_size = (width + i * 20, height + i * 20)  # Incrementally larger sizes
        aura_layer = aura_layer.resize(scaled_size, Image.Resampling.LANCZOS)

        # Reduce opacity for each layer
        aura_layer = ImageEnhance.Brightness(aura_layer).enhance(0.4 / i)

        # Paste the aura layer onto the canvas with transparency
        aura_canvas.paste(aura_layer,
                          (offset[0] - i * 10, offset[1] - i * 10),  # Adjust position to center each layer
                          mask=aura_layer)

    # Add the original image on top of the aura
    aura_canvas.paste(original_image, offset, mask=original_image)

    # Crop or resize the final canvas to the desired size
    final_image = aura_canvas.crop((width // 2, height // 2, width * 2.5, height * 2.5))

    # Save the resulting image
    final_image.resize((32,32))
    final_image.save(save_name)
    print("Foggy aura effect saved!")