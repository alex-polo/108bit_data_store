from typing import Optional

from pydantic import BaseModel


class NewsPostScheme(BaseModel):
    id: int
    date: int
    title: str
    details: str
    more: str
    image_url: str
    main_tag: str
    field_tags: str
    vendor: str


class UpdatePostScheme(BaseModel):
    post_id: int

class DispatchTimeScheme(BaseModel):
    time: int

class TgUserScheme(BaseModel):
    tg_identifier: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: Optional[str]


