from enum import Enum

from api_fhir.models.element import Element


class Address(Element):

    resource_type = "Address"

    def __init__(self):
        self.city = None  # Type `str`.

        self.country = None  # Type `str`.

        self.district = None  # Type `str`.

        self.line = None  # List of `str` items.

        self.period = None  # Type `Period` (represented as `dict` in JSON).

        self.postalCode = None  # Type `str`.

        self.state = None  # Type `str`.

        self.text = None  # Type `str`.

        self.type = None  # Type `str` (postal | physical | both).

        self.use = None  # Type `str` (home | work | temp | old | billing).

        super(Address, self).__init__()

    class Meta:
        app_label = 'api_fhir'

class AddressUse(Enum):
    HOME = "home"
    WORK = "work"
    TEMP = "temp"
    OLD = "old"

class AddressType(Enum):
    POSTAL = "postal"
    PHYSICAL = "physical"
    BOTH = "both"
