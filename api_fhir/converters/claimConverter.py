from claim.models import Claim, ClaimDiagnosisCode
from django.utils.translation import gettext

from api_fhir.configurations import Stu3IdentifierConfig
from api_fhir.converters import BaseFHIRConverter, LocationConverter, PatientConverter, PractitionerConverter
from api_fhir.models import Claim as FHIRClaim, Period, ClaimDiagnosis, Money, ImisClaimIcdTypes
from api_fhir.utils import TimeUtils


class ClaimConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, imis_claim):
        fhir_claim = FHIRClaim()
        fhir_claim.created = imis_claim.date_claimed.isoformat()
        fhir_claim.facility = LocationConverter.build_fhir_resource_reference(imis_claim.health_facility)
        cls.build_fhir_identifiers(fhir_claim, imis_claim)
        fhir_claim.patient = PatientConverter.build_fhir_resource_reference(imis_claim.insuree)
        cls.build_fhir_billable_period(fhir_claim, imis_claim)
        cls.build_fhir_diagnoses(fhir_claim, imis_claim)
        cls.build_fhir_total(fhir_claim, imis_claim)
        fhir_claim.enterer = PractitionerConverter.build_fhir_resource_reference(imis_claim.admin)
        return fhir_claim

    @classmethod
    def to_imis_obj(cls, fhir_claim, audit_user_id):
        errors = []
        imis_claim = Claim()
        cls.build_imis_date_claimed(imis_claim, fhir_claim, errors)
        cls.build_imis_health_facility(errors, fhir_claim, imis_claim)
        cls.build_imis_identifier(imis_claim, fhir_claim, errors)
        cls.build_imis_patient(imis_claim, fhir_claim, errors)
        cls.build_imis_date_range(imis_claim, fhir_claim, errors)
        cls.build_imis_diagnoses(imis_claim, fhir_claim, errors)
        cls.build_imis_total_claimed(imis_claim, fhir_claim, errors)
        cls.build_imis_claim_admin(imis_claim, fhir_claim, errors)
        cls.check_errors(errors)
        return imis_claim

    @classmethod
    def build_imis_date_claimed(cls, imis_claim, fhir_claim, errors):
        if fhir_claim.created:
            imis_claim.date_claimed = TimeUtils.str_to_date(fhir_claim.created)
        cls.valid_condition(imis_claim.date_claimed is None, gettext('Missing the date of creation'), errors)

    @classmethod
    def build_fhir_identifiers(cls, fhir_claim, imis_claim):
        identifiers = []
        cls.build_fhir_id_identifier(identifiers, imis_claim)
        claim_code = cls.build_fhir_identifier(imis_claim.code,
                                               Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                               Stu3IdentifierConfig.get_fhir_claim_code_type())
        identifiers.append(claim_code)
        fhir_claim.identifier = identifiers

    @classmethod
    def build_imis_identifier(cls, imis_claim, fhir_claim, errors):
        identifiers = fhir_claim.identifier
        if identifiers:
            for identifier in identifiers:
                identifier_type = identifier.type
                if identifier_type:
                    coding_list = identifier_type.coding
                    if coding_list:
                        first_coding = cls.get_first_coding_from_codeable_concept(identifier_type)
                        if first_coding.system == Stu3IdentifierConfig.get_fhir_identifier_type_system():
                            code = first_coding.code
                            value = identifier.value
                            if value and code == Stu3IdentifierConfig.get_fhir_claim_code_type():
                                imis_claim.code = value
        cls.valid_condition(imis_claim.code is None, gettext('Missing the claim code'), errors)

    @classmethod
    def build_imis_patient(cls, imis_claim, fhir_claim, errors):
        if fhir_claim.patient:
            imis_claim.insuree = PatientConverter.get_imis_obj_by_fhir_reference(fhir_claim.patient)
        cls.valid_condition(imis_claim.insuree is None, gettext('Missing the patient reference'), errors)

    @classmethod
    def build_imis_health_facility(cls, errors, fhir_claim, imis_claim):
        if fhir_claim.facility:
            imis_claim.health_facility = LocationConverter.get_imis_obj_by_fhir_reference(fhir_claim.facility)
        cls.valid_condition(imis_claim.health_facility is None, gettext('Missing the facility reference'), errors)

    @classmethod
    def build_fhir_billable_period(cls, fhir_claim, imis_claim):
        billable_period = Period()
        if imis_claim.date_from:
            billable_period.start = imis_claim.date_from.isoformat()
        if imis_claim.date_to:
            billable_period.end = imis_claim.date_to.isoformat()
        fhir_claim.billablePeriod = billable_period

    @classmethod
    def build_imis_date_range(cls, imis_claim, fhir_claim, errors):
        billable_period = fhir_claim.billablePeriod
        if billable_period:
            if billable_period.start:
                imis_claim.date_from = TimeUtils.str_to_date(billable_period.start)
            if billable_period.end:
                imis_claim.date_to = TimeUtils.str_to_date(billable_period.end)
        cls.valid_condition(imis_claim.date_from is None, gettext('Missing the billable start date'), errors)

    @classmethod
    def build_fhir_diagnoses(cls, fhir_claim, imis_claim):
        diagnoses = []
        cls.build_fhir_diagnosis(diagnoses, imis_claim.icd.code, ImisClaimIcdTypes.ICD_0.value)
        if imis_claim.icd_1:
            cls.build_fhir_diagnosis(diagnoses, imis_claim.icd_1, ImisClaimIcdTypes.ICD_1.value)
        if imis_claim.icd_2:
            cls.build_fhir_diagnosis(diagnoses, imis_claim.icd_2, ImisClaimIcdTypes.ICD_2.value)
        if imis_claim.icd_3:
            cls.build_fhir_diagnosis(diagnoses, imis_claim.icd_3, ImisClaimIcdTypes.ICD_3.value)
        if imis_claim.icd_4:
            cls.build_fhir_diagnosis(diagnoses, imis_claim.icd_4, ImisClaimIcdTypes.ICD_4.value)
        fhir_claim.diagnosis = diagnoses

    @classmethod
    def build_fhir_diagnosis(cls, diagnoses, icd_code, icd_type):
        claim_diagnosis = ClaimDiagnosis()
        claim_diagnosis.sequence = len(diagnoses) + 1
        claim_diagnosis.diagnosisCodeableConcept = cls.build_codeable_concept(icd_code, None)
        claim_diagnosis.type = [cls.build_simple_codeable_concept(icd_type)]
        diagnoses.append(claim_diagnosis)

    @classmethod
    def build_imis_diagnoses(cls, imis_claim, fhir_claim, errors):
        diagnoses = fhir_claim.diagnosis
        if diagnoses:
            for diagnosis in diagnoses:
                diagnosis_type = cls.get_diagnosis_type(diagnosis)
                diagnosis_code = cls.get_diagnosis_code(diagnosis)
                if diagnosis_type == ImisClaimIcdTypes.ICD_0.value:
                    imis_claim.icd = diagnosis_code
                elif diagnosis_type == ImisClaimIcdTypes.ICD_1.value:
                    imis_claim.icd_1 = diagnosis_code
                elif diagnosis_type == ImisClaimIcdTypes.ICD_2.value:
                    imis_claim.icd_2 = diagnosis_code
                elif diagnosis_type == ImisClaimIcdTypes.ICD_3.value:
                    imis_claim.icd_3 = diagnosis_code
                elif diagnosis_type == ImisClaimIcdTypes.ICD_4.value:
                    imis_claim.icd_4 = diagnosis_code
        cls.valid_condition(imis_claim.icd is None, gettext('Missing the main diagnosis for claim'), errors)

    @classmethod
    def get_diagnosis_type(cls, diagnosis):
        diagnosis_type = None
        type_concept = diagnosis.type
        if type_concept:
            diagnosis_type = type_concept.text
        return diagnosis_type

    @classmethod
    def find_claim_diagnosis_code(cls, icd_code):
        return ClaimDiagnosisCode.objects.get(code=icd_code)

    @classmethod
    def get_diagnosis_code(cls, diagnosis):
        code = None
        concept = diagnosis.diagnosisCodeableConcept
        if concept:
            coding = cls.get_first_coding_from_codeable_concept(concept)
            icd_code = coding.code
            if icd_code:
                code = cls.find_claim_diagnosis_code(icd_code)
        return code

    @classmethod
    def build_fhir_total(cls, fhir_claim, imis_claim):
        total_claimed = imis_claim.claimed
        if not total_claimed:
            total_claimed = 0
        fhir_total = Money()
        fhir_total.value = total_claimed
        fhir_claim.total = fhir_total

    @classmethod
    def build_imis_total_claimed(cls, imis_claim, fhir_claim, errors):
        total_money = fhir_claim.total
        if total_money is not None:
            imis_claim.claimed = total_money.value
        cls.valid_condition(imis_claim.claimed is None,
                            gettext('Missing the value for `total` attribute'), errors)

    @classmethod
    def build_imis_claim_admin(cls, imis_claim, fhir_claim, errors):
        if fhir_claim.enterer:
            imis_claim.admin = PractitionerConverter.get_imis_obj_by_fhir_reference(fhir_claim.enterer)
        cls.valid_condition(imis_claim.admin is None, gettext('Missing the enterer reference'), errors)
