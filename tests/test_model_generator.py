import json
import pytest
from decimal import Decimal

from dlt.common.schema import Schema

from src.model_generator import generate_models

from pydantic import ValidationError

# this is a dict that should pass validation of the "my_table" model
VALID_DICT = {
    "foo": "Hello",
    "id": 5,
    "name": "dlthub",
    "content": {"nested": "value"},
    "salary": Decimal("100.00"),
}


def test_model_generator() -> None:
    # load schema from file
    with open("tests/example_schema.json", "r") as f:
        example_schema = Schema.from_stored_schema(json.load(f))

    # generate models
    models = generate_models(example_schema)

    # check test_resource model
    table_model = models["my_table"]

    # validate model
    model_instance = table_model.model_validate(VALID_DICT)
    # attributes  should be set
    assert model_instance.name == "dlthub"  # type: ignore
    assert model_instance.id == 5  # type: ignore
    assert model_instance.content == {"nested": "value"}  # type: ignore

    # foo does not exist in schema
    assert not hasattr(model_instance, "foo")

    # incorrect datatype will raise
    with pytest.raises(ValidationError):
        table_model.model_validate({**VALID_DICT, "id": "five"})

    # missing required field will raise
    with pytest.raises(ValidationError):
        table_model.model_validate({"foo": "Hello"})
