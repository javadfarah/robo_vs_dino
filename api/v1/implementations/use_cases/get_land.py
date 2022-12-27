from api.v1.repositories.redis import LandRepository
from settings import GRID_SIZE
from fastapi import status
from fastapi.responses import JSONResponse


async def get_land_use_case():
    land = LandRepository.get_land()
    return JSONResponse(content={"data": {"items": land, "count": GRID_SIZE}}, status_code=status.HTTP_200_OK)
