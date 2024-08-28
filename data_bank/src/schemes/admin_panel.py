from typing import Optional

from pydantic import BaseModel


class ParsersResponse(BaseModel):
    id: int
    system_name: str
    parser_name: Optional[str]
    description: Optional[str]
    parser_type: Optional[str]
    is_enable: bool
