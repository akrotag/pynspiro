from voices import create_audio
from data import *
from sentences import generate_sentences
from videos import download_random_video
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, ColorClip, ImageClip, AudioFileClip
from moviepy.video.fx.all import crop
import librosa
import time
import os
from PIL import Image
from uploader.upload import upload_video
import random
from keep_alive import keep_alive


VOICE_EN = "en-US-ChristopherNeural"
VOICE_FR = "fr-FR-HenriNeural"



def create_text_img(text, crop_width, h, duration):    
    txt_clip = TextClip(text, fontsize=h*25/1080, color="white", size=(crop_width*.9, h), method="caption").set_duration(duration)
    txt_clip = txt_clip.set_pos("center")
    txt_img_uncropped = find_filename("output/png", "png")
    txt_clip.save_frame(txt_img_uncropped)

    txt_img = Image.open(txt_img_uncropped)
    txt_im_crop = txt_img.crop(txt_img.getbbox())
    txt_img_cropped_loc = find_filename("output/png", "png")
    txt_im_crop.save(txt_img_cropped_loc)

    txt_clip = ImageClip(txt_img_cropped_loc).set_position("center")

    tx_w, tx_h = txt_clip.size

    color_clip = ColorClip(size=(tx_w+50, tx_h+25), color=(0, 0, 0))
    color_clip = color_clip.set_opacity(.8)
    txt_clip = CompositeVideoClip([color_clip, txt_clip]).subclip(0, duration).set_position("center")

    return txt_clip, txt_img_cropped_loc, txt_img_uncropped

def clear():
    locs = ("output/audio/", "output/png/", "src/videos/")
    for l in locs:
        for f in os.listdir(l):
            os.remove(f"{l}{f}")

def create_video(text, voice, output_dir):
    files = []
    audio_loc = create_audio(text, voice)
    files.append(audio_loc)
    duration = librosa.get_duration(filename=audio_loc)

    video_location = download_random_video()
    files.append(video_location)
    clip = VideoFileClip(video_location).subclip(0, duration)

    (w, h) = clip.size
    crop_width = h * 9/16
    x1, x2 = (w - crop_width)//2, (w+crop_width)//2
    y1, y2 = 0, h
    cropped_clip = crop(clip, x1=x1, y1=y1, x2=x2, y2=y2)



    audio = AudioFileClip(audio_loc)

    txt_clip, i1, i2 = create_text_img(text, crop_width, h, duration)
    files.append(i1)
    files.append(i2)
    combined = CompositeVideoClip([cropped_clip, txt_clip])
    combined.audio = audio
    video_filename = find_filename(output_dir, "mp4")
    combined.write_videofile(video_filename)
    cropped_clip.close()
    txt_clip.close()
    combined.close()
    
    return video_filename

keep_alive()

while True:
    sentences = generate_sentences()
    for s in sentences:
        vid = create_video(s, VOICE_EN, "output/video/en")
        upload_video(filename=vid, description="Don't forget to follow for more #motivation #inspiration", cookies="src/cookies.txt")
        os.remove(vid)
        time.sleep(random.randint(30000, 40000))

#create_video("Le succès n'est pas la clé du bonheur. Le bonheur est la clé du succès. Si vous aimez ce que vous faites, vous réussirez.", VOICE_FR, "output/video/fr")
clear()