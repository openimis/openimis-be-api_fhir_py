from api_fhir.models import DomainResource, Property, BackboneElement


class EligibilityResponseError(BackboneElement):

    code = Property('code', 'CodeableConcept', required=True)


class InsuranceBenefitBalanceFinancial(BackboneElement):

    type = Property('type', 'CodeableConcept', required=True)
    allowedUnsignedInt = Property('allowedUnsignedInt', int)
    allowedString = Property('allowedString', str)
    allowedMoney = Property('allowedMoney', 'Money')
    usedUnsignedInt = Property('usedUnsignedInt', int)
    usedMoney = Property('usedMoney', 'Money')


class InsuranceBenefitBalance(BackboneElement):

    category = Property('category', 'CodeableConcept', required=True)
    subCategory = Property('subCategory', 'CodeableConcept')
    excluded = Property('excluded', bool)
    name = Property('name', str)
    description = Property('description', str)
    network = Property('network', 'CodeableConcept')
    unit = Property('unit', 'CodeableConcept')
    term = Property('term', 'CodeableConcept')
    financial = Property('financial', 'InsuranceBenefitBalanceFinancial', count_max='*')


class EligibilityResponseInsurance(BackboneElement):

    coverage = Property('coverage', 'Reference')
    contract = Property('contract', 'Reference')
    benefitBalance = Property('benefitBalance', 'InsuranceBenefitBalance', count_max='*')


class EligibilityResponse(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    status = Property('status', str)
    created = Property('created', 'FHIRDate')
    requestProvider = Property('requestProvider', 'Reference')  # referencing `Practitioner`
    requestOrganization = Property('requestOrganization', 'Reference')  # referencing `Organization`
    request = Property('request', 'Reference')  # referencing `EligibilityRequest`
    outcome = Property('outcome', 'CodeableConcept')  # RemittanceOutcome
    disposition = Property('disposition', str)
    insurer = Property('insurer', 'Reference')  # referencing `Organization`
    inforce = Property('inforce', bool)
    insurance = Property('insurance', 'EligibilityResponseInsurance', count_max='*')
    form = Property('form', 'CodeableConcept')
    code = Property('code', 'EligibilityResponseError', count_max='*')
