from api.v1.repositories.redis import LandRepository
from fastapi import status
import settings
from fastapi import status
from fastapi.responses import JSONResponse


async def attack_use_case(location):
    x = location.x
    y = location.y
    cells_to_destroy = [f"{x}:{y - 1}", f"{x}:{y + 1}", f"{x - 1}:{y}", f"{x + 1}:{y}"]
    cells_to_destroy = list(
        filter(lambda item: settings.GRID_SIZE > int(item.split(':')[0]) > 0 and settings.GRID_SIZE > int(
            item.split(':')[1]) > 0,
               cells_to_destroy))
    for cells in cells_to_destroy:
        entity = LandRepository.get_data_by_id(cells)
        if entity and entity.content == 'dino':
            LandRepository.set_data_by_id(entity.id, options=dict(content=None))
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)
