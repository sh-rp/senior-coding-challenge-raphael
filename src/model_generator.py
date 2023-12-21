from typing import Dict, Type, Optional, Any
from datetime import date, time, datetime
from decimal import Decimal

from dlt.common.schema import Schema, TTableSchema
from dlt.common.schema.typing import TDataType
from pydantic import BaseModel, create_model


def _generate_model(name: str, schema: TTableSchema) -> Type[BaseModel]:
    # TODO: IMPLEMENT ME
    return BaseModel


def generate_models(schema: Schema) -> Dict[str, Type[BaseModel]]:
    result: Dict[str, Type[BaseModel]] = {}
    for name, table in schema.tables.items():
        result[name] = _generate_model(name, table)
    return result
