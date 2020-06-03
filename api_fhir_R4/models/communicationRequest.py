from api_fhir_R4.models import DomainResource, Property, BackboneElement


class CommunicationRequestPayload(BackboneElement):

    contentString = Property('contentString', str, required=True)
    contentAttachment = Property('contentAttachment', 'Attachment', required=True)
    contentReference = Property('contentReference', 'Reference', required=True)  # referencing `Any`


class CommunicationRequest(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    basedOn = Property('basedOn', 'Reference', count_max='*')  # referencing `Any`
    replaces = Property('replaces', 'Reference', count_max='*')  # referencing `CommunicationRequest`
    groupIdentifier = Property('groupIdentifier', 'Identifier')
    status = Property('status', str, required=True)  # RequestStatus
    statusReason = Property('statusReason', 'CodeableConcept')
    category = Property('category', 'CodeableConcept', count_max='*')
    priority = Property('priority', str)  # RequestPriority
    doNotPerform = Property('doNotPerform', bool)
    medium = Property('medium', 'CodeableConcept', count_max='*')
    subject = Property('subject', 'Reference')  # referencing `Patient | Group`
    about = Property('about', 'Reference', count_max='*')  # referencing 'Any'
    encounter = Property('encounter', 'Reference')  # referencing 'Encounter'
    payload = Property('payload', 'CommunicationRequestPayload', count_max='*')
    occurrenceDateTime = Property('occurrenceDateTime', 'FHIRDate')
    occurrencePeriod = Property('occurrencePeriod', 'Period')
    authoredOn = Property('authoredOn', 'FHIRDate')
    requester = Property('requester', 'Reference')  # referencing 'Practitioner', 'PractitionerRole', ...
    recipient = Property('recipient', 'Reference', count_max='*')  # referencing `Device | Organization | Patient ...`
    sender = Property('sender', 'Reference')  # referencing `Device | Organization | Patient ...`
    reasonCode = Property('reasonCode', 'CodeableConcept', count_max='*')
    reasonReference = Property('reasonReference', 'Reference', count_max='*')  # referencing `Condition | Observation`
    note = Property('note', 'Annotation', count_max='*')
