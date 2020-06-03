from enum import Enum

from api_fhir_R4.models import Element, Property


class Identifier(Element):

    use = Property('use', str)  # IdentifierUse
    type = Property('type', 'CodeableConcept')
    system = Property('system', str)
    value = Property('value', str)
    period = Property('period', 'Period')
    assigner = Property('assigner', 'Reference')  # referencing `Organization`


class IdentifierUse(Enum):
    USUAL = "usual"
    OFFICIAL = "official"
    TEMP = "temp"
    SECONDARY = "secondary"
    OLD = 'old'
