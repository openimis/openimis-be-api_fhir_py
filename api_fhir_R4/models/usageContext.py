from api_fhir_R4.models import Property, Element
from enum import Enum


class UsageContext(Element):

    code = Property('code', 'Coding', required=True)
    valueCodeableConcept = Property('valueCodeableConcept', 'CodeableConcept', required=True)
    valueQuantity = Property('valueQuantity', 'Quantity', required=True)
    valueRange = Property('valueRange', 'Range', required=True)
    valueReference = Property('valueReference', 'Reference', required=True)  # referencing 'PlanDefinition',
    # 'ResearchStudy', 'InsurancePlan', 'HealthcareService', 'Group', 'Location' and 'Organization'


class UsageContextType(Enum):

    GENDER = 'gender'
    AGE_RANGE = 'age'
    CLINICAL_FOCUS = 'focus'
    USER_TYPE = 'user'
    WORKFLOW_SETTING = 'workflow'
    WORKFLOW_TASK = 'task'
    CLINICAL_VENUE = 'venue'
    SPECIES = 'species'
    PROGRAM = 'program'
