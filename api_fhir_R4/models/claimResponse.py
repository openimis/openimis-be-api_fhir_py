from api_fhir_R4.models import DomainResource, Property, BackboneElement


class ClaimResponseInsurance(BackboneElement):

    sequence = Property('sequence', int, required=True)
    focal = Property('focal', bool, required=True)
    coverage = Property('coverage', 'Reference', required=True)  # referencing `Coverage`
    businessArrangement = Property('businessArrangement', str)
    claimResponse = Property('claimResponse', 'Reference')  # referencing `ClaimResponse`


class ClaimResponseProcessNote(BackboneElement):

    number = Property('number', int)
    type = Property('type', str)
    text = Property('text', str, required=True)
    language = Property('language', 'CodeableConcept')


class ClaimResponsePayment(BackboneElement):

    type = Property('type', 'CodeableConcept', required=True)
    adjustment = Property('adjustment', 'Money')
    adjustmentReason = Property('adjustmentReason', 'CodeableConcept')
    date = Property('date', 'FHIRDate')
    amount = Property('amount', 'Money', required=True)
    identifier = Property('identifier', 'Identifier')


class ClaimResponseError(BackboneElement):

    itemSequence = Property('itemSequence', int)
    detailSequence = Property('detailSequence', int)
    subDetailSequence = Property('subDetailSequenceLinkId', int)
    code = Property('code', 'CodeableConcept', required=True)


class ClaimResponseTotal(BackboneElement):

    category = Property('category', 'CodeableConcept', required=True)
    amount = Property('amount', 'Money', required=True)


class ClaimResponseAddItemDetailSubDetail(BackboneElement):

    productOrService = Property('productOrService', 'CodeableConcept', required=True)
    modifier = Property('modifier', 'CodeableConcept', count_max='*')
    quantity = Property('quantity', 'Quantity')
    unitPrice = Property('unitPrice', 'Money')
    factor = Property('factor', float)
    net = Property('net', 'Money')
    noteNumber = Property('noteNumber', int, count_max='*')
    adjucation = Property('adjucation', 'ClaimResponseItemAdjucation', required=True, count_max='*')


class ClaimResponseAddItemDetail(BackboneElement):

    productOrService = Property('productOrService', 'CodeableConcept', required=True)
    modifier = Property('modifier', 'CodeableConcept', count_max='*')
    quantity = Property('quantity', 'Quantity')
    unitPrice = Property('unitPrice', 'Money')
    factor = Property('factor', float)
    net = Property('net', 'Money')
    noteNumber = Property('noteNumber', int, count_max="*")
    adjudication = Property('adjudication', 'ClaimResponseItemAdjudication', required=True, count_max='*')
    subDetail = Property('subDetail', 'ClaimResponseAddItemDetailSubDetail', count_max='*')


class ClaimResponseAddItem(BackboneElement):

    itemSequence = Property('itemSequence', int, count_max='*')
    detailSequence = Property('detailSequence', int, count_max='*')
    subDetailSequence = Property('subDetailSequence', int, count_max='*')
    provider = Property('provider', 'Reference', count_max='*')  # referencing 'Practitioner', ...
    productOrService = Property('productOrService', 'CodeableConcept', required=True)
    modifier = Property('modifier', 'CodeableConcept', count_max='*')
    programCode = Property('programCode', 'CodeableConcept', count_max='*')
    servicedDate = Property('servicedDate', 'FHIRDate')
    servicedPeriod = Property('servicedPeriod', 'Period')
    locationCodeableConcept = Property('locationCodeableConcept', 'CodeableConcept')
    locationAddress = Property('locationAddress', 'Address')
    locationReference = Property('locationReference', 'Reference')  # referencing 'Location'
    quantity = Property('quantity', 'Quantity')
    unitPrice = Property('unitPrice', 'Money')
    factor = Property('factor', float)
    net = Property('net', 'Money')
    bodySite = Property('bodySite', 'CodeableConcept')
    subSite = Property('subSite', 'CodeableConcept', count_max='*')
    noteNumber = Property('noteNumber', int, count_max="*")
    adjudication = Property('adjudication', 'ClaimResponseItemAdjudication', required=True, count_max='*')
    detail = Property('detail', 'ClaimResponseAddItemDetail', count_max="*")


class ClaimResponseItemDetailSubDetail(BackboneElement):

    subDetailSequence = Property('subDetailSequence', int, required=True)
    noteNumber = Property('noteNumber', int, count_max="*")
    adjudication = Property('adjudication', 'ClaimResponseItemAdjudication', count_max="*")


class ClaimResponseItemDetail(BackboneElement):

    detailSequence = Property('detailSequence', int, required=True)
    noteNumber = Property('noteNumber', int, count_max="*")
    adjudication = Property('adjudication', 'ClaimResponseItemAdjudication', required=True, count_max='*')
    subDetail = Property('subDetail', 'ClaimResponseItemDetailSubDetail', count_max="*")


class ClaimResponseItemAdjudication(BackboneElement):

    category = Property('category', 'CodeableConcept', required=True)
    reason = Property('reason', 'CodeableConcept')
    amount = Property('amount', 'Money')
    value = Property('value', float)


class ClaimResponseItem(BackboneElement):

    itemSequence = Property('itemSequence', int, required=True)
    noteNumber = Property('noteNumber', int, count_max="*")
    adjudication = Property('adjudication', 'ClaimResponseItemAdjudication', required=True, count_max='*')
    detail = Property('detail', 'ClaimResponseItemDetail', count_max="*")


class ClaimResponse(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    status = Property('status', str, required=True)
    type = Property('type', 'CodeableConcept', required=True)
    subType = Property('subType', 'CodeableConcept')
    use = Property('use', str, required=True)
    patient = Property('patient', 'Reference', required=True)  # referencing `Patient`
    created = Property('created', 'FHIRDate', required=True)
    insurer = Property('insurer', 'Reference', required=True)  # referencing `Organization`
    requestor = Property('requestor', 'Reference')  # referencing 'Practitioner', 'PractitionerRole' and 'Organization'
    request = Property('request', 'Reference')  # referencing `Claim`
    outcome = Property('outcome', str, required=True)
    disposition = Property('disposition', str)
    preAuthRef = Property('preAuthRef', str)
    preAuthPeriod = Property('preAuthPeriod', 'Period')
    payeeType = Property('payeeType', 'CodeableConcept')
    item = Property('item', 'ClaimResponseItem', count_max='*')
    addItem = Property('addItem', 'ClaimResponseAddItem', count_max='*')
    adjucation = Property('adjucation', 'ClaimResponseItemAdjucation', count_max='*')
    total = Property('total', 'ClaimResponseTotal', count_max='*')
    payment = Property('payment', 'ClaimResponsePayment')
    fundsReserve = Property('fundsReserve', 'CodeableConcept')
    formCode = Property('formCode', 'CodeableConcept')
    form = Property('form', 'Attachment')
    processNote = Property('processNote', 'ClaimResponseProcessNote', count_max='*')
    communicationRequest = Property('communicationRequest', 'Reference', count_max='*')  # referencing `CommunicationRequest`
    insurance = Property('insurance', 'ClaimResponseInsurance', count_max='*')
    error = Property('error', 'ClaimResponseError', count_max='*')
