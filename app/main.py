import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.youtube import youtube_router

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")


app = FastAPI(title="Ballroom Medellin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(youtube_router, prefix="/api/v1/youtube")


@app.get("/youtube-info")
async def youtube_info():
    return {
        "api_key": YOUTUBE_API_KEY,
        "channel_id": YOUTUBE_CHANNEL_ID,
    }
