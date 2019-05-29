from enum import Enum

from api_fhir.models.element import Element


class Identifier(Element):

    resource_type = "Identifier"

    def __init__(self):
        self.use = None  # Type `IdentifierUse`.

        self.type = None  # Type `CodeableConcept` (represented as `dict` in JSON).

        self.system = None  # Type `str`.

        self.value = None  # Type `str` (value need to be unique)

        self.period = None  # Type `Period` (represented as `dict` in JSON).

        self.assigner = None  # Type `FHIRReference` referencing `Organization` (represented as `dict` in JSON, may be just text).

        super(Identifier, self).__init__()

    class Meta:
        app_label = 'api_fhir'

class IdentifierUse(Enum):
    USUAL = "usual"
    OFFICIAL = "official"
    TEMP = "temp"
    SECONDARY = "secondary"