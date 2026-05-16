import os
from typing import Any
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig
from youtube_transcript_api.proxies import WebshareProxyConfig
from requests import Session
import certifi
def save_transcripts_to_files(selected_videos: list[dict[str, str]]) -> list[str]:
    file_path = []
    http_client = Session()
    http_client.headers.update({"Accept-Encoding": "gzip, deflate"})
    http_client.verify = certifi.where()
    
    os.makedirs("tmp", exist_ok=True)
    
    proxy_config = WebshareProxyConfig(
           proxy_username="kwufmbbg",
           proxy_password="qvakl1le04cn" ,
    )
    ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config,http_client=http_client)

    for video in selected_videos:
        video_id = video["videoid"]
        title = video["title"]
        transcript_data = ytt_api.fetch(video_id, languages=["th", "en"]).to_raw_data()
            
        full_text = f"video id : {video_id}\nTitle : {title}\n\n" + "\n".join([line["text"] for line in transcript_data])
            
        output_file = f"tmp/{video_id}.txt"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(full_text)
                
        file_path.append(output_file)
            
     

    return file_path