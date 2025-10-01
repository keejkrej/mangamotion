from utils import extract_panels
from create_mock_page import generate_mock_manga_page
from content_analysis import analyze_panel_content
import os
import json

# --- IMPORTANT ---
# This script uses the Google Gemini API for content analysis.
# For this to work, you must set your Google API Key as an environment variable
# named 'GOOGLE_API_KEY'.
#
# In your terminal, you can do this by running:
# export GOOGLE_API_KEY='YOUR_API_KEY_HERE'
#
# If the key is not set, the script will fall back to a mock response.
# -----------------

# Define a detailed prompt for the Gemini Vision model
ANALYSIS_PROMPT = """\
Analyze the provided manga panel and return a JSON object with the following structure:
{
  "scene_description": "A detailed, objective description of the scene, setting, and atmosphere.",
  "characters": [
    "A list of characters present in the panel, with brief descriptions of their appearance and expression."
  ],
  "actions": [
    "A list of actions or movements occurring in the panel."
  ],
  "text_ocr": "Any text found in the panel, including dialogue in speech bubbles and sound effects. If no text is present, state 'No dialogue present.'."
}
"""

if __name__ == "__main__":
    print("MangaMotion Demo: Full Pipeline with Gemini API Integration")

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
    print(f"\n--- Step 1: Generating mock manga page ---")
    generate_mock_manga_page(output_path=mock_image_path)

    if not os.path.exists(mock_image_path):
        print(f"Error: Mock page generation failed.")
    else:
        print(f"Mock page successfully created at {mock_image_path}")

        # 2. Extract panels
        print(f"\n--- Step 2: Extracting panels from the mock page ---")
        panel_files = extract_panels(mock_image_path, output_dir=panels_output_dir)

        if panel_files:
            print(f"Successfully extracted {len(panel_files)} panels.")

            # 3. Analyze content of each panel using Gemini API
            print(f"\n--- Step 3: Analyzing content of each panel (using Gemini API if configured) ---")
            for panel_file in panel_files:
                print(f"\nAnalyzing {panel_file}...")
                analysis = analyze_panel_content(panel_file, ANALYSIS_PROMPT)

                # Pretty print the JSON analysis
                print(json.dumps(analysis, indent=2))

            print(f"\n\nDemo complete. Check the '{panels_output_dir}' directory for the extracted panel images.")
        else:
            print("No panels were extracted. Check the extraction logic in utils.py.")