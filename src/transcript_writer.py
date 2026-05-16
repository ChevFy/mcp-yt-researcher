import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import VideoUnavailable, TranscriptsDisabled, NoTranscriptFound
import time

_SKIP_ERRORS = (VideoUnavailable, TranscriptsDisabled, NoTranscriptFound)


def save_transcripts_to_files(selected_videos: list[dict[str, str]]) -> list[str]:
    file_path = []
    os.makedirs("tmp", exist_ok=True)

    for video in selected_videos:
        video_id = video["videoid"]
        title = video["title"]

        transcript_data = None
        for attempt in range(4):
            try:
                transcript_data = YouTubeTranscriptApi().fetch(video_id, languages=["th", "en"]).to_raw_data()
                break
            except _SKIP_ERRORS as e:
                print(f"[{video_id}] skip — {e}")
                break
            except Exception as e:
                wait = 10 * (2 ** attempt)
                print(f"[{video_id}] attempt {attempt+1} failed: {e}. wait {wait}s...")
                time.sleep(wait)

        if transcript_data is None:
            print(f"[{video_id}] skip — all retries exhausted")
            continue

        full_text = f"video id : {video_id}\nTitle : {title}\n\n" + "\n".join([line["text"] for line in transcript_data])

        output_file = f"tmp/{video_id}.txt"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(full_text)

        file_path.append(output_file)
        time.sleep(5)
     

    return file_path


    