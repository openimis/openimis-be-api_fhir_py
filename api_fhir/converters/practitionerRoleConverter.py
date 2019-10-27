from api_fhir.converters import BaseFHIRConverter, PractitionerConverter, LocationConverter
from api_fhir.models import PractitionerRole


class PractitionerRoleConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, imis_claim_admin):
        fhir_practitioner_role = PractitionerRole()
        cls.build_fhir_pk(fhir_practitioner_role, imis_claim_admin.uuid)
        cls.build_fhir_identifiers(fhir_practitioner_role, imis_claim_admin)
        cls.build_fhir_practitioner_reference(fhir_practitioner_role, imis_claim_admin)
        cls.build_fhir_location_references(fhir_practitioner_role, imis_claim_admin)
        return fhir_practitioner_role

    @classmethod
    def to_imis_obj(cls, fhir_practitioner_role, audit_user_id):
        errors = []
        practitioner = fhir_practitioner_role.practitioner
        claim_admin = PractitionerConverter.get_imis_obj_by_fhir_reference(practitioner, errors)
        location_references = fhir_practitioner_role.location
        health_facility = cls.get_location_by_reference(location_references, errors)

        if not cls.valid_condition(claim_admin is None, "Practitioner doesn't exists", errors):
            claim_admin.health_facility = health_facility
        cls.check_errors(errors)
        return claim_admin

    @classmethod
    def build_fhir_identifiers(cls, fhir_practitioner_role, imis_claim_admin):
        identifiers = []
        cls.build_fhir_uuid_identifier(identifiers, imis_claim_admin)
        fhir_practitioner_role.identifier = identifiers

    @classmethod
    def build_fhir_practitioner_reference(cls, fhir_practitioner_role, imis_claim_admin):
        fhir_practitioner_role.practitioner = PractitionerConverter.build_fhir_resource_reference(imis_claim_admin)

    @classmethod
    def build_fhir_location_references(cls, fhir_practitioner_role, imis_claim_admin):
        if imis_claim_admin.health_facility:
            reference = LocationConverter.build_fhir_resource_reference(imis_claim_admin.health_facility)
            fhir_practitioner_role.location = [reference]

    @classmethod
    def get_location_by_reference(cls, location_references, errors):
        health_facility = None
        if location_references:
            location = cls.get_first_location(location_references)
            health_facility = LocationConverter.get_imis_obj_by_fhir_reference(location, errors)
        return health_facility

    @classmethod
    def get_first_location(cls, location_references):
        return location_references[0]
