from diffusers import StableDiffusionPipeline
import torch
from bot.config.bot_config import HUGGING_FACE_TOKEN


async def generate_picture(prompt: str, user_id: int):
    """
    Generates an image using Stable Diffusion based on the given prompt and saves it to disk.

    Args:
        prompt (str): The text prompt describing the image to generate.
        user_id (int): The Telegram user ID, used to name the output file.

    Returns:
        Optional[str]: The path to the saved image, or None if generation failed.
    """
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16,
        use_auth_token=HUGGING_FACE_TOKEN
    )

    pipe = pipe.to("cuda")
    image = pipe(prompt, num_inference_steps=30).images[0]
    image.save(f"bot/generation/images/generated_picture_{user_id}.png")

    return f"bot/generation/images/generated_picture_{user_id}.png"



