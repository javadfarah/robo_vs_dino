from settings import redis_instance, GRID_SIZE
from models import LandField


class RedisRepository:

    @staticmethod
    def get_data_with_key(key: str):
        return redis_instance.get(key)

    @staticmethod
    def add_data_with_key(key: str, data):
        redis_instance.set(key, data)

    @staticmethod
    def set_expire_with_key(key: str, seconds: int):
        redis_instance.expire(name=key, time=seconds)

    @staticmethod
    def get_all_data_with_orm(schema):
        all_data = schema.all_pks()
        result = []
        for data in all_data:
            _ = schema.get(data).dict()
            del _["pk"]
            result.append(_)
        return result

    @staticmethod
    def save_orm_object(schema):
        schema.save()

    @staticmethod
    def create_battle_land(schema: LandField, grid_size=GRID_SIZE):
        for x in range(1, grid_size):
            for y in range(1, grid_size):
                schema.x = x
                schema.y = y
                schema.pk = f"{x}:{y}"
                schema.save()

    @classmethod
    def move(cls, x, y, direction):
        entity = cls.get_data_with_key(f"{x}:{y}")
        if entity.content != "dino":
            return None
        if direction not in ["left", "right", "up", "down"]:
            return None

        match direction:
            case 'left':
                x -= 1
            case 'right':
                x += 1
            case 'up':
                y += 1
            case 'down':
                y -= 1
        entity.content = None
        entity.save()
        entity = cls.get_data_with_key(f"{x}:{y}")
        if entity.content is not None:
            return None
        entity.content = 'dino'
        entity.x = x
        entity.y = y
        entity.save()

    @classmethod
    def attack(cls, x, y):
        cells_to_destroy = [f"{x}:{y - 1}", f"{x}:{y + 1}", f"{x - 1}:{y}", f"{x + 1}:{y}"]
        for cells in cells_to_destroy:
            entity = cls.get_data_with_key(cells)
            if entity.content == 'dino':
                entity.content = None
                entity.save()
