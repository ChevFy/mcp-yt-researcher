
from src.env import load_environment, load_youtube_api_key
from src.research_selector import select_top_video_ids
from src.transcript_writer import save_transcripts_to_files
from src.youtube import build_research_results, fetch_video_details, search_videos
from langchain_google_genai import ChatGoogleGenerativeAI
from fastmcp import FastMCP
import shutil
import os

mcp = FastMCP()


@mcp.tool("generate_transcripts", description="Fetch transcripts for selected videos and save files to tmp. Returns list of file paths.")
def main(q : str):
    """Orchestrate YouTube search, selection and transcript export.

    Args:
        q (str): Search query string used to find relevant YouTube videos
            (e.g., "how to learn fast"). This parameter is passed to the
            YouTube search helper and drives which videos are fetched.

    Returns:
        dict: On success returns `{"status": "ok", "files": [...]}`.
            On partial success returns `{"status": "partial", "files": [...], "errors": [...]}`.
    """
    load_environment()
    yt_key = load_youtube_api_key()
    query = q

    search_results = search_videos(
        api_key=yt_key,
        query=query,
        max_results=10,
    )
    video_ids = [item["id"]["videoId"] for item in search_results.get("items", [])]
    video_data = fetch_video_details(yt_key, video_ids)
    research_results = build_research_results(video_data)
    sorted_by_likes = sorted(research_results, key=lambda item: item["likes"], reverse=True)
    

    model = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
    selected_videos = select_top_video_ids(model=model, query=query, videos=sorted_by_likes)
    print(selected_videos)
    file_paths  = save_transcripts_to_files(selected_videos)

    return {"files": file_paths}



@mcp.tool("cleanup_tmp", description="Remove the tmp directory and all its contents. Safe to call repeatedly.")
def remove_tmp():
    """Remove the `tmp` directory created by the toolset.
    Returns a dict describing outcome.
    """
    try:
        if os.path.exists("tmp"):
            shutil.rmtree("tmp")
            return {"deleted": True}
        return {"deleted": False, "reason": "not found"}
    except Exception as e:
        return {"deleted": False, "reason": str(e)}

    
if __name__ == "__main__":
    main("how to learn fast 2026")