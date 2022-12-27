import redis_om
from starlette import status
from starlette.responses import JSONResponse
from fastapi import HTTPException
from utils.exceptions import UnicornException
from models import LandField
from redis_om import Migrator


class LandRepository:

    @staticmethod
    def get_data_by_id(position_id: str):
        try:
            return LandField.find(LandField.id == position_id).first()
        except redis_om.NotFoundError:
            raise UnicornException(status_code=status.HTTP_404_NOT_FOUND, message="not found")

    @staticmethod
    def get_all_data(schema):
        all_data = schema.all_pks()
        result = []
        for data in all_data:
            _ = schema.get(data).dict()
            result.append(_['pk'])
        return result

    @staticmethod
    def create_battle_land(grid_size):
        for x in range(1, grid_size + 1):
            for y in range(1, grid_size + 1):
                schema = LandField(x=x, y=y, id=f"{x}:{y}")
                schema.save()
        Migrator().run()

    @classmethod
    def get_land(cls):
        all_data = LandField.all_pks()
        result = []
        for data in all_data:
            _ = LandField.get(data).dict()
            del _["pk"]
            result.append(_)
        return result

    @classmethod
    def insert_content_by_id(cls, position_id, content):
        field = LandField.find(LandField.id == position_id).first()
        field.content = content
        field.save()
        return

    @classmethod
    def destroy_land(cls):
        all_data = LandField.all_pks()
        for data in all_data:
            LandField.delete(data)

    @classmethod
    def set_data_by_id(cls, position_id: str, options: dict):
        entity = cls.get_data_by_id(position_id)
        for key, val in options.items():
            print(key)
            if hasattr(entity, key):
                setattr(entity, key, val)
        entity.save()
