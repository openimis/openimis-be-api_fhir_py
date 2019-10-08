from api_fhir.models import DomainResource, Property, BackboneElement


class ContractAgent(BackboneElement):
    actor = Property('actor', 'Reference', required=True)  # referencing `Contract` | `Device` | `Group` | `Location`...
    role = Property('role', 'CodeableConcept', count_max='*')


class ContractSigner(BackboneElement):
    type = Property('type', 'Coding', required=True)
    party = Property('party', 'Reference', required=True)  # referencing `Organization` | `Patient` | `Practitioner` ...
    signature = Property('signature', 'Signature', required=True, count_max='*')


class ContractValuedItem(BackboneElement):
    entityCodeableConcept = Property('entityCodeableConcept', 'CodeableConcept')
    entityReference = Property('entityReference', 'Reference')  # referencing `Any`
    identifier = Property('identifier', 'Identifier')
    effectiveTime = Property('effectiveTime', 'FHIRDate')
    quantity = Property('quantity', 'Quantity')
    unitPrice = Property('unitPrice', 'Money')
    factor = Property('factor', float)
    points = Property('points', float)
    net = Property('net', 'Money')


class ContractTerm(BackboneElement):
    identifier = Property('identifier', 'Identifier')
    issued = Property('issued', 'FHIRDate')
    applies = Property('applies', 'Period')
    type = Property('type', 'CodeableConcept')
    subType = Property('subType', 'CodeableConcept')
    topic = Property('topic', 'Reference', count_max='*')  # referencing `Any`
    action = Property('action', 'CodeableConcept', count_max='*')
    actionReason = Property('actionReason', 'CodeableConcept', count_max='*')
    securityLabel = Property('securityLabel', 'Coding', count_max='*')
    agent = Property('agent', 'ContractAgent', count_max='*')
    text = Property('text', str)
    valuedItem = Property('valuedItem', 'ContractValuedItem', count_max='*')
    group = Property('group', 'ContractTerm', count_max='*')


class ContractFriendly(BackboneElement):
    contentAttachment = Property('contentAttachment', 'Attachment')
    contentReference = Property('contentReference', 'Reference')  # referencing `Composition` | `DocumentReference` ...


class ContractLegal(BackboneElement):
    contentAttachment = Property('contentAttachment', 'Attachment')
    contentReference = Property('contentReference', 'Reference')  # referencing `Composition` | `DocumentReference` ...


class ContractRule(BackboneElement):
    contentAttachment = Property('contentAttachment', 'Attachment')
    contentReference = Property('contentReference', 'Reference')  # referencing `DocumentReference`


class Contract(DomainResource):
    identifier = Property('identifier', 'Identifier')
    status = Property('status', str)  # amended | appended | cancelled | disputed | entered-in-error | executable ...
    issued = Property('issued', 'FHIRDate')
    applies = Property('applies', 'Period')
    subject = Property('subject', 'Reference', count_max='*')  # referencing `Any`
    topic = Property('topic', 'Reference', count_max='*')  # referencing `Any`
    authority = Property('authority', 'Reference', count_max='*')  # referencing `Organization`
    domain = Property('domain', 'Reference', count_max='*')  # referencing `Location`
    type = Property('type', 'CodeableConcept')
    subType = Property('subType', 'CodeableConcept', count_max='*')
    action = Property('action', 'CodeableConcept', count_max='*')
    actionReason = Property('actionReason', 'CodeableConcept', count_max='*')
    decisionType = Property('decisionType', 'CodeableConcept')
    contentDerivative = Property('contentDerivative', 'CodeableConcept')
    securityLabel = Property('securityLabel', 'Coding', count_max='*')
    agent = Property('agent', 'ContractAgent', count_max='*')
    signer = Property('signer', 'ContractSigner', count_max='*')
    valuedItem = Property('valuedItem', 'ContractValuedItem', count_max='*')
    term = Property('term', 'ContractTerm', count_max='*')
    bindingAttachment = Property('bindingAttachment', 'Attachment')
    bindingReference = Property('bindingReference', 'Reference')  # referencing `Composition` | `DocumentReference` ...
    friendly = Property('friendly', 'ContractFriendly', count_max='*')
    legal = Property('legal', 'ContractLegal', count_max='*')
    rule = Property('rule', 'ContractRule', count_max='*')
