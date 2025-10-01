import numpy as np
from PIL import Image, ImageDraw

def create_halftone_pattern(size, dot_size, angle_deg):
    """Creates a circular halftone pattern tile."""
    # Create a transparent image for the pattern
    pattern_img = Image.new('L', (size, size), 255)  # White background
    draw = ImageDraw.Draw(pattern_img)

    # Calculate dot position
    center = size / 2
    radius = dot_size / 2

    # Draw a black dot in the center
    draw.ellipse((center - radius, center - radius, center + radius, center + radius), fill=0) # Black dot

    # Rotate the pattern
    rotated_pattern = pattern_img.rotate(angle_deg, resample=Image.BICUBIC, expand=True)

    # Crop to original size to make it tileable
    w, h = rotated_pattern.size
    cx, cy = w // 2, h // 2
    crop_size = size

    left = cx - crop_size // 2
    top = cy - crop_size // 2
    right = cx + crop_size // 2
    bottom = cy + crop_size // 2

    return rotated_pattern.crop((left, top, right, bottom))


def generate_mock_manga_page(width=800, height=1200, output_path="demo/mock_manga_page.png"):
    """
    Generates a mock manga page with multiple panels and a halftone effect.
    """
    # Create a white background
    page = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(page)

    # Define panel layouts (x, y, w, h)
    panels = [
        (50, 50, 700, 300),   # Top panel
        (50, 400, 340, 350),  # Middle-left panel
        (410, 400, 340, 350), # Middle-right panel
        (50, 800, 700, 350),  # Bottom panel
    ]

    # Create a halftone texture
    # Using a simple dot pattern for this example
    halftone_tile = create_halftone_pattern(size=20, dot_size=8, angle_deg=45)

    # Create a tiled halftone image large enough to cover the page
    halftone_texture = Image.new('RGB', (width, height))
    for i in range(0, width, halftone_tile.width):
        for j in range(0, height, halftone_tile.height):
            halftone_texture.paste(halftone_tile, (i, j))

    # Draw panels and apply halftone texture
    for (x, y, w, h) in panels:
        # Create a mask for the panel
        panel_mask = Image.new('L', (width, height), 0)
        draw_mask = ImageDraw.Draw(panel_mask)
        draw_mask.rectangle([x, y, x + w, y + h], fill=255)

        # Apply the halftone texture within the panel area
        page.paste(halftone_texture, (0, 0), mask=panel_mask)

        # Draw the black border around the panel
        draw.rectangle([x, y, x + w, y + h], outline='black', width=5)

    # Save the generated page
    page.save(output_path)
    print(f"Mock manga page saved to {output_path}")


if __name__ == "__main__":
    generate_mock_manga_page()