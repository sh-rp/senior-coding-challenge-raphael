import json
import pytest

from dlt.common.schema import Schema

from src.model_generator import generate_models

from pydantic import ValidationError


def test_model_generator() -> None:
    # load schema from file
    with open("tests/example_schema.json", "r") as f:
        example_schema = Schema.from_stored_schema(json.load(f))

    # generate models
    models = generate_models(example_schema)

    # check test_resource model
    table_model = models["my_table"]

    # missing required field
    with pytest.raises(ValidationError):
        table_model.model_validate({"foo": "Hello"})

    # has required field
    model_instance = table_model.model_validate({"foo": "Hello", "name": "dlthub"})
    assert model_instance.name == "dlthub"  # type: ignore

    # foo is not part of table definition
    assert not hasattr(model_instance, "foo")
