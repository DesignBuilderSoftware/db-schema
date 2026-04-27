import importlib
import inspect
from pathlib import Path

from pydantic import BaseModel


def generate_strawberry_types(module_path: str, output_path: str) -> None:
    """
    Generate Strawberry GraphQL types from Pydantic models in a given module.

    Args:
        module_path: Import path to the module containing Pydantic models (e.g., 'db_schema.attributes')
        output_path: File path where the generated code will be saved
    """
    # Import the module containing Pydantic models
    module = importlib.import_module(module_path)

    # Get all Pydantic models from the module
    pydantic_models: list[type[BaseModel]] = []
    for name, obj in inspect.getmembers(module):
        if (
            inspect.isclass(obj)
            and issubclass(obj, BaseModel)
            and obj != BaseModel
        ):
            pydantic_models.append(obj)

    # Generate the output code
    output_code = [
        "from strawberry.experimental.pydantic import type as strawberry_type",
        f"from {module_path} import *\n",
        "# Auto-generated Strawberry GraphQL types\n",
    ]

    # Generate Strawberry type classes
    for model in pydantic_models:
        class_code = [
            f"@strawberry_type(model={model.__name__}, all_fields=True)",
            f"class {model.__name__}Type:",
            "    pass\n",
        ]
        output_code.extend(class_code)

    # Write the generated code to file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(output_code))


def gen_attributes():
    generate_strawberry_types(
        module_path="db_schema.attributes",
        output_path="graph_ql/attributes.py",
    )


def gen_tables():
    generate_strawberry_types(
        module_path="db_schema.tables",
        output_path="graph_ql/tables.py",
    )


if __name__ == "__main__":
    # gen_attributes()
    gen_tables()
