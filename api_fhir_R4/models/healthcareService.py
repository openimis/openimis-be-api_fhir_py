from api_fhir_R4.models import Property, BackboneElement, DomainResource
from enum import Enum


class HealthcareNotAvailable(BackboneElement):
    description = Property('description', str, required=True)
    during = Property('during', 'Period')


class HealthcareServiceAvailableTime(BackboneElement):
    daysOfWeek = Property('daysOfWeek', str, count_max='*')
    allDay = Property('allDay', bool)
    availableStartTime = Property('availableStartTime', 'FHIRDate')
    availableEndTime = Property('availableEndTime', 'FHIRDate')


class HealthcareServiceEligibility(BackboneElement):
    code = Property('code', 'CodeableConcept')
    comment = Property('comment', str)


class HealthcareService(DomainResource):
    identifier = Property('identifier', 'Identifier', count_max='*')
    active = Property('active', bool)
    providedBy = Property('providedBy', 'Reference')  # referencing 'Organization'
    category = Property('category', 'CodeableConcept', count_max='*')
    type = Property('type', 'CodeableConcept', count_max='*')
    speciality = Property('speciality', 'CodeableConcept', count_max='*')
    location = Property('location', 'Reference', count_max='*')  # referencing 'Location'
    name = Property('name', str)
    comment = Property('comment', str)
    extraDetails = Property('extraDetails', str)
    photo = Property('photo', 'Attachment')
    telecom = Property('telecom', 'ContactPoint', count_max='*')
    coverageArea = Property('coverageArea', 'Reference', count_max='*')  # referencing 'Location'
    serviceProvisionCode = Property('serviceProvisionCode', 'CodeableConcept', count_max='*')
    eligibility = Property('eligibility', 'HealthcareServiceEligibility', count_max='*')
    program = Property('program', 'CodeableConcept', count_max='*')
    characteristic = Property('characteristic', 'CodeableConcept', count_max='*')
    communication = Property('communication', 'CodeableConcept', count_max='*')
    referralMethod = Property('referralMethod', 'CodeableConcept', count_max='*')
    appointmentRequired = Property('appointmentRequired', bool)
    availableTime = Property('availableTime', 'HealthcareServiceAvailableTme', count_max='*')
    notAvailable = Property('notAvailable', 'HealthcareServiceNotAvailable', count_max='*')
    availabilityExceptions = Property('availabilityExceptions', str)
    endpoint = Property('endpoint', 'Reference', count_max='*')  # referencing 'Endpoint'


class DaysOfWeek(Enum):
    MON = 'Monday'
    TUE = 'Tuesday'
    WED = 'Wednesday'
    THU = 'Thursday'
    FRI = 'Friday'
    SAT = 'Saturday'
    SUN = 'Sunday'
