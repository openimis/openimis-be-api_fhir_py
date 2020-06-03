from api_fhir_R4.models import DomainResource, BackboneElement, Property
from enum import Enum


class MedicationBatch(BackboneElement):

    lotNumber = Property('lotNumber', str)
    expirationDate = Property('expirationDate', 'FHIRDate')


class MedicationIngredient(BackboneElement):

    itemCodeableConcept = Property('itemCondeableConcept', 'CodeableConcept', required=True)
    itemReference = Property('itemReference', 'Reference', required=True)  # referencing 'Substance' and 'Medication'
    isActive = Property('isActive', bool)
    strength = Property('strength', 'Ratio')


class Medication(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    code = Property('code', 'CodeableConcept')
    status = Property('status', str)
    manufacturer = Property('manufacturer', 'Reference')  # referencing 'Organization'
    form = Property('form', 'CodeableConcept')
    amount = Property('amount', 'Ratio')
    ingredient = Property('ingredient', 'MedicationIngredient', count_max='*')
    batch = Property('batch', 'MedicationBatch')


class MedicationStatusCodes(Enum):

    ACTIVE = 'active'
    INACTIVE = 'inactive'
    ENTERED_IN_ERROR = 'entered-in-error'
