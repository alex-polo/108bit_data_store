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


