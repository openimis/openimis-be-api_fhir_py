from api_fhir.models import DomainResource, Property, BackboneElement, FHIRDate


class PractitionerAvailableTime(BackboneElement):

    daysOfWeek = Property('daysOfWeek', str)  # DaysOfWeek
    allDay = Property('allDay', bool)
    availableStartTime = Property('availableStartTime', FHIRDate)
    availableEndTime = Property('availableEndTime', FHIRDate)


class PractitionerNotAvailable(BackboneElement):

    description = Property('description', str, required=True)
    during = Property('during', 'Period')


class PractitionerRole(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    active = Property('active', bool)
    period = Property('period', 'Period')
    practitioner = Property('practitioner', 'Reference')
    organization = Property('organization', 'Reference')
    code = Property('code', 'CodeableConcept', count_max='*')
    specialty = Property('specialty', 'CodeableConcept', count_max='*')
    location = Property('location', 'Reference', count_max='*')
    healthcareService = Property('healthcareService', 'Reference', count_max='*')
    telecom = Property('telecom', 'ContactPoint', count_max='*')
    availableTime = Property('availableTime', 'PractitionerAvailableTime', count_max='*')
    notAvailable = Property('notAvailable', 'PractitionerNotAvailable', count_max='*')
    availabilityExceptions = Property('availabilityExceptions', str)
    endpoint = Property('endpoint', 'Reference', count_max="*")  # referencing `Endpoint`
