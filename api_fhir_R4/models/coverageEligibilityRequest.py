from api_fhir_R4.models import DomainResource, Property, BackboneElement


class CoverageEligibilityRequestSupportingInfo(BackboneElement):

    sequence = Property('sequence', int, required=True)
    information = Property('information', 'Reference', required=True)  # referencing 'Any'
    appliesToAll = Property('appliesToAll', bool)


class CoverageEligibilityRequestInsurance(BackboneElement):

    focal = Property('focal', bool)
    coverage = Property('coverage', 'Reference', required=True)  # referencing 'Coverage'
    businessArrangement = Property('businessArrangement', str)


class CoverageEligibilityRequestItem(BackboneElement):

    supportingInfoSequence = Property('supportingInfoSequence', int, count_max='*')
    category = Property('category', 'CodeableConcept')                                                          # mapped
    productOrService = Property('productOrService', 'CodeableConcept')                                          # mapped
    modifier = Property('modifier', 'CodeableConcept', count_max='*')
    provider = Property('provider', 'Reference')  # referencing 'Practitioner' and 'PractitionerRole'
    quantity = Property('quantity', 'Quantity')
    unitPrice = Property('unitPrice', 'Money')
    facility = Property('facility', 'Reference')  # referencing 'Location' and 'Organization'
    diagnosisCodeableConcept = Property('diagnosisCodeableConcept', 'CodeableConcept')
    diagnosisReference = Property('diagnosisReference', 'Reference')  # referencing 'Condition'


class CoverageEligibilityRequest(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    status = Property('status', str, required=True)  # active | cancelled | draft | entered-in-error
    priority = Property('priority', 'CodeableConcept')
    purpose = Property('purpose', str, required=True, count_max='*')  # auth-requirements | benefits | discovery | validation
    patient = Property('patient', 'Reference', required=True)  # referencing `Patient`
    servicedDate = Property('servicedDate', 'FHIRDate')
    servicedPeriod = Property('servicedPeriod', 'Period')
    created = Property('created', 'FHIRDate', required=True)
    enterer = Property('enterer', 'Reference')  # referencing `Practitioner` and 'PractitionerRole'
    provider = Property('provider', 'Reference')  # referencing `Practitioner`, 'PractitionerRole' and 'Organization'
    insurer = Property('insurer', 'Reference', required=True)  # referencing `Organization`
    facility = Property('facility', 'Reference')  # referencing `Location`
    supportingInfo = Property('supportingInfo', 'CoverageEligibilityRequestSupportingInfo', count_max='*')
    insurance = Property('insurance', 'CoverageEligibilityRequestInsurance', count_max='*')
    item = Property('item', 'CoverageEligibilityRequestItem', count_max='*')
