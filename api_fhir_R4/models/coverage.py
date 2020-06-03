from api_fhir_R4.models import DomainResource, Property, BackboneElement


class CoverageClass(BackboneElement):

    type = Property('type', 'CodeableConcept', required=True)
    value = Property('value', str, required=True)
    name = Property('name', str)


class CoverageCostToBeneficiaryException(BackboneElement):

    type = Property('type', 'CodeableConcept', required=True)
    period = Property('period', 'Period')


class CoverageCostToBeneficiary(BackboneElement):

    type = Property('type', 'CodeableConcept')
    valueSimpleQuantity = Property('valueSimpleQuantity', 'Quantity', required=True)
    valueMoney = Property('valueMoney', 'Money', required=True)
    exception = Property('exception', 'CoverageCostToBeneficiaryException', count_max='*')


class Coverage(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    status = Property('status', str, required=True)  # active | cancelled | draft | entered-in-error
    type = Property('type', 'CodeableConcept')
    policyHolder = Property('policyHolder', 'Reference')  # referencing `Patient` | `RelatedPerson` | `Organization`
    subscriber = Property('subscriber', 'Reference')  # referencing `Patient` | `RelatedPerson`
    subscriberId = Property('subscriberId', str)
    beneficiary = Property('beneficiary', 'Reference', required=True)  # referencing `Patient`
    dependent = Property('dependent', str)
    relationship = Property('relationship', 'CodeableConcept')
    period = Property('period', 'Period')
    payor = Property('payor', 'Reference', required=True, count_max='*')  # referencing `Patient` | `RelatedPerson` | `Organization`
    class_ = Property('class', 'CoverageClass', count_max='*')
    order = Property('order', int)
    network = Property('network', str)
    costToBeneficiary = Property('costToBeneficiary', 'CoverageCostToBeneficiary', count_max='*')
    subrogation = Property('subrogation', bool)
    contract = Property('contract', 'Reference', count_max='*')  # referencing `Contract`
