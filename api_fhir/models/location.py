from enum import Enum

from api_fhir.models import DomainResource, BackboneElement


class Location(DomainResource):

    resource_type = "Location"

    def __init__(self):
        self.identifier = None  # List of `Identifier` items (represented as `dict` in JSON).

        self.status = None  # Type `LocationStatus`.

        self.operationalStatus = None  # Type `Coding` (represented as `dict` in JSON).

        self.name = None  # Type `str`.

        self.alias = None  # List of `str` items.

        self.description = None  # Type `str`.

        self.mode = None  # Type `LocationMode`.

        self.type = None  # Type `CodeableConcept` (represented as `dict` in JSON).

        self.telecom = None  # List of `ContactPoint` items (represented as `dict` in JSON).

        self.address = None  # Type `Address` (represented as `dict` in JSON).

        self.physicalType = None  # Type `CodeableConcept` (represented as `dict` in JSON).

        self.position = None  # Type `LocationPosition` (represented as `dict` in JSON).

        self.managingOrganization = None  # Type `Reference` referencing `Organization` (represented as `dict` in JSON).

        self.partOf = None  # Type `Reference` referencing `Location` (represented as `dict` in JSON).

        self.endpoint = None  # List of `Reference` items referencing `Endpoint` (represented as `dict` in JSON).

        super(Location, self).__init__()

    class Meta:
        app_label = 'api_fhir'


class LocationPosition(BackboneElement):

    resource_type = "LocationPosition"

    def __init__(self):
        self.altitude = None  # Type `float`.

        self.latitude = None  # Type `float`.

        self.longitude = None  # Type `float`.

        super(LocationPosition, self).__init__()

    class Meta:
        app_label = 'api_fhir'


class LocationMode(Enum):
    INSTANCE = "instance"
    KIND = "kind"


class LocationStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"
