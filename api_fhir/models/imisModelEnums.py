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
