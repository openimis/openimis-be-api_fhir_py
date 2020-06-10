from api_fhir_R4.models import BackboneElement, Property, DomainResource
from enum import Enum


class ActivityDefinitionDynamicValue(BackboneElement):

    path = Property('path', str, required=True)
    expression = Property('expression', 'Expression', required=True)


class ActivityDefinitionParticipant(BackboneElement):

    type = Property('type', str, required=True)
    role = Property('role', 'CodeableConcept')


class ActivityDefinition(DomainResource):

    url = Property('url', str)
    identifier = Property('identifier', 'Identifier', count_max='*')
    version = Property('version', str)
    name = Property('name', str)
    title = Property('title', str)
    subtitle = Property('subtitle', str)
    status = Property('status', str, required=True)
    experimental = Property('experimental', bool)
    subjectCodeableConcept = Property('subjectCodeableConcept', 'CodeableConcept')
    subjectReference = Property('subjectReference', 'Reference')  # referencing 'Group'
    date = Property('date', 'FHIRDate')
    publisher = Property('publisher', str)
    contact = Property('contact', 'ContactDetail', count_max='*')
    description = Property('description', str)
    useContext = Property('useContext', 'UsageContext', count_max='*')
    jurisdiction = Property('jurisdiction', 'CodeableConcept', count_max='*')
    purpose = Property('purpose', str)
    usage = Property('usage', str)
    copyright = Property('copyright', str)
    approvalDate = Property('approvalDate', 'FHIRDate')
    lastReviewDate = Property('lastReviewDate', 'FHIRDate')
    effectivePeriod = Property('effectivePeriod', 'Period')
    topic = Property('topic', 'CodeableConcept', count_max='*')
    author = Property('author', 'ContactDetail', count_max='*')
    editor = Property('editor', 'ContactDetail', count_max='*')
    reviewer = Property('reviewer', 'ContactDetail', count_max='*')
    endorser = Property('endorser', 'ContactDetail', count_max='*')
    relatedArtifact = Property('relatedArtifact', 'RelatedArtifact', count_max='*')
    library = Property('library', str, count_max='*')
    kind = Property('kind', str)
    profile = Property('profile', str)
    code = Property('code', 'CodeableConcept')
    intent = Property('intent', str)
    priority = Property('priority', str)
    doNotPerform = Property('doNotPerform', bool)
    timingTiming = Property('timingTiming', 'Timing')
    timingDateTime = Property('timingDateTime', 'FHIRDate')
    timingAge = Property('timingAge', 'Age')
    timingPeriod = Property('timingPeriod', 'Period')
    timingRange = Property('timingRange', 'Range')
    timingDuration = Property('timingDuration', 'Duration')
    location = Property('location', 'Reference')  # referencing 'Location'
    participant = Property('participant', 'ActivityDefinitionParticipant', count_max='*')
    productReference = Property('productReference', 'Reference')  # referencing 'Medication' and 'Substance'
    productCodeableConcept = Property('productCodeableConcept', 'CodeableConcept')
    quantity = Property('quantity', 'Quantity')
    dosage = Property('dosage', 'Dosage', count_max='*')
    bodySite = Property('bodySite', 'CodeableConcept', count_max='*')
    specimenRequirement = Property('specimenRequirement', 'Reference', count_max='*')  # referencing 'SpecimenDefinition'
    observationRequirement = Property('observationRequirement', 'Reference', count_max='*')  # referencing 'ObservationDefinition'
    observationResultRequirement = Property('observationResultRequirement', 'Reference', count_max='*')  # referencing 'ObservationDefinition'
    transform = Property('transform', str)
    dynamicValue = Property('dynamicValue', 'ActivityDefinitionDynamicValue', count_max='*')


class PublicationStatus(Enum):

    DRAFT = 'draft'
    ACTIVE = 'active'
    RETIRED = 'retired'
    UNKNOWN = 'unknown'


class RequestResourceType(Enum):

    APPOINTMENT = 'appointment'
    APPOINTMENT_RESPONSE = 'appointmentResponse'
    CARE_PLAN = 'carePlan'
    CLAIM = 'claim'
    COMMUNICATION_REQUEST = 'communicationRequest'
    CONTRACT = 'contract'
    DEVICE_REQUEST = 'deviceRequest'
    ENROLLMENT_REQUEST = 'enrollmentRequest'
    IMMUNIZATION_RECOMMENDATION = 'immunizationRecommendation'
    MEDICATION_REQUEST = 'medicationRequest'
    NUTRITION_ORDER = 'nutritionOrder'
    SERVICE_REQUEST = 'serviceRequest'
    SUPPLY_REQUEST = 'supplyRequest'
    TASK = 'task'
    VISION_PRESCRIPTION = 'visionPrescription'


class RequestIntent(Enum):

    PROPOSAL = 'proposal'
    PLAN = 'plan'
    DIRECTIVE = 'directive'
    ORDER = 'order'
    ORIGINAL_ORDER = 'original-order'
    REFLEX_ORDER = 'reflex-order'
    FILLER_ORDER = 'filler-order'
    INSTANCE_ORDER = 'instance-order'
    OPTION = 'option'


class RequestPriority(Enum):

    ROUTINE = 'routine'
    URGENT = 'urgent'
    ASAP = 'asap'
    STAT = 'stat'
