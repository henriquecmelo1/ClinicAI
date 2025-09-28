import requests
import os
from dotenv import load_dotenv

import aiofiles
import whisper

from .message_handler import handle_message

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


async def audio_handler(message: dict):
    audio_info = message.get("audio", {})
    audio_id = audio_info.get("id")

    sender_id = message.get("from")
    # Get the audio URL and MIME type
    audio_url = await get_audio_url(audio_id)
    if audio_url:
        audio_path = await download_audio(audio_url)
        if audio_path:
            transcription = await transcribe_audio(audio_path)
            await handle_message({"from": sender_id, "text": {"body": transcription}, "type": "text"})
            return transcription
        
    return None

async def get_audio_url(audio_id: str):
    url = f"https://graph.facebook.com/v13.0/{audio_id}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will raise an exception for bad responses (4xx or 5xx)
        
        audio_data = response.json()
        audio_url = audio_data.get("url")
        
        return audio_url
    
    except requests.exceptions.RequestException as e:
        print(f"Error getting audio URL: {e}")
        return None
    
async def download_audio(audio_url: str):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    # 1. Define the directory where you want to save the files
    save_directory = "whatsapp_audio_files"
    
    # 2. Create the directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
        print(f"Created directory: {save_directory}")

    try:
        response = requests.get(audio_url, headers=headers)
        response.raise_for_status()

        file_name = f"audio_message.mp3"
        
        # 3. Construct the full path to the file
        full_path = os.path.join(save_directory, file_name)
        
        # 4. Use the full path with the async file handler
        async with aiofiles.open(full_path, "wb") as audio_file:
            await audio_file.write(response.content)

            return full_path

        # print(f"Successfully saved audio to: {full_path}")
        # transcription = await transcribe_audio(full_path)
        # await handle_message({"type": "text", "text": {"body": transcription}})


    except requests.exceptions.RequestException as e:
        print(f"Failed to download audio: {e}")
        return None
    

async def transcribe_audio(file_path: str):

    model = whisper.load_model("base")  # for english use .en (translation is better)
    result = model.transcribe(file_path, language="pt", fp16=False)
    print(f"Transcription: {result['text']}")
    return result["text"]