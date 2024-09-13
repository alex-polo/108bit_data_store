from typing import Optional

from pydantic import BaseModel


class ParsersResponse(BaseModel):
    id: int
    system_name: str
    parser_name: Optional[str]
    description: Optional[str]
    parser_type: Optional[str]
    is_enable: str
    is_parser_scheme_missing: str


class ChangeParserQuery(BaseModel):
    system_name: str
    parser_name: Optional[str]
    description: Optional[str]
    is_enable: str


class NewsGatheringResponse(BaseModel):
    id: int
    name: Optional[str]
    url: Optional[str]
    description: Optional[str]
    vendor: Optional[str]
    field_tags: Optional[str]
    parser_id: Optional[int]
    is_enable: str


class NewsGatheringById(BaseModel):
    id: int


class CatalogGatheringById(BaseModel):
    id: int


class NewsGatheringQuery(BaseModel):
    id: Optional[int] = -1
    name: Optional[str]
    url: Optional[str]
    description: Optional[str]
    vendor: Optional[str]
    field_tags: Optional[str]
    parser_id: int
    is_enable: str


class CatalogGatheringEntity(BaseModel):
    id: int
    name: Optional[str]
    url: Optional[str]
    description: Optional[str]
    parser_id: Optional[int]
    is_enable: str


class InternetSiteDTO(BaseModel):
    id: int
    name: str
    description: Optional[str]
    news_gathering_id: Optional[int]
    catalog_gathering_id: Optional[int]
