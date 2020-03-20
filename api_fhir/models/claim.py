from api_fhir.models import DomainResource, Property, BackboneElement


class ClaimRelated(BackboneElement):

    claim = Property('claim', 'Reference')  # referencing `Claim`
    relationship = Property('relationship', 'CodeableConcept')
    reference = Property('reference', 'Identifier')


class ClaimPayee(BackboneElement):

    type = Property('type', 'CodeableConcept')
    resourceType = Property('resourceType', 'Coding')
    party = Property('party', 'Reference')  # referencing `Practitioner` | `Organization` | `Patient` | `RelatedPerson`


class ClaimCareTeam(BackboneElement):

    sequence = Property('sequence', int, required=True)
    provider = Property('provider', 'Reference', required=True)  # referencing `Practitioner` | `Organization`
    responsible = Property('responsible', bool)
    role = Property('role', 'CodeableConcept')
    qualification = Property('qualification', 'CodeableConcept')


class ClaimInformation(BackboneElement):

    sequence = Property('sequence', int, required=True)
    category = Property('category', 'CodeableConcept', required=True)
    code = Property('code', 'CodeableConcept')
    timingDate = Property('timingDate', 'FHIRDate')
    timingPeriod = Property('timingPeriod', 'Period')
    valueString = Property('valueString', str)
    valueQuantity = Property('valueString', 'Quantity')
    valueAttachment = Property('valueString', 'Attachment')
    valueReference = Property('valueReference', 'Reference')  # referencing `Any`
    reason = Property('reason', 'CodeableConcept')


class ClaimDiagnosis(BackboneElement):

    sequence = Property('sequence', int, required=True)
    diagnosisCodeableConcept = Property('diagnosisCodeableConcept', 'CodeableConcept')
    diagnosisReference = Property('diagnosisReference', 'Reference')  # referencing `Condition`
    type = Property('type', 'CodeableConcept', count_max='*')
    packageCode = Property('packageCode', 'CodeableConcept')


class ClaimProcedure(BackboneElement):

    sequence = Property('sequence', int, required=True)
    date = Property('date', 'FHIRDate')
    procedureCodeableConcept = Property('procedureCodeableConcept', 'CodeableConcept')
    procedureReference = Property('procedureReference', 'Reference')  # referencing `Procedure`


class ClaimInsurance(BackboneElement):

    sequence = Property('sequence', int, required=True)
    focal = Property('focal', bool, required=True)
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
    service = Property('service', 'CodeableConcept')
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
    service = Property('service', 'CodeableConcept')
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
    careTeamLinkId = Property('careTeamLinkId', int, count_max='*')
    diagnosisLinkId = Property('diagnosisLinkId', int, count_max='*')
    procedureLinkId = Property('procedureLinkId', int, count_max='*')
    informationLinkId = Property('informationLinkId', int, count_max='*')
    revenue = Property('revenue', 'CodeableConcept')
    category = Property('category', 'CodeableConcept')
    service = Property('service', 'CodeableConcept')
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
    status = Property('status', str)
    type = Property('type', 'CodeableConcept')
    subType = Property('subType', 'CodeableConcept', count_max='*')
    use = Property('use', str)
    patient = Property('patient', 'Reference')  # referencing `Patient`
    billablePeriod = Property('billablePeriod', 'Period')
    created = Property('created', 'FHIRDate')
    enterer = Property('enterer', 'Reference')  # referencing `Practitioner`
    insurer = Property('insurer', 'Reference')  # referencing `Organization`
    provider = Property('provider', 'Reference')  # referencing `Practitioner`
    organization = Property('organization', 'Reference')  # referencing `Organization`
    priority = Property('priority', 'CodeableConcept')
    fundsReserve = Property('fundsReserve', 'CodeableConcept')
    related = Property('related', 'ClaimRelated', count_max='*')
    prescription = Property('prescription', 'Reference')  # referencing `MedicationRequest` | `VisionPrescription`
    originalPrescription = Property('originalPrescription', 'Reference')  # referencing `MedicationRequest`
    payee = Property('payee', 'ClaimPayee')
    referral = Property('referral', 'Reference')  # referencing `ReferralRequest`
    facility = Property('facility', 'Reference')  # referencing `Location`
    careTeam = Property('careTeam', 'ClaimCareTeam')
    information = Property('information', 'ClaimInformation', count_max='*')
    diagnosis = Property('diagnosis', 'ClaimDiagnosis', count_max='*')
    procedure = Property('procedure', 'ClaimProcedure', count_max='*')
    insurance = Property('insurance', 'ClaimInsurance', count_max='*')
    accident = Property('accident', 'ClaimAccident')
    employmentImpacted = Property('employmentImpacted', 'Period')
    hospitalization = Property('hospitalization', 'Period')
    item = Property('item', 'ClaimItem', count_max='*')
    total = Property('total', 'Money')
