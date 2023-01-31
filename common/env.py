import os

COIN_PRICE = int(os.getenv("COIN_PRICE", 4))
ORDER_LIMIT = int(os.getenv("COIN_PRICE", 10))
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_DB = int(os.getenv('REDIS_DB', 0))
