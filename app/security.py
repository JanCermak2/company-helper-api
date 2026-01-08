import os
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

# Lokálně default, v produkci se nastaví přes env var COMPANY_HELPER_API_KEY
API_KEY = os.getenv("COMPANY_HELPER_API_KEY", "dev-key")


def require_api_key(api_key: str | None = Security(API_KEY_HEADER)) -> None:
    if not api_key or api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
