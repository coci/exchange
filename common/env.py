import os

COIN_PRICE = int(os.getenv("COIN_PRICE", 4))
ORDER_LIMIT = int(os.getenv("ORDER_LIMIT", 10))
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))
