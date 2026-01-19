import os
from yt_dlp import *

URL = input("youtube URL> ")
# URL = """
# https://youtu.be/Wlmp9HvxXVU?si=eRcDn9Qd0b5P2bG_
# """

def download(url, output_dir="."):
    """
    download youtube video
    """
    file_name = "%(title)s.%(ext)s"
    
    ydl_opts = {
        "outtmpl": f"{output_dir}/{file_name}",
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "noplaylist": True
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
    print(f"successfully downloaded {file_name}")
        

download(URL, "./vid_samples")