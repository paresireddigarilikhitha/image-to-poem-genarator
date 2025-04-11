import gradio as gr
import google.generativeai as genai
import base64
from io import BytesIO
from PIL import Image

# Set up Google GenAI API Key
genai.configure(api_key="AIzaSyAVN_-mzCpydnDzIrsnDT31zL8bSg1ezzc")

# Supported languages for translation
LANGUAGES = ["Telugu", "Hindi", "Tamil", "Kannada", "Malayalam", "Bengali", "Gujarati", "Marathi", "Punjabi", "Odia"]

def image_to_poem(image, target_language):
    """Generates one English poem and its translation from an image into the selected language."""

    try:
        # Convert image to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        image_b64 = base64.b64encode(img_bytes).decode('utf-8')

        # Load Gemini model
        model = genai.GenerativeModel("gemini-1.5-pro")

        # Step 1: Describe the image
        description_prompt = "Describe this image briefly in one sentence."
        description_response = model.generate_content([
            {"mime_type": "image/png", "data": image_b64},
            description_prompt
        ])
        description = description_response.text.strip()

        # Step 2: Generate a short English poem
        poem_prompt = f"Based on this image description: '{description}', write a short 4-line poem in English."
        poem_response = model.generate_content(poem_prompt)
        english_poem = poem_response.text.strip()

        # Step 3: Translate the poem into selected language
        translate_prompt = (
            f"Translate the following English poem into {target_language}. "
            f"Only return the translated poem — do not include English:\n\n{english_poem}"
        )
        translation_response = model.generate_content(translate_prompt)
        translated_poem = translation_response.text.strip()

        return f"{english_poem}\n\n{translated_poem}"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Gradio Interface
interface = gr.Interface(
    fn=image_to_poem,
    inputs=[
        gr.Image(type="pil", label="Upload an Image"),
        gr.Dropdown(choices=LANGUAGES, label="Choose Translation Language", value="Tamil")
    ],
    outputs=gr.Textbox(label="Poem (English + Translation)"),
    title="AI-Powered Poem Generator",
    description="Upload an image. The AI will create a short English poem and translate it into the selected Indian language."
)

if __name__ == "__main__":
    interface.launch()
