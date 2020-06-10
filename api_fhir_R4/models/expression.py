from api_fhir_R4.models import Element, Property


class Expression(Element):

    description = Property('description', str)
    name = Property('name', str)
    language = Property('language', str, required=True)
    expression = Property('expression', str)
    reference = Property('reference', str)
