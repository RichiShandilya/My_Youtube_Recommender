from dotenv import load_dotenv
import os
import requests
import pandas as pd
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv("YT_API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)


# 🔹 1. Normal search ke liye
def fetch_youtube_videos(query, max_results=10):
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results
    )
    response = request.execute()

    videos = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        videos.append({
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "thumbnail": item["snippet"].get("thumbnails", {}).get("medium", {}).get("url"),
            "video_url": f"https://www.youtube.com/watch?v={video_id}",
        })
    return pd.DataFrame(videos)


# 🔹 2. Trending ke liye
def fetch_trending_videos(max_results=10, region_code="IN"):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet",
        "chart": "mostPopular",
        "regionCode": region_code,
        "maxResults": max_results,
        "key": API_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()

    videos = []
    for item in data.get("items", []):
        video_id = item["id"]
        videos.append({
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "thumbnail": item["snippet"]["thumbnails"].get("medium", {}).get("url"),
            "video_url": f"https://www.youtube.com/watch?v={video_id}",
        })
    return pd.DataFrame(videos)
