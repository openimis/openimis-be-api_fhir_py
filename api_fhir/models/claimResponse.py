from api_fhir.models import DomainResource, Property, BackboneElement


class ClaimResponseInsurance(BackboneElement):

    sequence = Property('sequence', int, required=True)
    focal = Property('focal', bool, required=True)
    coverage = Property('coverage', 'Reference', required=True)  # referencing `Coverage`
    businessArrangement = Property('businessArrangement', str)
    preAuthRef = Property('preAuthRef', str, count_max='*')
    claimResponse = Property('claimResponse', 'Reference')  # referencing `ClaimResponse`


class ClaimResponseProcessNote(BackboneElement):

    number = Property('number', int)
    type = Property('type', 'CodeableConcept')
    text = Property('text', str)
    language = Property('language', 'CodeableConcept')


class ClaimResponsePayment(BackboneElement):

    type = Property('type', 'CodeableConcept')
    adjustment = Property('adjustment', 'Money')
    adjustmentReason = Property('adjustmentReason', 'CodeableConcept')
    date = Property('date', 'FHIRDate')
    amount = Property('amount', 'Money')
    identifier = Property('identifier', 'Identifier')


class ClaimResponseError(BackboneElement):

    sequenceLinkId = Property('sequenceLinkId', int)
    detailSequenceLinkId = Property('detailSequenceLinkId', int)
    subdetailSequenceLinkId = Property('subdetailSequenceLinkId', int)
    code = Property('code', 'CodeableConcept', required=True)


class ClaimResponseAddItemDetail(BackboneElement):

    revenue = Property('revenue', 'CodeableConcept')
    category = Property('category', 'CodeableConcept')
    service = Property('service', 'CodeableConcept')
    modifier = Property('modifier', 'CodeableConcept', count_max='*')
    fee = Property('fee', 'Money')
    noteNumber = Property('noteNumber', int, count_max="*")
    adjudication = Property('adjudication', 'ClaimResponseItemAdjudication', count_max="*")


class ClaimResponseAddItem(BackboneElement):

    sequenceLinkId = Property('sequenceLinkId', int, count_max='*')
    revenue = Property('revenue', 'CodeableConcept')
    category = Property('category', 'CodeableConcept')
    service = Property('service', 'CodeableConcept')
    modifier = Property('modifier', 'CodeableConcept', count_max='*')
    fee = Property('fee', 'Money')
    noteNumber = Property('noteNumber', int, count_max="*")
    adjudication = Property('adjudication', 'ClaimResponseItemAdjudication', count_max="*")
    detail = Property('detail', 'ClaimResponseAddItemDetail', count_max="*")


class ClaimResponseItemSubDetail(BackboneElement):

    sequenceLinkId = Property('sequence', int, required=True)
    noteNumber = Property('noteNumber', int, count_max="*")
    adjudication = Property('adjudication', 'ClaimResponseItemAdjudication', count_max="*")


class ClaimResponseItemDetail(BackboneElement):

    sequenceLinkId = Property('sequence', int, required=True)
    noteNumber = Property('noteNumber', int, count_max="*")
    adjudication = Property('adjudication', 'ClaimResponseItemAdjudication', count_max="*")
    subDetail = Property('subDetail', 'ClaimResponseItemSubDetail', count_max="*")


class ClaimResponseItemAdjudication(BackboneElement):

    category = Property('category', 'CodeableConcept', required=True)
    reason = Property('reason', 'CodeableConcept')
    amount = Property('amount', 'Money')
    value = Property('value', float)


class ClaimResponseItem(BackboneElement):

    sequenceLinkId = Property('sequenceLinkId', int, required=True)
    noteNumber = Property('noteNumber', int, count_max="*")
    adjudication = Property('adjudication', 'ClaimResponseItemAdjudication', count_max="*")
    detail = Property('detail', 'ClaimResponseItemDetail', count_max="*")


class ClaimResponse(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    status = Property('status', str)
    patient = Property('patient', 'Reference')  # referencing `Patient`
    created = Property('created', 'FHIRDate')
    insurer = Property('insurer', 'Reference')  # referencing `Organization`
    requestProvider	= Property('requestProvider', 'Reference')  # referencing `Practitioner`
    requestOrganization = Property('requestOrganization', 'Reference')  # referencing `Organization`
    request = Property('request', 'Reference')  # referencing `Claim`
    outcome = Property('outcome', 'CodeableConcept')
    disposition = Property('disposition', str)
    payeeType = Property('payeeType', 'CodeableConcept')
    item = Property('item', 'ClaimResponseItem', count_max='*')
    addItem = Property('addItem', 'ClaimResponseAddItem', count_max='*')
    error = Property('error', 'ClaimResponseError', count_max='*')
    totalCost = Property('totalCost', 'Money')
    unallocDeductable = Property('unallocDeductable', 'Money')
    totalBenefit = Property('totalBenefit', 'Money')
    payment = Property('payment', 'ClaimResponsePayment')
    reserved = Property('reserved', 'Coding')
    form = Property('form', 'CodeableConcept')
    processNote = Property('processNote', 'ClaimResponseProcessNote', count_max='*')
    communicationRequest = Property('communicationRequest', 'Reference', count_max='*')  # referencing `CommunicationRequest`
    insurance = Property('insurance', 'ClaimResponseInsurance', count_max='*')
