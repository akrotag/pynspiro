import requests as req
import json
from random import randint
import os
from data import find_filename


def download_random_video()-> str:
    """
    Downloads a random video from Pexels' API with the tags "nature landscape"
    OUTPUT:
        - 
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

    video_location = find_filename("src/videos", "mp4")

    open(video_location, "wb+").write(vid_req.content)

    return video_location