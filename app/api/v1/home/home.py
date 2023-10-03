from fastapi import APIRouter
from app.schemas.extras.health import Home
from core.config import config


router = APIRouter()


@router.get("/")
async def home() -> Home:
    return Home(version=config.RELEASE_VERSION, status="Healthy")
