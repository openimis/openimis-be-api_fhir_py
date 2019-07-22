from enum import Enum

from api_fhir.models import Element, Property


class HumanName(Element):

    family = Property('family', str)
    given = Property('given', str, count_max='*')
    period = Property('period', 'Period')
    prefix = Property('prefix', str, count_max='*')
    suffix = Property('suffix', str, count_max='*')
    text = Property('text', str)
    use = Property('use', str)  # NameUse


class NameUse(Enum):
    USUAL = "usual"
    OFFICIAL = "official"
    TEMP = "temp"
    NICKNAME = "nickname"
    ANONYMOUS = "anonymous"
    OLD = "old"
    MAIDEN = "maiden"
