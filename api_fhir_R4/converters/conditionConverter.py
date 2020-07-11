from medical.models import Diagnosis
from insuree.models import Insuree
from api_fhir_R4.converters import R4IdentifierConfig, BaseFHIRConverter, ReferenceConverterMixin, PatientConverter
from api_fhir_R4.models.condition import Condition as FHIRCondition
from api_fhir_R4.models import Reference
from django.utils.translation import gettext
from api_fhir_R4.utils import DbManagerUtils, TimeUtils


class ConditionConverter(BaseFHIRConverter, ReferenceConverterMixin):

    @classmethod
    def to_fhir_obj(cls, imis_condition):
        fhir_condition = FHIRCondition()
        cls.build_fhir_pk(fhir_condition, str(imis_condition.id))  # id as string because of db, has to be changed to uuid
        cls.build_fhir_identifiers(fhir_condition, imis_condition)
        cls.build_fhir_codes(fhir_condition, imis_condition)
        cls.build_fhir_recorded_date(fhir_condition, imis_condition)
        cls.build_fhir_subject(fhir_condition)
        return fhir_condition

    @classmethod
    def to_imis_obj(cls, fhir_condition, audit_user_id):
        errors = []
        imis_condition = Diagnosis()
        cls.build_imis_identifier(imis_condition, fhir_condition, errors)
        cls.build_imis_validity_from(imis_condition, fhir_condition, errors)
        cls.build_imis_icd_code(imis_condition, fhir_condition, errors)
        cls.build_imis_icd_name(imis_condition, fhir_condition, errors)
        cls.check_errors(errors)
        return imis_condition

    #  TODO: replace code with uuid when it's implemented into database
    @classmethod
    def get_reference_obj_id(cls, imis_condition):
        return imis_condition.code

    @classmethod
    def get_fhir_resource_type(cls):
        return FHIRCondition

    @classmethod
    def get_imis_obj_by_fhir_reference(cls, reference, errors=None):
        imis_condition_code = cls.get_resource_id_from_reference(reference)
        return DbManagerUtils.get_object_or_none(Diagnosis, code=imis_condition_code)

    @classmethod
    def build_fhir_identifiers(cls, fhir_condition, imis_condition):
        identifiers = []
        icd_id = cls.build_fhir_identifier(str(imis_condition.id),    # because of db as string, has to be changed to uuid
                                             R4IdentifierConfig.get_fhir_identifier_type_system(),
                                             R4IdentifierConfig.get_fhir_acsn_type_code())
        identifiers.append(icd_id)
        icd_code = cls.build_fhir_identifier(imis_condition.code,
                                             R4IdentifierConfig.get_fhir_identifier_type_system(),
                                             R4IdentifierConfig.get_fhir_diagnosis_code_type())
        identifiers.append(icd_code)
        fhir_condition.identifier = identifiers

    @classmethod
    def build_imis_identifier(cls, imis_condition, fhir_condition, errors):
        value = cls.get_fhir_identifier_by_code(fhir_condition.identifier, R4IdentifierConfig.get_fhir_claim_code_type())
        if value:
            imis_condition.code = value
        cls.valid_condition(imis_condition.code is None, gettext('Missing the ICD code'), errors)

    @classmethod
    def build_fhir_recorded_date(cls, fhir_condition, imis_condition):
        fhir_condition.recordedDate = imis_condition.validity_from.isoformat()

    @classmethod
    def build_imis_validity_from(cls, imis_condition, fhir_condition, errors):
        validity_from = fhir_condition.recordedDate
        if not cls.valid_condition(validity_from is None,
                                   gettext('Missing condition `recorded_date` attribute'), errors):
            imis_condition.validity_from = TimeUtils.str_to_date(validity_from)

    @classmethod
    def build_fhir_codes(cls, fhir_condition, imis_condition):
        fhir_condition.code = cls.build_codeable_concept(imis_condition.code, text=imis_condition.name)

    @classmethod
    def build_imis_icd_code(cls, imis_condition, fhir_condition, errors):
        icd_code = fhir_condition.code.coding
        if not cls.valid_condition(icd_code is None,
                                   gettext('Missing condition `icd_code` attribute'), errors):
            imis_condition.code = icd_code

    @classmethod
    def build_imis_icd_name(cls, imis_condition, fhir_condition, errors):
        icd_name = fhir_condition.code.text
        if not cls.valid_condition(icd_name is None,
                                   gettext('Missing condition `icd_name` attribute'), errors):
            imis_condition.name = icd_name

    @classmethod
    def build_fhir_subject(cls, fhir_condition):
        reference = Reference()
        reference.type = "Patient"
        fhir_condition.subject = reference

