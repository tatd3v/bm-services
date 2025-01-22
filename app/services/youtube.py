import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Any

from app.utils import (
    YOUTUBE_API_KEY,
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    YOUTUBE_CHANNEL_ID,
)

logger = logging.getLogger(__name__)


class YoutubeService:
    def __init__(self):
        if not YOUTUBE_API_KEY or not YOUTUBE_CHANNEL_ID:
            raise ValueError("YOUTUBE_API_KEY and YOUTUBE_CHANNEL_ID must be set.")

        try:
            self.youtube = build(
                YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=YOUTUBE_API_KEY,
            )
        except HttpError as e:
            logger.error(f"Failed to initialize the YouTube API client: {e}")
            raise

    def fetch_playlists(self) -> List[Dict[str, Any]]:
        try:
            response = (
                self.youtube.playlists()
                .list(part="snippet", channelId=YOUTUBE_CHANNEL_ID, maxResults=50)
                .execute()
            )
            return response.get("items", [])
        except HttpError as e:
            logger.error(f"Error fetching playlists: {e}")
            return []

    def fetch_videos_for_playlist(self, playlist_id: str) -> List[Dict[str, Any]]:
        try:
            response = (
                self.youtube.playlistItems()
                .list(part="snippet", playlistId=playlist_id, maxResults=50)
                .execute()
            )
            return [
                {
                    "videoId": item["snippet"]["resourceId"]["videoId"],
                    "title": item["snippet"]["title"],
                }
                for item in response.get("items", [])
            ]
        except HttpError as e:
            logger.error(f"Error fetching videos for playlist {playlist_id}: {e}")
            return []

    def fetch_playlists_with_videos(self) -> List[Dict[str, Any]]:
        playlists = self.fetch_playlists()

        if not playlists:
            logger.warning("No playlists found for the specified channel.")
            return []

        result = []
        for playlist in playlists:
            playlist_id = playlist["id"]
            playlist_title = playlist["snippet"]["title"]

            videos = self.fetch_videos_for_playlist(playlist_id)
            result.append(
                {
                    "id": playlist_id,
                    "title": playlist_title,
                    "videos": videos,
                }
            )
        return result
