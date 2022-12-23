from redis_om import get_redis_connection

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0
SUM_LIMIT_HOURLY = 100
BAD_REQUEST_LIMIT = 15
GRID_SIZE = 10
redis_instance = get_redis_connection(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password='',
    db=REDIS_DB,
    decode_responses=True
)
