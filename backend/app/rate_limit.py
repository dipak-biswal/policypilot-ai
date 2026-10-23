import os

from slowapi import Limiter
from slowapi.util import get_remote_address


def client_ip(request):
    forwarded = request.headers.get("x-forwarded-for")
    return forwarded.split(",").strip() if forwarded else get_remote_address(request)


limiter = Limiter(
    key_func=client_ip, enabled=os.getenv("RATE_LIMIT_ENABLED", "true") == "true"
)
