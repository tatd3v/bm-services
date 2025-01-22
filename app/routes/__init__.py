from fastapi import APIRouter
from .youtube import youtube_router
from models import Playlist

router = APIRouter()


router.include_router(youtube_router, prefix="/playlists", tags=["Playlists"])
