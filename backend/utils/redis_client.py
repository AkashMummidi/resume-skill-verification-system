import redis

redis_client = redis.StrictRedis(
    host="127.0.0.1",
    port=6379,
    decode_responses=True,
    socket_timeout=3
)