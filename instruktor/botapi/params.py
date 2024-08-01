from typing import Optional

from instruktor.config import get_api_credentials, get_endpoints_config

TOKEN: Optional[str] = None
ENDPOINTS = get_endpoints_config()
AC = get_api_credentials()

