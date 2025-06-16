import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.utils.database import get_db
from app.routes.youtube import youtube_router

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")

if not YOUTUBE_API_KEY or not YOUTUBE_CHANNEL_ID:
    raise RuntimeError(
        "Missing required environment variables: YOUTUBE_API_KEY or YOUTUBE_CHANNEL_ID"
    )

app = FastAPI(
    title="Ballroom Medellin API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

ENV = os.getenv("ENV", "development")

ALLOWED_ORIGINS = [
    "https://www.ballroomedellin.com",
    "https://dev.ballroomedellin.com",
    "http://localhost",
    "http://localhost:5173",
    "https://localhost:5173",
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
            status_code=500, detail="Missing YouTube channel configuration."
        )

    return {"channel_id": YOUTUBE_CHANNEL_ID}


@app.get("/calendar-events")
async def calendar_events(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute("SELECT 1")
        return {"status": "Database connection successful"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database connection failed")
