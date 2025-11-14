import spacy
nlp = spacy.load("en_core_web_sm")

import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import io, base64
from evaluate import load

# Load model and processor once when the backend starts
print("Loading BLIP model...")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
model.eval()
print("Model loaded successfully.")

# Load the BERTScore metric
bertscore = load("bertscore")


def decode_image(image_base64):
    """Decode base64 image to a PIL image."""
    try:
        if not image_base64:
            return None
        # Remove base64 header if present
        if "," in image_base64:
            image_base64 = image_base64.split(",", 1)[1]
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        return image
    except Exception as e:
        print("Image decode failed:", e)
        return None


def generate_title(story_text, image_base64=None, reference_title=None):
    """
    Generate a contextual title using BLIP (requires image input).
    Uses NLP to extract key phrases from story for better multimodal grounding.
    """
    image = decode_image(image_base64)
    if image is None:
        raise ValueError("BLIP requires an image for contextual title generation.")

    # --- Step 1: Extract key entities & adjectives from story ---
    doc = nlp(story_text)
    keywords = []
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN", "ADJ"]:
            keywords.append(token.text)
    short_context = " ".join(keywords[:25])  # limit to 25 important words

    # --- Step 2: Give BLIP a clear caption-style prompt ---
    prompt = (
        f"Story keywords: {short_context}. "
        f"Generate a short, meaningful and creative title summarizing this story."
    )

    # --- Step 3: Generate title ---
    inputs = processor(image, prompt, return_tensors="pt")
    output_ids = model.generate(
        **inputs,
        max_new_tokens=20,
        num_beams=8,
        temperature=0.7,
        repetition_penalty=1.2
    )

    # --- Step 4: Decode and clean output ---
    generated_text = processor.decode(output_ids[0], skip_special_tokens=True).strip()

    # Clean filler phrases
    for token in ["Story Keywords:", "Generate", "Title:", "Context:", "Keywords:", "Story"]:
        generated_text = generated_text.replace(token, "").strip()

    # Capitalize
    generated_text = generated_text.title()
    generated_text = " ".join(generated_text.split()[:8])

    # --- Step 5: Compute BERTScore ---
    if not reference_title:
        raise ValueError("Reference title is required for BERTScore.")

    bert_res = bertscore.compute(predictions=[generated_text], references=[reference_title], lang="en")
    result = {
        "generated_title": generated_text,
        "bertscore": round(bert_res["f1"][0], 4)
    }

    print(f"[DEBUG] Final Title: {generated_text} | BERTScore: {result['bertscore']}")
    return result
