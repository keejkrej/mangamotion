import os
import google.generativeai as genai
from PIL import Image
import json

# --- IMPORTANT ---
# Set your Google API Key as an environment variable named 'GOOGLE_API_KEY'
# For example, in your terminal:
# export GOOGLE_API_KEY='YOUR_API_KEY_HERE'
# -----------------

# Load the API key from environment variables
API_KEY = os.getenv("GOOGLE_API_KEY")

def configure_genai():
    """Configures the generative AI model with the API key."""
    if not API_KEY:
        print("="*80)
        print("WARNING: GOOGLE_API_KEY environment variable not found.")
        print("The analysis will proceed with a mock response.")
        print("To use the Gemini API, please set your GOOGLE_API_KEY.")
        print("For example: export GOOGLE_API_KEY='YOUR_API_KEY'")
        print("="*80)
        return False

    try:
        genai.configure(api_key=API_KEY)
        return True
    except Exception as e:
        print(f"Error configuring Google AI: {e}")
        return False

# Flag to check if GenAI is configured
IS_GENAI_CONFIGURED = configure_genai()

def analyze_panel_content(image_path, prompt):
    """
    Analyzes the content of a manga panel using the Google Gemini API.
    If the API key is not configured, it returns a mock response.

    Args:
        image_path (str): The path to the panel image.
        prompt (str): The prompt to guide the analysis.

    Returns:
        dict: A structured dictionary containing the analysis of the panel.
    """
    if not IS_GENAI_CONFIGURED:
        return {
            "scene_description": "Mock response: Gemini API not configured.",
            "characters": ["N/A"],
            "actions": ["N/A"],
            "text_ocr": "Please set your GOOGLE_API_KEY to get a real analysis."
        }

    try:
        # Load the image
        img = Image.open(image_path)

        # Create the model instance
        model = genai.GenerativeModel('gemini-pro-vision')

        # Generate content
        response = model.generate_content([prompt, img], stream=False)

        # Assuming the response is a JSON string, try to parse it
        # This part may need refinement based on the actual model output
        try:
            # The response might be in a markdown block, so we clean it up
            cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
            return json.loads(cleaned_response)
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"Could not parse Gemini response as JSON: {e}")
            return {"error": "Failed to parse response", "raw_response": response.text}

    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return {"error": str(e)}