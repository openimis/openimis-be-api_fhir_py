from api_fhir_R4.models import Element, Property


class Narrative(Element):

    div = Property('div', str, required=True)
    status = Property('status', str, required=True)  # generated | extensions | additional | empty
