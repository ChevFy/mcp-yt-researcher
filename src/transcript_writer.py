import os
from typing import Any
from youtube_transcript_api import YouTubeTranscriptApi

def save_transcripts_to_files(selected_videos: list[dict[str, str]]) -> None:
    yt = YouTubeTranscriptApi()
    file_path = []
    os.makedirs("tmp", exist_ok=True)

    for video in selected_videos:
        transcript = yt.fetch(video_id=video["videoid"], languages=["th", "en"])
        full_text =  f"video id : {video["videoid"]}\nTitle : {video["title"]}\n\n"+ "\n".join([line.text for line in transcript])
        with open(f"tmp/{video['videoid']}.txt", "w") as file:
            file.write(full_text)
            file_path.append(f"tmp/{video['videoid']}.txt")

    return file_path