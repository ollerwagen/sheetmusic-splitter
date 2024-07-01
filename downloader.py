import sys

from pytube import YouTube
from urllib.parse import urlparse, parse_qs

def download(url: str):    
    video_id = ytid(url)

    yt = YouTube(url)
    stream = get_best_stream(yt)
    stream.download(output_path='downloads', filename=f'{video_id}.mp4', skip_existing=True)

def ytid(url: str) -> str:
    parsed_url = urlparse(url)
    qparams = parse_qs(parsed_url.query)

    vid = qparams.get('v')
    if vid:
        return vid[0]
    else:
        return parsed_url.path.split('/')[-1]

def get_best_stream(yt: YouTube):
    streams = yt.streams
    return streams.order_by('resolution').filter(file_extension='mp4').last()
