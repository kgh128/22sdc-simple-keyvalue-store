import hashlib

from app.repository.lruCache import LruCache
from app.schemas.item import Item

CACHE_LIST_SIZE = 10


def make_cache_list() -> list[LruCache]:
    cache_list: list[LruCache] = list()

    for index in range(CACHE_LIST_SIZE):
        cache_list.append(LruCache(index))

    return cache_list


def cache_index(arg: int | Item) -> int:
    if isinstance(arg, int):
        key = arg
    else:
        key = arg.key
    return int(hashlib.sha256(key).hexdigest(), 16) % CACHE_LIST_SIZE
