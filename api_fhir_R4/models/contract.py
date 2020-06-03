from api_fhir_R4.models import DomainResource, Property, BackboneElement


class ContractTermOfferAnswer(BackboneElement):

    valueBoolean = Property('valueBoolean', bool, required=True)
    valueDecimal = Property('valueDecimal', float, required=True)
    valueInteger = Property('valueInteger', int, required=True)
    valueDate = Property('valueDate', 'FHIRDate', required=True)
    valueDateTime = Property('valueDateTime', 'FHIRDate', required=True)
    valueTime = Property('valueTime', 'Time', required=True)
    valueString = Property('valueString', str, required=True)
    valueUri = Property('valueUri', str, required=True)
    valueAttachment = Property('valueAttachment', 'Attachment', required=True)
    valueCoding = Property('valueCoding', 'Coding', required=True)
    valueQuantity = Property('valueQuantity', 'Quantity', required=True)
    valueReference = Property('valueReference', 'Reference', required=True)  # referencing 'Any'


class ContractTermOfferParty(BackboneElement):

    reference = Property('reference', 'Reference', required=True, count_max='*')  # referencing 'Patient', 'RelatedPerson', ...
    role = Property('role', 'CodeableConcept', required=True)


class ContractTermOffer(BackboneElement):

    identifier = Property('identifier', 'Identifier', count_max='*')
    party = Property('party', 'ContractTermOfferParty', count_max='*')
    topic = Property('topic', 'Reference')  # referencing 'Any'
    type = Property('type', 'CodeableConcept')
    decision = Property('decision', 'CodeableConcept')
    decisionMode = Property('decisionMode', 'CodeableConcept', count_max='*')
    answer = Property('answer', 'ContractTermOfferAnswer', count_max='*')
    text = Property('text', str)
    linkId = Property('linkId', str, count_max='*')
    securityLabelNumber = Property('securityLabelNumber', int, count_max='*')


class ContractTermSecurityLabel(BackboneElement):

    number = Property('number', int, count_max='*')
    classification = Property('classification', 'Coding', required=True)
    category = Property('category', 'Coding', count_max='*')
    control = Property('control', 'Coding', count_max='*')


class ContractTermAssetContext(BackboneElement):

    reference = Property('reference', 'Reference')  # referencing 'Any'
    code = Property('code', 'CodeableConcept', count_max='*')
    text = Property('text', str)


class ContractTermAssetValuedItem(BackboneElement):

    entityCodeableConcept = Property('entityCodeableConcept', 'CodeableConcept')
    entityReference = Property('entityReference', 'Reference')  # referencing 'Any'
    identifier = Property('identifier', 'Identifier')
    effectiveTime = Property('effectiveTime', 'FHIRDate')
    quantity = Property('quantity', 'Quantity')
    unitPrice = Property('unitPrice', 'Money')
    factor = Property('factor', float)
    points = Property('points', float)
    net = Property('net', 'Money')
    payment = Property('payment', str)
    paymentDate = Property('paymentDate', 'FHIRDate')
    responsible = Property('responsible', 'Reference')  # referencing 'Organization', 'Patient', ...
    recipient = Property('recipient', 'Reference')  # referencing 'Organization', 'Patient', ...
    linkId = Property('linkId', str, count_max='*')
    securityLabelNumber = Property('securityLabelNumber', int, count_max='*')


class ContractTermAsset(BackboneElement):

    scope = Property('scope', 'CodeableConcept')
    type = Property('type', 'CodeableConcept', count_max='*')
    typeReference = Property('typeReference', 'Reference', count_max='*')  # referencing 'Any'
    subtype = Property('subType', 'CodeableConcept', count_max='*')
    relationship = Property('relationship', 'Coding')
    context = Property('context', 'ContractTermAssetContext', count_max='*')
    condition = Property('condition', str)
    periodType = Property('periodType', 'CodeableConcept', count_max='*')
    period = Property('period', 'Period', count_max='*')
    usePeriod = Property('usePeriod', 'Period', count_max='*')
    text = Property('text', str)
    linkId = Property('linkId', str, count_max='*')
    answer = Property('answer', 'ContractTermOfferAnswer', count_max='*')
    securityLabelNumber = Property('securityLabelnumber', int, count_max='*')
    valuedItem = Property('valuedItem', 'ContractTermAssetValuedItem', count_max='*')


class ContractTermActionSubject(BackboneElement):

    reference = Property('reference', 'Reference', required=True, count_max='*')  # referencing 'Patient', 'RelatedPerson', ...
    role = Property('role', 'CodeableConcept')


class ContractTermAction(BackboneElement):

    doNotPerform = Property('doNotPerform', bool)
    type = Property('type', 'CodeableConcept', required=True)
    subject = Property('subject', 'ContractTermActionSubject', count_max='*')
    intent = Property('intent', 'CodeableConcept', required=True)
    linkId = Property('linkId', str, count_max='*')
    status = Property('status', 'CodeableConcept', required=True)
    context = Property('context', 'Reference')  # referencing 'Encounter' and 'EpisodeOfCare'
    contextLinkId = Property('contextLinkId', str, count_max='*')
    occurrenceDateTime = Property('occurrenceDateTime', 'FHIRDate')
    occurrencePeriod = Property('occurrencePeriod', 'Period')
    occurrenceTiming = Property('occurrenceTiming', 'Timing')
    requester = Property('requester', 'Reference', count_max='*')  # referencing 'Patient', 'RelatedPerson', ...
    requesterLinkId = Property('requesterLinkId', str, count_max='*')
    performerType = Property('performerType', 'CodeableConcept', count_max='*')
    performerRole = Property('performerRole', 'CodeableConcept')
    performer = Property('performer', 'Reference')  # referencing 'RelatedPerson', 'Patient', ...
    performerLinkId = Property('performerLinkId', str, count_max='*')
    reasonCode = Property('reasonCode', 'CodeableConcept', count_max='*')
    reasonReference = Property('reasonReference', 'Reference', count_max='*')  # referencing 'Condition', 'Observation', ...
    reason = Property('reason', str, count_max='*')
    reasonLinkId = Property('reasonLinkId', str, count_max='*')
    note = Property('note', 'Annotation', count_max='*')
    securityLabelNumber = Property('securityLabelNumber', int, count_max='*')


class ContractTerm(BackboneElement):

    identifier = Property('identifier', 'Identifier')
    issued = Property('issued', 'FHIRDate')
    applies = Property('applies', 'Period')
    topicCodeableConcept = Property('topicCodeableConcept', 'CodeableConcept')
    topicReference = Property('topicReference', 'Reference')  # referencing 'Any'
    type = Property('type', 'CodeableConcept')
    subType = Property('subType', 'CodeableConcept')
    text = Property('text', str)
    securityLabel = Property('securityLabel', 'ContractTermSecurityLabel', count_max='*')
    offer = Property('offer', 'ContractTermOffer', required=True)
    asset = Property('asset', 'ContractTermAsset', count_max='*')
    action = Property('action', 'ContractTermAction', count_max='*')
    group = Property('group', 'ContractTerm', count_max='*')


class ContractContentDefinition(BackboneElement):

    type = Property('type', 'CodeableConcept', required=True)
    subType = Property('subType', 'CodeableConcept')
    publisher = Property('publisher', 'Reference')  # referencing 'Practitioner', 'PractitionerRole' and 'Organization'
    publicationDate = Property('publicationDate', 'FHIRDate')
    publicationStatus = Property('publicationStatus', str, required=True)
    copyright = Property('copyright', 'Markdown')


class ContractSigner(BackboneElement):

    type = Property('type', 'Coding', required=True)
    party = Property('party', 'Reference', required=True)  # referencing 'Organization', 'Patient', ...
    signature = Property('signature', 'Signature', required=True, count_max='*')


class ContractFriendly(BackboneElement):

    contentAttachment = Property('contentAttachment', 'Attachment', required=True)
    contentReference = Property('contentReference', 'Reference', required=True)  # referencing 'Composition', ...


class ContractLegal(BackboneElement):

    contentAttachment = Property('contentAttachment', 'Attachment', required=True)
    contentReference = Property('contentReference', 'Reference', required=True)  # referencing 'Composition', ...


class ContractRule(BackboneElement):

    contentAttachment = Property('contentAttachment', 'Attachment', required=True)
    contentReference = Property('contentReference', 'Reference', required=True)  # referencing 'DocumentReference'


class Contract(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    url = Property('url', str)
    version = Property('version', str)
    status = Property('status', str)  # amended | appended | cancelled | disputed | entered-in-error | executable ...
    legalState = Property('legalState', 'CodeableConcept')
    instantiatesCanonical = Property('instantiatesCanonical', 'Reference')  # referencing 'Contract'
    instantiatesUri = Property('instantiatesUri', str)
    contentDerivative = Property('contentDerivative', 'CodeableConcept')
    issued = Property('issued', 'FHIRDate')
    applies = Property('applies', 'Period')
    expirationType = Property('expirationType', 'CodeableConcept')
    subject = Property('subject', 'Reference', count_max='*')  # referencing `Any`
    authority = Property('authority', 'Reference', count_max='*')  # referencing `Organization`
    domain = Property('domain', 'Reference', count_max='*')  # referencing `Location`
    site = Property('site', 'Reference', count_max='*')  # referencing 'Location'
    name = Property('name', str)
    title = Property('title', str)
    subtitle = Property('subtitle', str)
    alias = Property('alias', str, count_max='*')
    author = Property('author', 'Reference')  # referencing 'Patient', 'Practitioner', PractitionerRole' and 'Organization'
    scope = Property('scope', 'CodeableConcept')
    topicCodeableConcept = Property('topicCodeableConcept', 'CodeableConcept')
    topicReference = Property('topicReference', 'Reference')  # referencing 'Any'
    type = Property('type', 'CodeableConcept')
    subType = Property('subType', 'CodeableConcept', count_max='*')
    contentDefinition = Property('contentDefinition', 'ContractContentDefinition')
    term = Property('term', 'ContractTerm', count_max='*')
    supportingInfo = Property('supportingInfo', 'Reference', count_max='*')  # referencing 'Any'
    relevantHistory = Property('relevantHistory', 'Reference', count_max='*')  # referencing 'Provenance'
    signer = Property('signer', 'ContractSigner', count_max='*')
    friendly = Property('friendly', 'ContractFriendly', count_max='*')
    legal = Property('legal', 'ContractLegal', count_max='*')
    rule = Property('rule', 'ContractRule', count_max='*')
    legallyBindingAttachment = Property('legallyBindingAttachment', 'Attachment')
    legallyBindingReference = Property('legallyBindingReference', 'Reference')  # referencing 'Composition', ...


