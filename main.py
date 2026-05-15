
from src.env import load_environment, load_youtube_api_key
from src.research_selector import select_top_video_ids
from src.youtube import build_research_results, fetch_video_details, search_videos
from langchain_google_genai import ChatGoogleGenerativeAI



def main():
    load_environment()
    yt_key = load_youtube_api_key()
    query = "how to learn fast"

    search_results = search_videos(
        api_key=yt_key,
        query=query,
        max_results=10,
    )
    video_ids = [item["id"]["videoId"] for item in search_results.get("items", [])]
    video_data = fetch_video_details(yt_key, video_ids)
    research_results = build_research_results(video_data)
    sorted_by_likes = sorted(research_results, key=lambda item: item["likes"], reverse=True)
    
    print(sorted_by_likes)

    model = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
    video_ids = select_top_video_ids(model=model, query=query, videos=sorted_by_likes)
    print(video_ids)

    
    
    
    

    

if __name__ == "__main__":
    main()