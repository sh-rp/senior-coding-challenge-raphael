from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional, Type

from dlt.common.schema import Schema, TTableSchema
from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo


def _generate_model(name: str, schema: TTableSchema) -> Type[BaseModel]:
    columns = schema["columns"]
    # If the name of the column in the schema might shadow an
    # attribute for the base model, we get an error. So we need to
    # check names that we should use an alias
    protected_names = ["schema"]
    column_type_map = {
        "bool": bool,
        "timestamp": datetime,
        "bigint": int,
        "text": str,
        "decimal": Decimal,
        "complex": Dict,
    }

    fields = {}

    for column, column_spec in columns.items():
        required = not column_spec["nullable"]

        field_name = column if column not in protected_names else f"_{column}"
        data_type = column_type_map.get(str(column_spec["data_type"]))

        assert data_type is not None

        # I'd rather find a more proper way to do this check, but
        # apparently create_model is not meant to be used for more
        # complex field definitions
        if not required:
            data_type = Optional[data_type]  # type: ignore

        fields[field_name] = (data_type, FieldInfo(alias=column))

    return create_model(name, **fields)  # type: ignore


def generate_models(schema: Schema) -> Dict[str, Type[BaseModel]]:
    result: Dict[str, Type[BaseModel]] = {}
    for name, table in schema.tables.items():
        result[name] = _generate_model(name, table)
    return result
