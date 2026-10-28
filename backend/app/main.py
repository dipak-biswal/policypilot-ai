from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.rate_limit import limiter
from app.routers import agent, chat, documents, health
from app.core.config import settings

from app.core.timing import timing_middleware
from contextlib import asynccontextmanager
from app.retrieval.search import warm_up


@asynccontextmanager
async def lifespan(app: FastAPI):
    warm_up()  # runs once before the first request
    yield  # app serves requests here
    # (cleanup on shutdown would go after yield)


app = FastAPI(title="PolicyPilot AI", lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.middleware("http")(timing_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

for module in (health, documents, chat, agent):
    app.include_router(module.router)
