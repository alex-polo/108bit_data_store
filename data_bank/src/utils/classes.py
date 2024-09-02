import enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union, Any, List


class Status(enum.Enum):
    Ok = 101
    Warning = 102
    Error = 103


@dataclass
class Response:
    status: Status


@dataclass
class SuccessResponse(Response):
    content: Union[Any]


@dataclass
class MalfunctionResponse(Response):
    date: datetime
    type: str
    type_detail: str
    service_name: str
    module_name: str
    source: str
    title: str
    image_path: str
    description: Optional[str] = None
    error_text: Optional[str] = None
    text_details: Optional[str] = None
    attribute_1: Optional[str] = None
    attribute_2: Optional[str] = None
    attribute_3: Optional[str] = None
    attribute_4: Optional[str] = None
    attribute_5: Optional[str] = None


@dataclass
class ParserField:
    is_format: bool
    text: str


@dataclass
class ParsedData:
    is_valid = True
    site_name: str
    date: datetime
    title: ParserField
    more: str
    image_url: Optional[str]
    details: ParserField
    error_content = Optional[MalfunctionResponse]
