from typing import Optional

from pydantic import BaseModel


class NewsPost(BaseModel):
    id: int
    date: int
    title: str
    details: str
    more: str
    image_url: str
    main_tag: str
    field_tags: str
    vendor: str


class UpdatePostRequest(BaseModel):
    id: int

class TgUser(BaseModel):
    id: int
    tg_id: int
    first_name: Optional[str]
    second_name: Optional[str]
    surname: Optional[str]
    phone_number_tg: Optional[str]
    is_active: Optional[bool]


