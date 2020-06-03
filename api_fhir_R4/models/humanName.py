from enum import Enum

from api_fhir_R4.models import Element, Property


class HumanName(Element):

    use = Property('use', str)  # NameUse
    text = Property('text', str)
    family = Property('family', str)
    given = Property('given', str, count_max='*')
    prefix = Property('prefix', str, count_max='*')
    suffix = Property('suffix', str, count_max='*')
    period = Property('period', 'Period')


class NameUse(Enum):
    USUAL = "usual"
    OFFICIAL = "official"
    TEMP = "temp"
    NICKNAME = "nickname"
    ANONYMOUS = "anonymous"
    OLD = "old"
    MAIDEN = "maiden"
