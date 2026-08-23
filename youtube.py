from datetime import datetime, timezone, timedelta
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

from helper import YOUTUBE_API_KEY


def _get_youtube():
    if not YOUTUBE_API_KEY:
        raise RuntimeError("YOUTUBE_API_KEY not set in .env")
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def get_channel_id(handle: str):
    response = _get_youtube().search().list(
        part="snippet", q=handle, type="channel", maxResults=1
    ).execute()
    return response["items"][0]["snippet"]["channelId"]


def get_channel_videos(channel_id: str, max_results: int = 10):
    response = _get_youtube().search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=max_results,
        order="date",
        type="video",
    ).execute()

    return [
        {
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "published_at": item["snippet"]["publishedAt"],
            "thumbnail_url": f"https://img.youtube.com/vi/{item['id']['videoId']}/hqdefault.jpg",
        }
        for item in response["items"]
    ]


def search_channel_videos(channel_id: str, query: str, max_results: int = 10):
    response = _get_youtube().search().list(
        part="snippet",
        channelId=channel_id,
        q=query,
        type="video",
        maxResults=max_results,
    ).execute()

    return [
        {
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "published_at": item["snippet"]["publishedAt"],
            "thumbnail_url": f"https://img.youtube.com/vi/{item['id']['videoId']}/hqdefault.jpg",
        }
        for item in response["items"]
    ]


def get_todays_videos(channel_name: str, hours: int = 30):
    channel_id = get_channel_id(channel_name)
    videos = get_channel_videos(channel_id, max_results=10)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)

    return [
        v for v in videos
        if datetime.fromisoformat(v["published_at"].replace("Z", "+00:00")) > cutoff
    ]


def get_transcript(video_id: str) -> str:
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    return "\n".join(snippet.text for snippet in transcript)
