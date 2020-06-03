from api_fhir_R4.models import BackboneElement, DomainResource, Property
from enum import Enum


class ConditionEvidence(BackboneElement):

    code = Property('code', 'CodeableConcept', count_max='*')
    detail = Property('detail', 'Reference', count_max='*')  # referencing 'Any'


class ConditionStage(BackboneElement):

    summary = Property('summary', 'CodeableConcept')
    assessment = Property('assessment', 'Reference', count_max='*')  # referencing 'ClinicalImpression', ...
    type = Property('type', 'CodeableConcept')


class Condition(DomainResource):

    identifier = Property('identifier', 'Identifier', count_max='*')
    clinicalStatus = Property('clinicalStatus', 'CodeableConcept')
    verificationStatus = Property('verificationStatus', 'CodeableConcept')
    category = Property('category', 'CodeableConcept', count_max='*')
    severity = Property('severity', 'CodeableConcept')
    code = Property('code', 'CodeableConcept')
    bodySite = Property('bodySite', 'CodeableConcept', count_max='*')
    subject = Property('subject', 'Reference', required=True)  # referencing 'Patient' and 'Group'
    encounter = Property('encounter', 'Reference')  # referencing 'Encounter'
    onsetDateTime = Property('onsetDateTime', 'FHIRDate')
    onsetAge = Property('onsetAge', 'Age')
    onsetPeriod = Property('onsetPeriod', 'Period')
    onsetRange = Property('onsetRange', 'Range')
    onsetString = Property('onsetString', str)
    abatementDateTime = Property('abatementDateTime', 'FHIRDate')
    abatementAge = Property('abatementAge', 'Age')
    abatementPeriod = Property('abatementPeriod', 'Period')
    abatementRange = Property('abatementRange', 'Range')
    abatementString = Property('abatementString', str)
    recordedDate = Property('recordedDate', 'FHIRDate')
    recorder = Property('recorder', 'Reference')  # referencing 'Practitioner', 'PractitionerRole', ...
    asserter = Property('asserter', 'Reference')  # referencing 'Practitioner', 'PractitionerRole', ...
    stage = Property('stage', 'ConditionStage', count_max='*')
    evidence = Property('evidence', 'ConditionEvidence', count_max='*')
    note = Property('note', 'Annotation', count_max='*')


class ConditionClinicalStatusCodes(Enum):

    ACTIVE = 'active'
    RECURRENCE = 'recurrence'
    RELAPSE = 'relapse'
    INACTIVE = 'inactive'
    REMISSION = 'remission'
    RESOLVED = 'resolved'


class ConditionVerificationStatus(Enum):

    UNCONFIRMED = 'unconfirmed'
    PROVISIONAL = 'provisional'
    DIFFERENTIAL = 'differential'
    CONFIRMED = 'confirmed'
    REFUTED = 'refuted'
    ENTERED_IN_ERROR = 'entered-in-error'
