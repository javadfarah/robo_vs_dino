import settings
from api.v1.repositories.redis import LandRepository
from fastapi import status
from utils.exceptions import UnicornException
from fastapi import status
from fastapi.responses import JSONResponse


async def move_entity_use_case(move):
    if move.direction not in ["left", "right", "up", "down"]:
        raise UnicornException(message='bad request', status_code=status.HTTP_400_BAD_REQUEST)

    x = move.x
    y = move.y
    direction = move.direction
    origin_entity = LandRepository.get_data_by_id(f"{x}:{y}")
    if origin_entity.content != "robo":
        raise UnicornException(message='you cant move anything but robots', status_code=status.HTTP_400_BAD_REQUEST)

    match direction:
        case 'left':
            y -= 1
        case 'right':
            y += 1
        case 'up':
            x -= 1
        case 'down':
            x += 1
    print(x, y)
    if settings.GRID_SIZE < y or y < 1 or settings.GRID_SIZE < x or x < 1:
        raise UnicornException(status_code=status.HTTP_400_BAD_REQUEST, message='you can not move out of the box')
    destination_entity = LandRepository.get_data_by_id(f"{x}:{y}")
    if destination_entity.content is not None:
        raise UnicornException(message='conflict', status_code=status.HTTP_409_CONFLICT)
    LandRepository.set_data_by_id(origin_entity.id, options=dict(content=None))
    LandRepository.set_data_by_id(destination_entity.id, options=dict(content='robo'))
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)
