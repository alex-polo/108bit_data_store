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


class GetParserQuery(BaseModel):
    parser_system_name: str
