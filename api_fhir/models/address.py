from enum import Enum

from api_fhir.models import Element, Property


class Address(Element):

    city = Property('city', str)
    country = Property('country', str)
    district = Property('district', str)
    line = Property('line', str, count_max='*')
    period = Property('period', 'Period')
    postalCode = Property('postalCode', str)
    state = Property('state', str)
    text = Property('text', str)
    type = Property('type', str)  # postal | physical | both
    use = Property('use', str)  # home | work | temp | old


class AddressUse(Enum):
    HOME = "home"
    WORK = "work"
    TEMP = "temp"
    OLD = "old"


class AddressType(Enum):
    POSTAL = "postal"
    PHYSICAL = "physical"
    BOTH = "both"
