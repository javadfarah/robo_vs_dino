from api.v1.repositories.redis import LandRepository
from fastapi import status
from fastapi import status
from fastapi.responses import JSONResponse


async def insert_content_use_case(location):
    LandRepository.insert_content_by_id(location.position, location.content)
    return JSONResponse(content={}, status_code=status.HTTP_201_CREATED)
