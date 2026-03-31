from designbuilder_schema.core import DSB, Site
from designbuilder_schema.attributes import NameAttributes, NameAttribute
from designbuilder_schema.utils import save_model
import datetime

version = "8.0.0.057"

version_site_attribute = NameAttribute(name="Version", text=version)

site_attributes = NameAttributes(Attribute=[version_site_attribute])

site = Site(
    handle=1,
    count=1,
    Attributes=site_attributes,
    Tables=None,
    AssemblyLibrary=None,
    Buildings=None,
)

model = DSB(
    name="MadeByPydantic",
    date=datetime.date.today().isoformat(),
    version=version,
    objects="all",
    Site=site,
)

save_model(model, "examples/SmallestDSB.xml")
save_model(model, "examples/SmallestDSB.json")
