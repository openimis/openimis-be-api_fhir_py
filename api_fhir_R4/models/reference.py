from api_fhir_R4.models import Element, Property


class Reference(Element):

    display = Property('display', str)
    identifier = Property('identifier', 'Identifier')
    reference = Property('reference', str)
    type = Property('type', str)  # e.g. "Patient"
