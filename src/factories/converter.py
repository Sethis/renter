

import json
from typing import Type, TypeVar, Sequence
from src.database.structure.model import Transport, User, Rent

T = TypeVar("T")


def get_converted_db_model_to_pydantic_model(db_model: Transport | User | Rent, pydantic_model: Type[T]) -> T:
    """
    Get a pydantic object converted from db models
    :param db_model: A object with data from the database
    :param pydantic_model: A type which will be result
    :return: the pydantic model with data from the database model
    """
    data = db_model.get_attributes_dict()

    return pydantic_model(**data)


def get_converted_sequence_of_db_model_to_pydantic_model_list(
        db_models: Sequence[Transport | User | Rent],
        pydantic_model: Type[T]
) -> list[T]:
    """
    Get a list of pydantic models from the sequence of db_models
    :param db_models: Some sequence of a db models
    :param pydantic_model: A type which list will be result
    :return: A list of the pydantic model with data from the database model
    """

    result = []

    for item in db_models:
        data = pydantic_model(**item.get_attributes_dict())

        result.append(data)

    return result
