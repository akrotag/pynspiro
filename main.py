from sentences import generate_sentences
from videos import create_video
from files import clear



VOICE_EN = "en-US-ChristopherNeural"
VOICE_FR = "fr-FR-HenriNeural"
directories = ("output/audio/", "output/png/", "src/videos/")
    
#clears the output folder and generates 3 motivational videos
if(__name__ == '__main__'):
    sentences = generate_sentences()
    for s in sentences:
        vid = create_video(s, VOICE_EN, "output/video/en")
        clear(directories)
