"""Load JSON Schemas."""
import os
import ujson
from functools import wraps

from aiohttp import web
from jsonschema import Draft7Validator, validators
from jsonschema.exceptions import ValidationError



def load_schema(name):
    """Load JSON schemas."""
    module_path = os.path.dirname(__file__)
    path = os.path.join(module_path, f"{name}.json")
    with open(os.path.abspath(path), "r") as fp:
        data = fp.read()
    return ujson.loads(data)


def extend_with_default(validator_class):
    """Include default values present in JSON Schema.
    Source: https://python-jsonschema.readthedocs.io/en/latest/faq/#why-doesn-t-my-schema-s-default-property-set-the-default-on-my-instance
    """
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(
            validator,
            properties,
            instance,
            schema,
        ):
            yield error

    return validators.extend(
        validator_class,
        {"properties": set_defaults},
    )


DefaultValidatingDraft7Validator = extend_with_default(Draft7Validator)


def validate_schema(schema):
    """Validate JSON Schema, ensuring it is of correct form."""

    def wrapper(func):
        @wraps(func)
        async def wrapped(*args):
            request = args[-1]
            if not isinstance(request, web.Request):
                raise web.HTTPBadRequest(text="Invalid HTTP Request.")
            try:
                request_body = await request.json()
            except Exception:
                raise web.HTTPBadRequest(text="Could not properly parse Request Body as JSON")
            try:
                DefaultValidatingDraft7Validator(schema).validate(request_body)
            except ValidationError as e:
                raise web.HTTPBadRequest(text=f"Could not validate request body: {e.message}")

            return await func(*args)

        return wrapped

    return wrapper
