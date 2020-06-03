from enum import Enum

from api_fhir_R4.models import Property, BackboneElement, DomainResource, FHIRDate


class LocationPosition(BackboneElement):

    longitude = Property('longitude', float, required=True)
    latitude = Property('latitude', float, required=True)
    altitude = Property('altitude', float, required=True)


class LocationHoursOfOperation(BackboneElement):

    daysOfWeek = Property('daysOfWeek', str, count_max='*')
    allDay = Property('allDay', bool)
    openingTime = Property('openingTime', FHIRDate)
    closingTime = Property('closingTime', FHIRDate)


class Location(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    status = Property('status', str)  # LocationStatus
    operationalStatus = Property('operationalStatus', 'Coding')
    name = Property('name', str)
    alias = Property('alias', str, count_max='*')
    description = Property('description', str)
    mode = Property('mode', str)  # LocationMode
    type = Property('type', 'CodeableConcept', count_max='*')
    telecom = Property('telecom', 'ContactPoint', count_max='*')
    address = Property('address', 'Address')
    physicalType = Property('physicalType', 'CodeableConcept')
    position = Property('position', 'LocationPosition')
    managingOrganization = Property('managingOrganization', 'Reference')  # referencing `Organization`
    partOf = Property('partOf', 'Reference')  # referencing `Location`
    hoursOfOperation = Property('hoursOfOperation', 'LocationHoursOfOperation', count_max='*')
    availabilityExceptions = Property('availabilityExceptions', str)
    endpoint = Property('endpoint', 'Reference', count_max='*')  # referencing `Endpoint`


class LocationMode(Enum):
    INSTANCE = "instance"
    KIND = "kind"


class LocationStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"
