from fastapi import APIRouter, FastAPI

from core.config import settings
from routers import BaseRouterGroup
from routers.chat import ChatRouterGroup


def register_router(app: FastAPI):
    api_router = APIRouter()

    list_router: list[BaseRouterGroup] = [
        ChatRouterGroup(),
    ]

    for router in list_router:
        api_router.include_router(router.router)

    app.include_router(api_router, prefix=settings.API_V1_STR)
