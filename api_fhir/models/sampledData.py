from api_fhir.models import Element, Property


class SampledData(Element):

    data = Property('data', str)  # "E" | "U" | "L"
    dimensions = Property('dimensions', int)
    factor = Property('factor', float)
    lowerLimit = Property('lowerLimit', float)
    origin = Property('origin', 'Quantity')
    period = Property('period', float)
    upperLimit = Property('upperLimit', float)
