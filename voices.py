from data import *
import edge_tts
import asyncio
import os

#fr: fr-FR-HenriNeural
#en: en-US-ChristopherNeural
TEXT = "Believe in yourself, and all that you are. Know that there is something inside you that is greater than any obstacle."
VOICE = "en-US-ChristopherNeural"
output = "output/audio/001.mp3"

async def save_voice(text, voice) -> None:
    """Main function"""
    communicate = edge_tts.Communicate(text, voice)
    output = find_filename("output/audio", "wav")
    await communicate.save(output)
    return output


def create_audio(text, voice):
    #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    out = asyncio.run(save_voice(text, voice))
    """loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        out = loop.run_until_complete(save_voice(text, voice))
    finally:
        loop.close()"""
    return out
