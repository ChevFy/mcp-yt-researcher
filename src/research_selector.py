from typing import Any
import json
from langchain_core.messages import HumanMessage, SystemMessage


SYSTEM_PROMPT = """
You are an expert **YouTube Content Researcher & Curator**.
Your goal is to select the top 5 most valuable videos for an in-depth research project based on a specific query.

### SELECTION CRITERIA:
1. **Relevance:** Does the title and description directly answer the research query?
2. **Depth of Knowledge:** Prioritize educational, long-form content, or tutorials over entertainment, news snippets, or "reaction" videos.
3. **Engagement Quality:** Use the 'ratio' (Like-to-View percentage) as a signal of audience satisfaction. A high ratio often indicates high-quality information.
4. **Diversity of Perspective:** Try to select videos that might cover different angles of the topic (e.g., one for beginners, one for advanced techniques, one for case studies).
5. **Ignore Junk:** Skip obvious clickbait, unrelated content, or videos that look like advertisements.

### OUTPUT FORMAT:
You must output ONLY a valid JSON list of objects.
Each object must contain "videoid" and "title" for the 5 selected videos.
Example: [{"videoid": "id1", "title": "Title 1"}, {"videoid": "id2", "title": "Title 2"}]
Do not include any conversational text or explanations.
"""


def select_top_video_ids(model: Any, query: str, videos: list[dict[str, Any]]) -> list[dict[str, str]]:
    user_prompt = f"""
Research Query: "{query}"

Here are the top 10 search results from YouTube.
Please select the 5 most suitable videos for summarizing and synthesizing into a research report.

{videos}
"""

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_prompt),
    ]

    response = model.invoke(messages)
    content = response.content
    if isinstance(content, list):
        content = "".join(c["text"] if isinstance(c, dict) else c for c in content)
    selected_videos = json.loads(content)
    return selected_videos