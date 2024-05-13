from fastapi import APIRouter, FastAPI

from core.config import settings
from routers.auth import AuthRouterGroup
from routers.chat import ChatRouterGroup
from routers.core import BaseRouterGroup


def register_router(app: FastAPI):
    api_router = APIRouter()

    list_router: list[BaseRouterGroup] = [
        ChatRouterGroup(),
        AuthRouterGroup()
    ]

    for router in list_router:
        api_router.include_router(router.router)

    app.include_router(api_router, prefix=settings.API_V1_STR)
