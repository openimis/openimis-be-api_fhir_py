from api_fhir_R4.models import Element, Property


class Range(Element):

    high = Property('high', 'Quantity')
    low = Property('low', 'Quantity')
