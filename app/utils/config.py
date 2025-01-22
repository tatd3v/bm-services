import os

from dotenv import load_dotenv

load_dotenv()

# Youtube Service Config Static Variables

YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3"
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")
