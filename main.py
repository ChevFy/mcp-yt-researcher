
from src.env import load_environment, load_youtube_api_key
from src.youtube import build_research_results, fetch_video_details, search_videos


def main():
    load_environment()
    yt_key = load_youtube_api_key()

    search_results = search_videos(
        api_key=yt_key,
        query="how to learn fast",
        max_results=10,
    )
    video_ids = [item["id"]["videoId"] for item in search_results.get("items", [])]
    video_data = fetch_video_details(yt_key, video_ids)
    research_results = build_research_results(video_data)
    sorted_by_likes = sorted(research_results, key=lambda item: item["likes"], reverse=True)

    
    print(sorted_by_likes)
    

if __name__ == "__main__":
    main()