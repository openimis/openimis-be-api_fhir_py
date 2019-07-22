from api_fhir.models import DomainResource, Property


class EligibilityRequest(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    status = Property('status', str)  # active | cancelled | draft | entered-in-error
    priority = Property('priority', 'CodeableConcept')
    patient = Property('patient', 'Reference')  # referencing `Patient`
    servicedDate = Property('servicedDate', 'FHIRDate')
    servicedPeriod = Property('servicedPeriod', 'Period')
    created = Property('created', 'FHIRDate')
    enterer = Property('enterer', 'Reference')  # referencing `Practitioner`
    provider = Property('provider', 'Reference')  # referencing `Practitioner`
    organization = Property('organization', 'Reference')  # referencing `Organization`
    insurer = Property('insurer', 'Reference')  # referencing `Organization`
    facility = Property('facility', 'Reference')  # referencing `Location`
    coverage = Property('coverage', 'Reference')  # referencing `Coverage`
    businessArrangement = Property('businessArrangement', str)
    benefitCategory = Property('benefitCategory', 'CodeableConcept')
    benefitSubCategory = Property('benefitSubCategory', 'CodeableConcept')
