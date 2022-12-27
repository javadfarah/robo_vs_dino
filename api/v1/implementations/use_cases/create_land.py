from api.v1.repositories.redis import LandRepository
from settings import GRID_SIZE
from fastapi import status
from fastapi.responses import JSONResponse


async def create_land_use_case(grid_size=GRID_SIZE):
    LandRepository.create_battle_land(grid_size)
    return JSONResponse(content={}, status_code=status.HTTP_201_CREATED)
