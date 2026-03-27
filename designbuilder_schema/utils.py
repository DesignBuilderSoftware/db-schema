import json, xmltodict
from designbuilder_schema.core import DSB
from designbuilder_schema.id import set_site_counter


def remove_prefixes(_, key, value):
    if key[0] in "@#":
        return key[1:], value
    else:
        return key, value


def add_prefixes(data_dict):
    if isinstance(data_dict, list):
        return [add_prefixes(l) for l in data_dict]
    elif isinstance(data_dict, dict):
        return {
            ("#text" if key == "text" else "@" + key if key[0].islower() else key): (
                add_prefixes(val) if isinstance(val, (dict, list)) else val
            )
            for key, val in data_dict.items()
        }
    else:
        return data_dict


def file_to_dict(filepath: str) -> dict:
    """Load a file as a dictionary"""
    if filepath.endswith(".json"):
        with open(filepath, "r") as f:
            return json.loads(f.read())
    elif filepath.endswith(".xml"):
        with open(filepath, "rb") as f:
            return xmltodict.parse(f.read(), postprocessor=remove_prefixes)
    else:
        raise ValueError("Unsupported file format")


def load_model(filepath: str) -> DSB:
    """Loads DBJSON model from file and validates at the same time."""
    dict = file_to_dict(filepath)
    root_key = next(iter(dict))
    site_handle = int(dict[root_key]["Site"]["handle"])
    set_site_counter(site_handle)
    return DSB.model_validate(dict[root_key])


def dict_to_file(dictionary: dict, filepath: str) -> None:
    """Save dictionary to either JSON or XML file format."""
    if not (filepath.endswith(".json") or filepath.endswith(".xml")):
        raise ValueError(f"Unsupported file format: {filepath}")

    root_key = next(iter(dictionary))
    file_format = "JSON" if filepath.endswith(".json") else "XML"
    new_key = f"dsb{file_format}"
    pop = dictionary.pop(root_key)

    if file_format == "JSON":
        dictionary[new_key] = pop
        data = json.dumps(dictionary, indent=4)
    else:
        dictionary[new_key] = add_prefixes(pop)
        data = xmltodict.unparse(dictionary, full_document=True, pretty=True)

    with open(filepath, "w") as f:
        f.write(data)


def save_model(model: DSB, filepath: str) -> None:
    model = model.model_dump(mode="json", by_alias=True)
    dict_to_file({"dsbXML": model}, filepath)
