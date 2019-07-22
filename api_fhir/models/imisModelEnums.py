from enum import Enum


class ImisMaritalStatus(Enum):
    MARRIED = "M"
    SINGLE = "S"
    DIVORCED = "D"
    WIDOWED = "W"
    NOT_SPECIFIED = "N"


class ImisHfLevel(Enum):
    HEALTH_CENTER = "C"
    HOSPITAL = "H"
    DISPENSARY = "D"


class ImisClaimIcdTypes(Enum):
    ICD_0 = "icd_0"
    ICD_1 = "icd_1"
    ICD_2 = "icd_2"
    ICD_3 = "icd_3"
    ICD_4 = "icd_4"
