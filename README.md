# DLT Hub Senior Dev coding challenge

## Introduction
This task is modelled around a typical ticket that you would work on in dlt.

Our python library `dlt` has an internal representation of database schemas, defined in the [schema.py](https://github.com/dlt-hub/dlt/blob/master/dlt/common/schema/schema.py) class. This schema is serializable to JSON with the `to_dict` method. In `dlt` these schemas automatically get inferred from your actual most of the time to create the correct tables and columns in the destination database. You can learn more about `dlt` schemas in our [schema docs](https://dlthub.com/docs/general-usage/schema). 

`Pydantic` is a straightforward python library for data validation. You can find their docs [here](https://docs.pydantic.dev/latest/). A very simple example of how pydantic works is this:

```python
from pydantic import BaseModel

# definition of the pydantic model
class User(BaseModel):
    index: int
    name: str
    
# validating a json
user_instance = User.model_validate({"index": 1, "name": "dave"})
# accessing attribute of pydantic instance
print(user_instance.name)

# this will fail, because index should be an int
user_instance = User.model_validate({"index": "one", "name": "dave"})
```

These pydantic models can also be created dynamically.

In this task you will create a converter function that converts a dlt schema (which includes a list of tables with columns) to a dict of pydantic models that can be used to validate actual data against a dlt schema. You will also need to write the relevant tests to make sure that your code works for all cases.


## Preparation
* Clone this repository to your local hard drive with `git clone ...`
* Install the python dependencies `poetry install`
* Start the poetry shell with `poetry shell`
* Ensure the pytest tests run with `pytest tests`(they will not pass, you need to finish the main task to get them to run, but they should execute)
* Now you're all set

## Main Task
The main task will be to implement the function `generate_model` in `src/model_generator.py`. This function converts a single dlt table schema `TTableSchema` to a pydantic `BaseModel`. To get started there is one simple test defined that takes an example model stored in `tests/example_schema.json`, and uses your implementation to create pydantic models which then have basic tests. Once you get this first test to pass (run `pytest tests`), please implement further tests that test that all types of dlt schemas are converted correctly into pydantic models, including optional fields and complex fields (JSON) among others.

Though not mandatory, it would be nice if you could format your code (run `black .` from the command line) and add python typings where applicable (run `mypy .` to check your typings).

If you get stuck at some point or you know what is still missing but you could not implement it because you ran out of time or do not know how to do it, leave a comment in the code. It is better to know that something is missing and be able to ask for help than not adding anything at all :)

## Additional Tasks
If you have time left, you can earn extra points by implementing and testing some or all of the following features:

1. Find a way to store additional field annotations in the pydantic models, such as as `primary_key` or `unique`.

2. `dlt` has a concept of `schema contracts`. Though our schema contracts are more complex than this, for the sake of the test let's assume we have one contract that says the incoming data will fail validation by raising an exception if there are extra fields that are not defined in the schema. Another contract might say, that extra fields will simply be removed without an exception, so the data will be sanitized. Both is possible with `pydantic` models. Extend your function to be able to respect these two contracts.

3. dlt schemas can store precision information for Numbers. Extend your function to be able to validate the precision of an incoming decimal if it is defined in the `dlt` schema.

## Resources
* [dlt docs](https://dlthub.com/docs)
* [pydantic docs](https://docs.pydantic.dev/latest/)

## Questions

	