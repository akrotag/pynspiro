from uploader.upload import upload_video, upload_videos
from uploader.auth import AuthBackend

# single video
upload_video('001.mp4', 
            description='this is my description', 
            cookies='cookies.txt')
