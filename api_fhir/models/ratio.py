from api_fhir.models import Element, Property


class Ratio(Element):

    denominator = Property('denominator', 'Quantity')
    numerator = Property('numerator', 'Quantity')
