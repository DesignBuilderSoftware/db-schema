from designbuilder_schema.core import dsbXML, Site
from designbuilder_schema.utils import save_model
import datetime

version = "2025.1.1.004"

site = Site(
    handle=1,
    count=1,
    Attributes=None,
    Tables=None,
    AssemblyLibrary=None,
    Buildings=None,
)

model = dsbXML(
    name="MadeByPydantic",
    date=datetime.date.today().isoformat(),
    version=version,
    objects="all",
    Site=site,
)

save_model(model, "examples/SmallestDSB.xml")
