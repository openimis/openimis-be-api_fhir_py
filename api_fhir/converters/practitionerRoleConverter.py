from claim.models import ClaimAdmin
from location.models import HealthFacility

from api_fhir.converters import BaseFHIRConverter, PractitionerConverter, LocationConverter
from api_fhir.models import PractitionerRole


class PractitionerRoleConverter(BaseFHIRConverter):

    @classmethod
    def to_fhir_obj(cls, imis_claim_admin):
        fhir_practitioner_role = PractitionerRole()
        cls.build_fhir_identifiers(fhir_practitioner_role, imis_claim_admin)
        cls.build_fhir_practitioner_reference(fhir_practitioner_role, imis_claim_admin)
        cls.build_fhir_location_references(fhir_practitioner_role, imis_claim_admin)
        return fhir_practitioner_role

    @classmethod
    def to_imis_obj(cls, fhir_practitioner_role, audit_user_id):
        errors = []
        practitioner = fhir_practitioner_role.practitioner
        claim_admin = cls.get_practitioner_by_reference(practitioner, errors)
        location_references = fhir_practitioner_role.location
        health_facility = cls.get_location_by_reference(location_references, errors)

        if claim_admin:
            claim_admin.health_facility = health_facility
        cls.check_errors(errors)
        return claim_admin

    @classmethod
    def build_fhir_identifiers(cls, fhir_practitioner_role, imis_claim_admin):
        identifiers = []
        cls.build_fhir_id_identifier(identifiers, imis_claim_admin)
        fhir_practitioner_role.identifier = identifiers

    @classmethod
    def build_fhir_practitioner_reference(cls, fhir_practitioner_role, imis_claim_admin):
        fhir_practitioner_role.practitioner = PractitionerConverter.build_fhir_resource_reference(imis_claim_admin)

    @classmethod
    def get_practitioner_by_reference(cls, practitioner, errors):
        claim_admin = None
        imis_claim_admin_id = PractitionerConverter.get_resource_id_from_reference(practitioner)
        if not cls.valid_condition(imis_claim_admin_id is None,
                                   'Could not fetch Practitioner id from reference'.format(practitioner), errors):
            claim_admin = ClaimAdmin.objects.get(pk=imis_claim_admin_id)
        return claim_admin

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
            location_id = LocationConverter.get_resource_id_from_reference(location)
            if not cls.valid_condition(location_id is None,
                                       'Could not fetch Location id from reference'.format(location), errors):
                health_facility = HealthFacility.objects.get(pk=location_id)
        return health_facility

    @classmethod
    def get_first_location(cls, location_references):
        return location_references[0]

    class Meta:
        app_label = 'api_fhir'
