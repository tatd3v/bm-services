from pydantic import BaseModel
from typing import List


class Video(BaseModel):
    title: str
    videoId: str


class Playlist(BaseModel):
    id: str
    title: str
    videos: List[Video]
