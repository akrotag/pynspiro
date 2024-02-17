from files import *
import edge_tts
import asyncio

#fr: fr-FR-HenriNeural
#en: en-US-ChristopherNeural
#VOICE = "en-US-ChristopherNeural"


async def save_voice(text: str, voice: str, path: str) -> None:
    """
    INPUT:
        text: str - text to be read
        voice: str - voice that will read the give text (type "edge-tts --list-voices" in a terminal to see available presets, use ShortName)
        path: str - directory to which the audio will be saved
    OUTPUT:
        str - path of the generated audio of the chosen voice reading the given text
    """
    communicate = edge_tts.Communicate(text, voice)
    output = find_filename(path, "wav")
    await communicate.save(output)
    return output


def create_audio(text: str, voice: str, path: str):
    """
    INPUT:
        text: str - text to be read
        voice: str - voice that will read the give text (type "edge-tts --list-voices" in a terminal to see available presets, use ShortName)
        path: str - directory to which the audio will be saved
    OUTPUT:
        str - path of the generated audio of the chosen voice reading the given text
    """
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    output = asyncio.run(save_voice(text, voice, path))
    return output
