from app.schemas.item import Item

DB_NUM = 10


def get_path(arg: int | Item) -> str:
    if isinstance(arg, int):
        key = arg
    else:
        key = arg.key

    dir_index = key % DB_NUM + 1
    path = f'database/DB{dir_index}/{key}.json'

    return path