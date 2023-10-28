

import json
from typing import Type, TypeVar
from src.database.structure.model import User

T = TypeVar("T")


def get_converted_db_user_to_pydantic_model(db_model: User, pydantic_model: Type[T]) -> T:
    data = db_model.get_attributes_dict()

    data = json.dumps(data)

    return pydantic_model.model_validate_json(data)
