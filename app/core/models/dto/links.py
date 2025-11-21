from datetime import datetime
import uuid

from pydantic import BaseModel, HttpUrl


class ShortLinkDTO(BaseModel):
    id: uuid.UUID
    link: HttpUrl
    slug: str
    created_at: datetime

class CreateShortLink(BaseModel):
    link: HttpUrl

class ShortLinkResponse(BaseModel):
    link: HttpUrl
    link_with_slug: str


