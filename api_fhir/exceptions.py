class FhirRequestProcessException(Exception):
    def __init__(self, message):
        super(FhirRequestProcessException, self).__init__(message)


class FHIRException(Exception):
    def __init__(self, message):
        super(FHIRException, self).__init__(message)


class InvalidAttributeError(FHIRException):
    def __init__(self, attr, property_type):
        msg = "The attribute named `{}` is not a valid property for `{}`.".format(attr, property_type)
        super(InvalidAttributeError, self).__init__(msg)


class PropertyError(FHIRException):
    def __init__(self, message):
        super(PropertyError, self).__init__(message)


class PropertyMaxSizeError(PropertyError):
    def __init__(self, definition):
        message = "The max size was exceeded for property {} [{}..{}]".format(definition.name,
                                                                              definition.count_min,
                                                                              definition.count_max)
        super(PropertyMaxSizeError, self).__init__(message)


class PropertyTypeError(Exception):
    def __init__(self, local_type, description):
        msg = "Expected '{}' but got '{}' for '{}' property".format(description.type, local_type, description.name)
        super(PropertyTypeError, self).__init__(msg)


class UnsupportedFormatError(Exception):
    def __init__(self, data_format):
        message = "The format '{}' is not supported".format(data_format)
        super(UnsupportedFormatError, self).__init__(message)
