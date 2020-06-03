from medical.models import Diagnosis
from api_fhir_R4.converters import R4IdentifierConfig, BaseFHIRConverter
from api_fhir_R4.models.condition import Condition as FHIRCondition, ConditionStage, ConditionEvidence
from django.utils.translation import gettext

class ConditionConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, imis_condition):
        fhir_condition = FHIRCondition()
        cls.build_fhir_pk(fhir_condition, imis_condition.id)
        cls.build_fhir_identifiers(fhir_condition, imis_condition)
        cls.build_fhir_codes(fhir_condition, imis_condition)
        cls.build_fhir_recordedDate(fhir_condition, imis_condition)
        return fhir_condition

    @classmethod
    def to_imis_obj(cls, fhir_condition, audit_user_id):
        errors = []
        imis_condition = Diagnosis()
        cls.build_imis_identifier(imis_condition, fhir_condition, errors)
        cls.check_errors(errors)
        return imis_condition

    @classmethod
    def get_fhir_resource_type(cls):
        return FHIRCondition

    @classmethod
    def build_fhir_identifiers(cls, fhir_condition, imis_condition):
        identifiers = []


    @classmethod
    def build_imis_identifier(cls, imis_condition, fhir_condition, errors):
        value = cls.get_fhir_identifier_by_code(fhir_condition.identifier, R4IdentifierConfig.get_fhir_claim_code_type())
        if value:
            imis_condition.code = value
        cls.valid_condition(imis_condition.code is None, gettext('Missing the ICD code'), errors)


