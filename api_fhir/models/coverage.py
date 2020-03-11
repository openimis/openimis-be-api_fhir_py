from api_fhir.models import DomainResource, Property, BackboneElement


class CoverageGrouping(BackboneElement):
    group = Property('group', str)
    groupDisplay = Property('groupDisplay', str)
    subGroup = Property('subGroup', str)
    subGroupDisplay = Property('subGroupDisplay', str)
    plan = Property('plan', str)
    planDisplay = Property('planDisplay', str)
    subPlan = Property('subPlan', str)
    subPlanDisplay = Property('subPlanDisplay', str)
    clazz = Property('clazz', str)
    classDisplay = Property('classDisplay', str)
    subClass = Property('subClass', str)
    subClassDisplay = Property('subClassDisplay', str)


class Coverage(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    status = Property('status', str)  # active | cancelled | draft | entered-in-error
    type = Property('type', 'CodeableConcept')
    policyHolder = Property('policyHolder', 'Reference')  # referencing `Patient` | `RelatedPerson` | `Organization`
    subscriber = Property('subscriber', 'Reference')  # referencing `Patient` | `RelatedPerson`
    subscriberId = Property('subscriberId', str)
    beneficiary = Property('beneficiary', 'Reference')  # referencing `Patient`
    relationship = Property('relationship', 'CodeableConcept')
    period = Property('period', 'Period')
    payor = Property('payor', 'Reference', count_max='*')  # referencing `Patient` | `RelatedPerson` | `Organization`
    grouping = Property('grouping', 'CoverageGrouping')
    dependent = Property('dependent', str)
    sequence = Property('sequence', str)
    order = Property('order', int)
    network = Property('network', str)
    contract = Property('contract', 'Reference', count_max='*')  # referencing `Contract`
