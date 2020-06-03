from api_fhir_R4.models import Element, Property


class Ratio(Element):

    denominator = Property('denominator', 'Quantity')
    numerator = Property('numerator', 'Quantity')
