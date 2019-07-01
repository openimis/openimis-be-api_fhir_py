from api_fhir.models import Element, Property


class Narrative(Element):

    div = Property('div', str)
    status = Property('status', str)  # generated | extensions | additional | empty

    class Meta:
        app_label = 'api_fhir'
