from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Any

from app.utils import (
    YOUTUBE_API_KEY,
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    YOUTUBE_CHANNEL_ID,
)


class YoutubeService:
    def __init__(self):
        try:
            self.youtube = build(
                YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=YOUTUBE_API_KEY,
            )
        except HttpError as e:
            print(f"An error occurred while initializing the YouTube API client: {e}")
            raise

    def fetch_playlists(self) -> List[Dict]:
        try:
            playlists_request = self.youtube.playlists().list(
                part="snippet", channelId=YOUTUBE_CHANNEL_ID
            )
            playlists_response = playlists_request.execute()
            return playlists_response.get("items", [])
        except HttpError as e:
            logger.error(f"Error fetching playlists: {e}")
            return []

    def fetch_videos_for_playlist(self, playlist_id: str) -> List[Dict]:
        try:
            videos_request = self.youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
            )
            videos_response = videos_request.execute()
            return [
                {
                    "videoId": item["snippet"]["resourceId"]["videoId"],
                    "title": item["snippet"]["title"],
                }
                for item in videos_response.get("items", [])
            ]
        except HttpError as e:
            logger.error(f"Error fetching videos for playlist {playlist_id}: {e}")
            return []

    def fetch_playlists_with_videos(self) -> List[Dict]:
        playlists = self.fetch_playlists()  # Get playlists with their snippets

        if not playlists:
            logger.warning("No playlists found for the specified channel.")
            return []

        result = []
        for playlist in playlists:
            playlist_id = playlist["id"]
            playlist_title = playlist["snippet"]["title"]  # Get the title from snippet

            videos = self.fetch_videos_for_playlist(playlist_id)
            result.append(
                {
                    "id": playlist_id,
                    "title": playlist_title,  # Store playlist title
                    "videos": videos,
                }
            )
        return result
