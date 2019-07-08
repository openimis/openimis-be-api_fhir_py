from enum import Enum

from api_fhir.models import Element, Property


class ContactPoint(Element):

    period = Property('period', 'Period')
    rank = Property('rank', int)  # 1 = highest
    system = Property('system', str)  # ContactPointSystem (phone | fax | email | pager | url | sms | other)
    use = Property('use', str)  # ContactPointUse (home | work | temp | old | mobile)
    value = Property('value', str)


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
