import re
from typing import Any, Dict


def snake_to_camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part[:1].upper() + part[1:] for part in parts[1:])


def camel_to_snake(value: str) -> str:
    value = value.replace("-", "_").replace(".", "_").replace(" ", "_")
    value = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", value)
    value = re.sub("([a-z0-9])([A-Z])", r"\1_\2", value)
    return value.lower()


def keys_to_snake(data: Any) -> Any:
    if isinstance(data, list):
        return [keys_to_snake(item) for item in data]
    if isinstance(data, dict):
        return {camel_to_snake(str(key)): keys_to_snake(value) for key, value in data.items()}
    return data


def params_to_camel(params: Dict[str, Any]) -> Dict[str, Any]:
    return {snake_to_camel(key): value for key, value in params.items() if value is not None}
