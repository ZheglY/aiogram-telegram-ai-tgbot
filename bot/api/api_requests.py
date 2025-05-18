from bot.config.bot_config import MISTRAL_AI_TOKEN
from mistralai import Mistral
import logging
from googletrans import Translator


logger = logging.getLogger("bot_logger")


async def text_generation_request(request: str):
    """
    Sends a text generation request to the Mistral model using API.

    Args:
        request (str): The user prompt to send to the model.

    Returns:
        str: The generated text. Returns an error message if the response is empty.
    """
    model = "mistral-large-latest"
    client = Mistral(api_key=MISTRAL_AI_TOKEN)

    response = await client.chat.stream_async(
        model=model,
        messages=[
            {
                "role": "user",
                "content": request,
            },
        ],
    )

    full_text = ""
    async for chunk in response:
        delta = chunk.data.choices[0].delta
        if delta.content:
            logger.info(f"📦 Received fragment: {delta.content}")
            full_text += delta.content

    if full_text:
        logger.info(f"🟢 Final answer: {full_text}")
        return full_text
    else:
        logger.error(f"❌ Nothing generated.")
        return "Error: empty response"


async def google_translator(text: str, language: str):
    """
    Sends a text generation request to the Google translator API.

    Args:
        text (str): The user prompt to send to the model.
        language(str): Language from which the request will be translated to English

    Returns:
        str: The translated text. Returns an error message if the response is empty.
    """
    translator = Translator()
    translated_text = await translator.translate(text, src=language, dest='en')
    return translated_text.text