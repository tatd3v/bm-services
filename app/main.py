import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.youtube import youtube_router

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")


app = FastAPI(title="Ballroom Medellin API")

origins = [
    "http://localhost:5173",
    "https://ballroomedellin.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    print("Response Headers:", response.headers)
    return response


app.include_router(youtube_router, prefix="/api/v1/youtube")


@app.get("/youtube-info")
async def youtube_info():
    return {
        "api_key": YOUTUBE_API_KEY,
        "channel_id": YOUTUBE_CHANNEL_ID,
    }
