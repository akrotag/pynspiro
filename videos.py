import requests as req
import json
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip, ImageClip, AudioFileClip
from moviepy.video.fx.all import crop
import librosa
from PIL import Image
from random import randint
from files import find_filename
from voices import create_audio


def download_random_video(path: str)-> str:
    """
    INPUT:
        path: str - Path to which the video will be saved
    OUTPUT:
        str - Video file path
    Downloads a random video from Pexels' API with the tags "nature landscape"
    """
    headers = {"Authorization": "y1NkY5u0XbVCKWTPTYlw1Uzmkrjx1jNNkPn59O16MZCxQfhuzLYzexCk"}

    resp = req.get("https://api.pexels.com/videos/search?query=nature%20landscape&size=medium&per_page=80&orientation=landscape", headers=headers)
    resp_json = json.loads(resp.text)['videos']

    video = resp_json[randint(0, len(resp_json)-1)]['video_files']
    for vid in video:
        if vid['width'] >=1920:
            video = vid
            break
    vid_req = req.get(video['link'])

    video_location = find_filename(path, "mp4")

    open(video_location, "wb+").write(vid_req.content)

    return video_location



def create_text_video(text: str, width: int, height: int, duration: int, path: str) -> CompositeVideoClip:
    """
    INPUT:
        text: str - Text that will be on the video
        width: int - width of the output 
        height: int - height of the output 
        duration: int - duration of the ouput
        path: str - path to which the images created in the process will be saved
    OUTPUT:
        moviepy.editor.CompositeVideoClip - Clip to be used in the editing of another video
        
    """
    txt_clip = TextClip(text, fontsize=height*25/1080, color="white", size=(width*.9, height), method="caption").set_duration(duration)
    txt_clip = txt_clip.set_pos("center")
    txt_img_uncropped = find_filename(path, "png")
    txt_clip.save_frame(txt_img_uncropped)

    txt_img = Image.open(txt_img_uncropped)
    txt_im_crop = txt_img.crop(txt_img.getbbox())
    txt_img_cropped_loc = find_filename(path, "png")
    txt_im_crop.save(txt_img_cropped_loc)

    txt_clip = ImageClip(txt_img_cropped_loc).set_position("center")

    tx_w, tx_h = txt_clip.size

    color_clip = ColorClip(size=(tx_w+50, tx_h+25), color=(0, 0, 0))
    color_clip = color_clip.set_opacity(.8)
    txt_clip = CompositeVideoClip([color_clip, txt_clip]).subclip(0, duration).set_position("center")

    return txt_clip

def create_video(text: str, voice: str, output_dir: str):
    """
    INPUT:
        text: str - text to be generated and read on the video
        voice: str - voice preset to be used (type "edge-tts --list-voices" in a terminal to see available presets, use ShortName)
        output_dir: str - directory to which the newly generated video will be saved
    OUTPUT:
        str - path of the generated video of the given voice reading the given text on a landscape video background
    """

    audio_loc = create_audio(text, voice, "output/audio")

    duration = librosa.get_duration(path=audio_loc)

    video_location = download_random_video("src/videos")

    clip = VideoFileClip(video_location).subclip(0, duration)

    (w, h) = clip.size
    crop_width = h * 9/16
    x1, x2 = (w - crop_width)//2, (w+crop_width)//2
    y1, y2 = 0, h
    cropped_clip = crop(clip, x1=x1, y1=y1, x2=x2, y2=y2)



    audio = AudioFileClip(audio_loc)

    txt_clip= create_text_video(text, crop_width, h, duration, "output/png")

    combined = CompositeVideoClip([cropped_clip, txt_clip])
    combined.audio = audio
    video_filename = find_filename(output_dir, "mp4")
    combined.write_videofile(video_filename)
    cropped_clip.close()
    txt_clip.close()
    combined.close()
    
    return video_filename
