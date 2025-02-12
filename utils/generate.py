from uuid import uuid4


def generate_unique_id() -> int:
    id_number = str(uuid4().int)[:18]
    return int(id_number)
