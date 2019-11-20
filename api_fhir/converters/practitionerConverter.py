from claim.models import ClaimAdmin
from django.utils.translation import gettext

from api_fhir.configurations import Stu3IdentifierConfig
from api_fhir.converters import BaseFHIRConverter, PersonConverterMixin, ReferenceConverterMixin
from api_fhir.models import Practitioner
from api_fhir.utils import TimeUtils, DbManagerUtils


class PractitionerConverter(BaseFHIRConverter, PersonConverterMixin, ReferenceConverterMixin):

    @classmethod
    def to_fhir_obj(cls, imis_claim_admin):
        fhir_practitioner = Practitioner()
        cls.build_fhir_pk(fhir_practitioner, imis_claim_admin.uuid)
        cls.build_fhir_identifiers(fhir_practitioner, imis_claim_admin)
        cls.build_human_names(fhir_practitioner, imis_claim_admin)
        cls.build_fhir_birth_date(fhir_practitioner, imis_claim_admin)
        cls.build_fhir_telecom(fhir_practitioner, imis_claim_admin)
        return fhir_practitioner

    @classmethod
    def to_imis_obj(cls, fhir_practitioner, audit_user_id):
        errors = []
        imis_claim_admin = PractitionerConverter.create_default_claim_admin(audit_user_id)
        cls.build_imis_identifiers(imis_claim_admin, fhir_practitioner, errors)
        cls.build_imis_names(imis_claim_admin, fhir_practitioner)
        cls.build_imis_birth_date(imis_claim_admin, fhir_practitioner)
        cls.build_imis_contacts(imis_claim_admin, fhir_practitioner)
        cls.check_errors(errors)
        return imis_claim_admin

    @classmethod
    def get_reference_obj_id(cls, imis_claim_admin):
        return imis_claim_admin.uuid

    @classmethod
    def get_fhir_resource_type(cls):
        return Practitioner

    @classmethod
    def get_imis_obj_by_fhir_reference(cls, reference, errors=None):
        imis_claim_admin_uuid = cls.get_resource_id_from_reference(reference)
        return DbManagerUtils.get_object_or_none(ClaimAdmin, uuid=imis_claim_admin_uuid)

    @classmethod
    def create_default_claim_admin(cls, audit_user_id):
        imis_claim_admin = ClaimAdmin()
        imis_claim_admin.validity_from = TimeUtils.now()
        imis_claim_admin.audit_user_id = audit_user_id
        return imis_claim_admin

    @classmethod
    def build_fhir_identifiers(cls, fhir_practitioner, imis_claim_admin):
        identifiers = []
        cls.build_fhir_uuid_identifier(identifiers, imis_claim_admin)
        cls.build_fhir_code_identifier(identifiers, imis_claim_admin)
        fhir_practitioner.identifier = identifiers

    @classmethod
    def build_fhir_code_identifier(cls, identifiers, imis_claim_admin):
        if imis_claim_admin.code:
            identifier = cls.build_fhir_identifier(imis_claim_admin.code,
                                                   Stu3IdentifierConfig.get_fhir_identifier_type_system(),
                                                   Stu3IdentifierConfig.get_fhir_claim_admin_code_type())
            identifiers.append(identifier)

    @classmethod
    def build_imis_identifiers(cls, imis_claim_admin, fhir_practitioner, errors):
        value = cls.get_fhir_identifier_by_code(fhir_practitioner.identifier,
                                                Stu3IdentifierConfig.get_fhir_claim_admin_code_type())
        if value:
            imis_claim_admin.code = value
        cls.valid_condition(imis_claim_admin.code is None, gettext('Missing the claim admin code'), errors)

    @classmethod
    def build_human_names(cls, fhir_practitioner, imis_claim_admin):
        name = cls.build_fhir_names_for_person(imis_claim_admin)
        fhir_practitioner.name = [name]

    @classmethod
    def build_imis_names(cls, imis_claim_admin, fhir_practitioner):
        names = fhir_practitioner.name
        imis_claim_admin.last_name, imis_claim_admin.other_names = cls.build_imis_last_and_other_name(names)

    @classmethod
    def build_fhir_birth_date(cls, fhir_practitioner, imis_claim_admin):
        fhir_practitioner.birthDate = imis_claim_admin.dob.isoformat()

    @classmethod
    def build_imis_birth_date(cls, imis_claim_admin, fhir_practitioner):
        birth_date = fhir_practitioner.birthDate
        if birth_date:
            imis_claim_admin.dob = TimeUtils.str_to_date(birth_date)

    @classmethod
    def build_fhir_telecom(cls, fhir_practitioner, imis_claim_admin):
        fhir_practitioner.telecom = cls.build_fhir_telecom_for_person(phone=imis_claim_admin.phone,
                                                                      email=imis_claim_admin.email_id)

    @classmethod
    def build_imis_contacts(cls, imis_claim_admin, fhir_practitioner):
        imis_claim_admin.phone, imis_claim_admin.email_id = cls.build_imis_phone_num_and_email(fhir_practitioner.telecom)
