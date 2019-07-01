from api_fhir.converters import PractitionerRoleConverter
from mixin.practitionerRoleTestMixin import PractitionerRoleTestMixin


class PractitionerRoleConverterTestCase(PractitionerRoleTestMixin):

    def test_to_fhir_obj(self):
        imis_claim_admin = self.create_test_imis_instance()
        fhir_practitioner_role = PractitionerRoleConverter.to_fhir_obj(imis_claim_admin)
        self.verify_fhir_instance(fhir_practitioner_role)

    def test_to_imis_obj(self):
        fhir_practitioner_role = self.create_test_fhir_instance()
        imis_claim_admin = PractitionerRoleConverter.to_imis_obj(fhir_practitioner_role, None)
        self.verify_imis_instance(imis_claim_admin)
