import enum
from dataclasses import dataclass, asdict
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


@dataclass
class PostData(Response):
    date: datetime
    title: str
    details: str
    more: str
    image_url: Optional[str]
    main_tag: Optional[str]
    fields_tags: Optional[str]
    author: Optional[str]
    malfunctions: Optional[List[MalfunctionResponse]]


@dataclass
class FormatField:
    status: Status
    field_name: str
    field_value: str
    warning_message: Optional[MalfunctionResponse]
