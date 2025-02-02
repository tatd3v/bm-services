import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes.youtube import youtube_router

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")

if not YOUTUBE_API_KEY or not YOUTUBE_CHANNEL_ID:
    raise ValueError(
        "Missing required environment variables: YOUTUBE_API_KEY or YOUTUBE_CHANNEL_ID"
    )

app = FastAPI(title="Ballroom Medellin API")

ENV = os.getenv("ENV", "development")

ALLOWED_ORIGINS = (
    [
        "https://www.ballroomedellin.com",
        "https://development.ballroomedellin.com",
    ]
    if ENV == "production"
    else [
        "http://localhost",
        "http://localhost:5173",
        "https://localhost",
    ]
)


if os.getenv("ENV") == "production":
    origins = [
        "https://www.ballroomedellin.com",
        "https://development.ballroomedellin.com",
    ]
else:
    origins = [
        "http://localhost",
        "http://localhost:5173",
        "https://localhost",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(youtube_router, prefix="/api/v1/youtube")


@app.get("/youtube-info", response_model=dict)
async def youtube_info():
    if not YOUTUBE_CHANNEL_ID:
        raise HTTPException(
            status_code=500, detail="Falta la configuración del canal de YouTube."
        )

    return {"channel_id": YOUTUBE_CHANNEL_ID}
