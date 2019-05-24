from enum import Enum

from api_fhir.models.element import Element


class ContactPoint(Element):

    resource_type = "ContactPoint"

    def __init__(self):
        self.period = None  # Type `Period` (represented as `dict` in JSON).

        self.rank = None  # Type `int` (1 = highest).

        self.system = None  # Type `str` (phone | fax | email | pager | url | sms | other).

        self.use = None  # Type `str` (home | work | temp | old | mobile).

        self.value = None  # Type `str`.

        super(ContactPoint, self).__init__()

    class Meta:
        app_label = 'api_fhir'

class ContactPointSystem(Enum):
    PHONE = "phone"
    FAX = "fax"
    EMAIL = "email"
    PAGER = "pager"
    URL = "url"
    SMS = "sms"
    OTHER = "other"

class ContactPointUse(Enum):
    HOME = "home"
    WORK = "work"
    TEMP = "temp"
    OLD = "old"
    MOBILE = "mobile"
