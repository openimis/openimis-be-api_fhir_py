from api_fhir.models import Element, Property


class Range(Element):

    high = Property('high', 'Quantity')
    low = Property('low', 'Quantity')
