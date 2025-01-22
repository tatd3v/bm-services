from fastapi import APIRouter, HTTPException
from typing import List

from app.services.youtube import YoutubeService
from models import Playlist

youtube_router = APIRouter()


@youtube_router.get("/", response_model=List[Playlist])
async def get_playlists_with_videos():
    youtube_service = YoutubeService()

    try:
        playlists = youtube_service.fetch_playlists_with_videos()
        if not playlists:
            raise HTTPException(status_code=404, detail="Playlists not found")
        return playlists
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
