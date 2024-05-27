from fastapi import APIRouter, FastAPI

from app.core.config import settings
from app.routers.core import BaseRouterGroup
from app.routers.game import GameRouterGroup


def register_router(app: FastAPI):
    api_router = APIRouter()

    list_router: list[BaseRouterGroup] = [
        # ChatRouterGroup(),
        GameRouterGroup()
    ]

    for router in list_router:
        api_router.include_router(router.router)

    app.include_router(api_router, prefix=settings.API_V1_STR)
