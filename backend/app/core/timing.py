import logging
import time


from fastapi import Request

logger = logging.getLogger("policypilot.timing")


async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    ms = (time.perf_counter() - start) * 1000

    response.headers["X-Response-Time-ms"] = f"{ms:.0f}"

    logger.warning(
        "%s %s -> %s in %.0f ms",
        request.method,
        request.url.path,
        response.status_code,
        ms,
    )

    return response
