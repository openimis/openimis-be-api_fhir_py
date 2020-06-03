from api_fhir_R4.models import Element, Property


class CodeableConcept(Element):

    coding = Property('coding', 'Coding', count_max='*')
    text = Property('text', str)
