from api_fhir_R4.models import DomainResource, Property, BackboneElement


class CoverageEligibilityResponseError(BackboneElement):

    code = Property('code', 'CodeableConcept', required=True)


class CoverageEligibilityResponseInsuranceItemBenefit(BackboneElement):

    type = Property('type', 'CodeableConcept', required=True)
    allowedUnsignedInt = Property('allowedUnsignedInt', int)
    allowedString = Property('allowedString', str)
    allowedMoney = Property('allowedMoney', 'Money')
    usedUnsignedInt = Property('usedUnsignedInt', int)
    usedString = Property('usedString', str)
    usedMoney = Property('usedMoney', 'Money')


class CoverageEligibilityResponseInsuranceItem(BackboneElement):

    category = Property('category', 'CodeableConcept')
    productOrService = Property('productOrService', 'CodeableConcept')
    modifier = Property('modifier', 'CodeableConcept', count_max='*')
    provider = Property('provider', 'Reference')  # referencing 'Practitioner' and 'PractitionerRole'
    excluded = Property('excluded', bool)
    name = Property('name', str)
    description = Property('description', str)
    network = Property('network', 'CodeableConcept')
    unit = Property('unit', 'CodeableConcept')
    term = Property('term', 'CodeableConcept')
    benefit = Property('benefit', 'CoverageEligibilityResponseInsuranceItemBenefit', count_max='*')
    authorizationRequired = Property('authorizationRequired', bool)
    authorizationSupporting = Property('authorizationSupporting', 'CodeableConcept', count_max='*')
    authorizationUrl = Property('authorizationUrl', str)


class CoverageEligibilityResponseInsurance(BackboneElement):

    coverage = Property('coverage', 'Reference', required=True)  # referencing 'Coverage'
    inforce = Property('inforce', bool)
    benefitPeriod = Property('benefitPeriod', 'Period')
    item = Property('item', 'CoverageEligibilityResponseInsuranceItem', count_max='*')


class CoverageEligibilityResponse(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    status = Property('status', str, required=True)  # active | cancelled | draft | entered-in-error
    purpose = Property('purpose', str, required=True, count_max='*')  # auth-requirements | benefits | discovery | validation
    patient = Property('patient', 'Reference', required=True)  # referencing 'Patient'
    servicedDate = Property('servicedDate', 'FHIRDate')
    servicedPeriod = Property('servicedPeriod', 'Period')
    created = Property('created', 'FHIRDate', required=True)
    requestor = Property('requestor', 'Reference')  # referencing 'Practitioner', 'PractitionerRole' and 'Organization'
    request = Property('request', 'Reference', required=True)  # referencing `CoverageEligibilityRequest`
    outcome = Property('outcome', str, required=True)  # RemittanceOutcome
    disposition = Property('disposition', str)
    insurer = Property('insurer', 'Reference', required=True)  # referencing `Organization`
    insurance = Property('insurance', 'CoverageEligibilityResponseInsurance', count_max='*')
    preAuthRef = Property('preAuthRef', str)
    form = Property('form', 'CodeableConcept')
    error = Property('error', 'CoverageEligibilityResponseError', count_max='*')
