from typing import Any

import requests


SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"


def search_videos(api_key: str, query: str, max_results: int = 10) -> dict[str, Any]:
    params = {
        "maxResults": max_results,
        "part": "snippet",
        "q": query,
        "type": "video",
        "order": "viewCount",
        "videoDuration": "long",
        "key": api_key,
    }
    response = requests.get(SEARCH_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_video_details(api_key: str, video_ids: list[str]) -> dict[str, Any]:
    if not video_ids:
        return {"items": []}

    params = {
        "part": "statistics,snippet",
        "id": ",".join(video_ids),
        "key": api_key,
    }
    response = requests.get(VIDEOS_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def build_research_results(video_data: dict[str, Any]) -> list[dict[str, Any]]:
    research_results: list[dict[str, Any]] = []

    for item in video_data.get("items", []):

        views = int(item["statistics"].get("viewCount", 0))
        likes = int(item["statistics"].get("likeCount", 0))
        ratio = (likes / views * 100) if views > 0 else 0
        research_results.append(
            {
                "videoid": item["id"],
                "title": item["snippet"]["title"],
                "views": views,
                "description": item["snippet"].get("description", ""),
                "likes": likes,
                "ratio": round(ratio, 2),
                "url": f"https://www.youtube.com/watch?v={item['id']}",
            }
        )

    return research_results