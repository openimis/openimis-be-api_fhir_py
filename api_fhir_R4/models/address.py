from enum import Enum

from api_fhir_R4.models import Element, Property


class Address(Element):

    use = Property('use', str)  # home | work | temp | old | billing
    type = Property('type', str)  # postal | physical | both
    text = Property('text', str)
    line = Property('line', str, count_max='*')
    city = Property('city', str)
    district = Property('district', str)
    state = Property('state', str)
    postalCode = Property('postalCode', str)
    country = Property('country', str)
    period = Property('period', 'Period')


class AddressUse(Enum):
    HOME = "home"
    WORK = "work"
    TEMP = "temp"
    OLD = "old"
    BILLING = 'billing'


class AddressType(Enum):
    POSTAL = "postal"
    PHYSICAL = "physical"
    BOTH = "both"
