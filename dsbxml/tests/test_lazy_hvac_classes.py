import subprocess
import sys

# Each check runs in a fresh interpreter: the build-on-first-use state is per process.
PROBE = """
import dsbxml
from dsbxml.hvac.components import {cls}
_ = dsbxml.dsbXML
print({cls}.__pydantic_complete__)
{action}
"""


def run(cls: str, action: str) -> str:
    code = PROBE.format(cls=cls, action=action)
    return subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True
    ).stdout


def test_a_component_class_is_built_on_first_use_not_at_import():
    assert run("Chiller", "").strip() == "False"


def test_an_unbuilt_component_class_still_reads_and_writes_on_its_own():
    out = run(
        "Chiller",
        "c = Chiller.from_xml('<Chiller type=\"Chiller\"></Chiller>')\n"
        "print(c.type, b'Chiller' in c.to_xml())",
    )
    assert out.split() == ["False", "Chiller", "True"]
