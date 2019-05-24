from enum import Enum


class ImisGenderCodes(Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"

class ImisMaritialStatus(Enum):
    MARRIED = "M"
    SINGLE = "S"
    DIVORCED = "D"
    WIDOWED = "W"
    NOT_SPECIFIED = "N"
