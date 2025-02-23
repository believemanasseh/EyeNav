import torch
from transformers import LlavaNextForConditionalGeneration, LlavaNextProcessor

# Load the processor and model
model_path = "ibm-granite/granite-vision-3.1-2b-preview"
processor = LlavaNextProcessor.from_pretrained(model_path)

model = LlavaNextForConditionalGeneration.from_pretrained(
    model_path, use_safetensors=True, weights_only=True
).to("cuda" if torch.cuda.is_available() else "cpu")

# processor = AutoProcessor.from_pretrained(
#     "ibm-granite/granite-vision-3.1-2b-preview", cache_dir=os.environ["HF_HOME"]
# )


def interpret_gaze(coordinates: dict[str, float]):
    """
    Interprets gaze data using IBM Granite Vision Model.
    """
    system_prompt = "System Prompt: You are to determine the user intent given the gaze coordinates (x, y). Intents include scrolling up or down. Keep answer as precise as possible (e.g. 'up' or 'down')"

    user_prompt = f"User Prompt: Gaze coordinates: x=({coordinates['x']})), y=({coordinates['y']}). Interpret the user's intent."

    conversation = [
        {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_prompt},
            ],
        },
    ]
    inputs = processor.apply_chat_template(
        conversation,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to("cuda")

    # autoregressively complete prompt
    output = model.generate(**inputs, max_new_tokens=100)

    response = processor.decode(output[0], skip_special_tokens=True)
    return response
