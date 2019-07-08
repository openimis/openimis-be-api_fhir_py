from api_fhir.models import Element, Property


class Quantity(Element):

    code = Property('code', str)
    comparator = Property('comparator', str)  # < | <= | >= | >
    system = Property('system', str)
    unit = Property('unit', str)
    value = Property('value', float)
