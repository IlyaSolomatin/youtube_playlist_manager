import re
import pandas as pd
from bs4 import BeautifulSoup

def extract_video_details(html):
    soup = BeautifulSoup(html, 'html.parser')

    title_tag = soup.select_one('a#video-title')
    video_title = title_tag.get('title') if title_tag else None

    video_link = title_tag.get('href') if title_tag else None
    if video_link:
        video_link = f"https://www.youtube.com{video_link}"

    duration_tag = soup.select_one('ytd-thumbnail-overlay-time-status-renderer .badge-shape-wiz__text')
    if duration_tag:
        duration_parts = duration_tag.text.strip().split(':')
        video_duration = sum(int(x) * 60 ** i for i, x in enumerate(reversed(duration_parts)))
    else:
        video_duration = None

    return {
        "title": video_title,
        "link": video_link,
        "duration_seconds": video_duration
    }

f = open("yt_playlist.txt", 'r')
content = f.read()
f.close()

data = []
for i in re.findall("<ytd-playlist-video-renderer.*?<\/ytd-playlist-video-renderer>", content, re.DOTALL):
    data.append(extract_video_details(i))

print(pd.DataFrame(data).sort_values('duration_seconds'))
