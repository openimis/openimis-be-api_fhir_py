from api_fhir.models import DomainResource, Property, BackboneElement


class CommunicationRequestRequester(BackboneElement):

    agent = Property('agent', 'Reference')  # referencing `Practitioner | Organization | Patient | RelatedPerson ...`
    onBehalfOf = Property('onBehalfOf', 'Reference')  # referencing `Organization`


class CommunicationRequestPayload(BackboneElement):

    contentString = Property('contentString', str)
    contentAttachment = Property('contentAttachment', 'Attachment')
    contentReference = Property('contentReference', 'Reference')  # referencing `Any`


class CommunicationRequest(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    basedOn = Property('basedOn', 'Reference', count_max='*')  # referencing `Any`
    replaces = Property('replaces', 'Reference', count_max='*')  # referencing `CommunicationRequest`
    groupIdentifier = Property('groupIdentifier', 'Identifier')
    status = Property('status', str, required=True)  # RequestStatus
    category = Property('category', 'CodeableConcept', count_max='*')
    priority = Property('priority', str)  # RequestPriority
    medium = Property('medium', 'CodeableConcept', count_max='*')
    subject = Property('subject', 'Reference')  # referencing `Patient | Group`
    recipient = Property('recipient', 'Reference', count_max='*')  # referencing `Device | Organization | Patient ...`
    topic = Property('topic', 'Reference', count_max='*')  # referencing `Any`
    context = Property('context', 'Reference')  # referencing `Encounter | EpisodeOfCare`
    payload = Property('payload', 'CommunicationRequestPayload', count_max='*')
    occurrenceDateTime = Property('occurrenceDateTime', 'FHIRDate')
    occurrencePeriod = Property('occurrencePeriod', 'Period')
    authoredOn = Property('authoredOn', 'FHIRDate')
    sender = Property('sender', 'Reference')  # referencing `Device | Organization | Patient ...`
    requester = Property('requester', 'CommunicationRequestRequester')
    reasonCode = Property('reasonCode', 'CodeableConcept', count_max='*')
    reasonReference = Property('reasonReference', 'Reference', count_max='*')  # referencing `Condition | Observation`
    note = Property('note', 'Annotation', count_max='*')
