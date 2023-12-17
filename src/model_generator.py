from typing import Dict, Type, Optional, Any
from datetime import date, time, datetime
from decimal import Decimal

from dlt.common.schema import Schema, TTableSchema
from dlt.common.schema.typing import TDataType
from pydantic import BaseModel, create_model


def _generate_model(name: str, schema: TTableSchema) -> Type[BaseModel]:
    # implement me

    # START: THIS WILL BE REMOVED FOR THE HOMEWORK
    type_map: Dict[TDataType, Any] = {
        "text": str,
        "double": float,
        "bool": bool,
        "timestamp": int,
        "bigint": int,
        "binary": bytes,
        "complex": Dict[Any, Any],
        "decimal": Decimal,
        "wei": int,
        "date": date,
        "time": datetime,
    }

    fields: Dict[str, Any] = {}
    for cname, column in schema["columns"].items():
        if cname == "schema":
            continue
        fields[cname] = (
            (type_map[column["data_type"]] | None, None)
            if column.get("nullable")
            else (type_map[column["data_type"]], ...)
        )

    return create_model(name + "_model", **fields)  # type: ignore
    # END: THIS WILL BE REMOVED FOR THE HOMEWORK


def generate_models(schema: Schema) -> Dict[str, Type[BaseModel]]:
    result: Dict[str, Type[BaseModel]] = {}
    for name, table in schema.tables.items():
        result[name] = _generate_model(name, table)
    return result
