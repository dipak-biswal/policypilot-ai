from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings


def client_ip(request):
    forwarded = request.headers.get("x-forwarded-for")
    return forwarded.split(",")[0].strip() if forwarded else get_remote_address(request)


limiter = Limiter(key_func=client_ip, enabled=settings.rate_limit_enabled)
