from enum import Enum

from api_fhir.models import Property, BackboneElement, DomainResource


class LocationPosition(BackboneElement):
    altitude = Property('altitude', float)
    latitude = Property('latitude', float)
    longitude = Property('longitude', float)


class Location(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    status = Property('status', str)  # LocationStatus
    operationalStatus = Property('operationalStatus', 'Coding')
    name = Property('name', str)
    alias = Property('alias', str, count_max='*')
    description = Property('description', str)
    mode = Property('mode', str)  # LocationMode
    type = Property('type', 'CodeableConcept')
    telecom = Property('telecom', 'ContactPoint', count_max='*')
    address = Property('address', 'Address')
    physicalType = Property('physicalType', 'CodeableConcept')
    position = Property('position', 'LocationPosition')
    managingOrganization = Property('managingOrganization', 'Reference')  # referencing `Organization`
    partOf = Property('partOf', 'Reference')  # referencing `Location`
    endpoint = Property('endpoint', 'Reference', count_max='*')  # referencing `Endpoint`


class LocationMode(Enum):
    INSTANCE = "instance"
    KIND = "kind"


class LocationStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"
