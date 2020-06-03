from api_fhir_R4.models import DomainResource, Property, BackboneElement


class ClaimRelated(BackboneElement):

    claim = Property('claim', 'Reference')  # referencing `Claim`
    relationship = Property('relationship', 'CodeableConcept')
    reference = Property('reference', 'Identifier')


class ClaimPayee(BackboneElement):

    type = Property('type', 'CodeableConcept', required=True)
    party = Property('party', 'Reference')  # referencing `Practitioner` | `Organization` | `Patient` | `RelatedPerson`


class ClaimCareTeam(BackboneElement):

    sequence = Property('sequence', int, required=True)
    provider = Property('provider', 'Reference', required=True)  # referencing `Practitioner` | `Organization`
    responsible = Property('responsible', bool)
    role = Property('role', 'CodeableConcept')
    qualification = Property('qualification', 'CodeableConcept')


class ClaimSupportingInfo(BackboneElement):

    sequence = Property('sequence', int, required=True)
    category = Property('category', 'CodeableConcept', required=True)
    code = Property('code', 'CodeableConcept')
    timingDate = Property('timingDate', 'FHIRDate')
    timingPeriod = Property('timingPeriod', 'Period')
    valueBoolean = Property('valueBoolean', bool)
    valueString = Property('valueString', str)
    valueQuantity = Property('valueString', 'Quantity')
    valueAttachment = Property('valueString', 'Attachment')
    valueReference = Property('valueReference', 'Reference')  # referencing `Any`
    reason = Property('reason', 'CodeableConcept')


class ClaimDiagnosis(BackboneElement):

    sequence = Property('sequence', int, required=True)
    diagnosisCodeableConcept = Property('diagnosisCodeableConcept', 'CodeableConcept', required=True)
    diagnosisReference = Property('diagnosisReference', 'Reference', required=True)  # referencing `Condition`
    type = Property('type', 'CodeableConcept', count_max='*')
    onAdmission = Property('onAdmission', 'CodeableConcept')
    packageCode = Property('packageCode', 'CodeableConcept')


class ClaimProcedure(BackboneElement):

    sequence = Property('sequence', int, required=True)
    type = Property('type', 'CodeableConcept', count_max='*')
    date = Property('date', 'FHIRDate')
    procedureCodeableConcept = Property('procedureCodeableConcept', 'CodeableConcept', required=True)
    procedureReference = Property('procedureReference', 'Reference', required=True)  # referencing `Procedure`
    udi = Property('udi', 'Reference', count_max='*')  # referencing 'Device'


class ClaimInsurance(BackboneElement):

    sequence = Property('sequence', int, required=True)
    focal = Property('focal', bool, required=True)
    identifier = Property('identifier', 'Identifier')
    coverage = Property('coverage', 'Reference', required=True)  # referencing `Coverage`
    businessArrangement = Property('businessArrangement', str)
    preAuthRef = Property('preAuthRef', str, count_max='*')
    claimResponse = Property('claimResponse', 'Reference')  # referencing `ClaimResponse`


class ClaimAccident(BackboneElement):

    date = Property('date', 'FHIRDate', required=True)
    type = Property('type', 'CodeableConcept')
    locationAddress = Property('locationAddress', 'Address')
    locationReference = Property('locationReference', 'Reference')  # referencing `Location`


class ClaimItemDetailSubDetail(BackboneElement):

    sequence = Property('sequence', int, required=True)
    revenue = Property('revenue', 'CodeableConcept')
    category = Property('category', 'CodeableConcept')
    productOrService = Property('productOrService', 'CodeableConcept', required=True)
    modifier = Property('modifier', 'CodeableConcept', count_max='*')
    programCode = Property('programCode', 'CodeableConcept', count_max='*')
    quantity = Property('quantity', 'Quantity')
    unitPrice = Property('unitPrice', 'Money')
    factor = Property('factor', float)
    net = Property('net', 'Money')
    udi = Property('udi', 'Reference', count_max='*')  # referencing `Device`


class ClaimItemDetail(BackboneElement):

    sequence = Property('sequence', int, required=True)
    revenue = Property('revenue', 'CodeableConcept')
    category = Property('category', 'CodeableConcept')
    productOrService = Property('productOrService', 'CodeableConcept', required=True)
    modifier = Property('modifier', 'CodeableConcept', count_max='*')
    programCode = Property('programCode', 'CodeableConcept', count_max='*')
    quantity = Property('quantity', 'Quantity')
    unitPrice = Property('unitPrice', 'Money')
    factor = Property('factor', float)
    net = Property('net', 'Money')
    udi = Property('udi', 'Reference', count_max='*')  # referencing `Device`
    subDetail = Property('subDetail', 'ClaimItemDetailSubDetail', count_max='*')


class ClaimItem(BackboneElement):

    sequence = Property('sequence', int, required=True)
    careTeamSequence = Property('careTeamSequence', int, count_max='*')
    diagnosisSequence = Property('diagnosisSequence', int, count_max='*')
    procedureSequence = Property('procedureSequence', int, count_max='*')
    informationSequence = Property('informationSequence', int, count_max='*')
    revenue = Property('revenue', 'CodeableConcept')
    category = Property('category', 'CodeableConcept')
    productOrService = Property('productOrService', 'CodeableConcept', required=True)
    modifier = Property('modifier', 'CodeableConcept', count_max='*')
    programCode = Property('programCode', 'CodeableConcept', count_max='*')
    servicedDate = Property('servicedDate', 'FHIRDate')
    servicedPeriod = Property('servicedPeriod', 'Period')
    locationCodeableConcept = Property('locationCodeableConcept', 'CodeableConcept')
    locationAddress = Property('locationAddress', 'Address')
    locationReference = Property('locationReference', 'Reference')  # referencing `Location`
    quantity = Property('quantity', 'Quantity')
    unitPrice = Property('unitPrice', 'Money')
    factor = Property('factor', float)
    net = Property('net', 'Money')
    udi = Property('udi', 'Reference', count_max='*')  # referencing `Device`
    bodySite = Property('bodySite', 'CodeableConcept')
    subSite = Property('subSite', 'CodeableConcept', count_max='*')
    encounter = Property('encounter', 'Reference', count_max='*')  # referencing `Encounter`
    detail = Property('detail', 'ClaimItemDetail', count_max='*')


class Claim(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    status = Property('status', str, required=True)
    type = Property('type', 'CodeableConcept', required=True)
    subType = Property('subType', 'CodeableConcept')
    use = Property('use', str, required=True)
    patient = Property('patient', 'Reference', required=True)  # referencing `Patient`
    billablePeriod = Property('billablePeriod', 'Period')
    created = Property('created', 'FHIRDate', required=True)
    enterer = Property('enterer', 'Reference')  # referencing `Practitioner`
    insurer = Property('insurer', 'Reference')  # referencing `Organization`
    provider = Property('provider', 'Reference', required=True)  # referencing `Practitioner`
    priority = Property('priority', 'CodeableConcept', required=True)
    fundsReserve = Property('fundsReserve', 'CodeableConcept')
    related = Property('related', 'ClaimRelated', count_max='*')
    prescription = Property('prescription', 'Reference')  # referencing `MedicationRequest` | `VisionPrescription`
    originalPrescription = Property('originalPrescription', 'Reference')  # referencing `MedicationRequest`
    payee = Property('payee', 'ClaimPayee')
    referral = Property('referral', 'Reference')  # referencing `ReferralRequest`
    facility = Property('facility', 'Reference')  # referencing `Location`
    careTeam = Property('careTeam', 'ClaimCareTeam', count_max='*')
    supportingInfo = Property('supportingInfo', 'ClaimSupportingInfo', count_max='*')
    diagnosis = Property('diagnosis', 'ClaimDiagnosis', count_max='*')
    procedure = Property('procedure', 'ClaimProcedure', count_max='*')
    insurance = Property('insurance', 'ClaimInsurance', required=True, count_max='*')
    accident = Property('accident', 'ClaimAccident')
    item = Property('item', 'ClaimItem', count_max='*')
    total = Property('total', 'Money')
