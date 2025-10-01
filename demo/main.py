from utils import extract_panels
from create_mock_page import generate_mock_manga_page
import os

if __name__ == "__main__":
    print("MangaMotion Demo: Generating mock page and extracting panels...")

    # Define paths
    output_dir = "demo/generated_output"
    mock_image_path = os.path.join(output_dir, "mock_manga_page.png")
    panels_output_dir = os.path.join(output_dir, "extracted_panels")

    # Create output directories if they don't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(panels_output_dir):
        os.makedirs(panels_output_dir)

    # 1. Generate the mock manga page
    print(f"\nStep 1: Generating mock manga page at {mock_image_path}")
    generate_mock_manga_page(output_path=mock_image_path)

    # Check if the image was created
    if not os.path.exists(mock_image_path):
        print(f"Error: Mock page generation failed. File not found at {mock_image_path}")
    else:
        print("\nStep 2: Extracting panels from the mock page...")
        # 2. Call the extraction function
        panel_files = extract_panels(mock_image_path, output_dir=panels_output_dir)

        if panel_files:
            print(f"\nSuccessfully extracted {len(panel_files)} panels:")
            for panel_file in panel_files:
                print(f"- {panel_file}")
            print(f"\nDemo complete. Check the '{panels_output_dir}' directory for the output.")
        else:
            print("No panels were extracted. Check the extraction logic in utils.py.")