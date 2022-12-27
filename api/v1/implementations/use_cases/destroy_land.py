from api.v1.repositories.redis import LandRepository
from fastapi import status
from fastapi.responses import JSONResponse


async def destroy_land_use_case():
    LandRepository.destroy_land()
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)
