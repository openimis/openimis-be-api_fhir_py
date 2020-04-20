from api_fhir.models import PractitionerRole, Reference
from api_fhir.tests import GenericTestMixin, PractitionerTestMixin, LocationTestMixin


class PractitionerRoleTestMixin(GenericTestMixin):

    _TEST_CLAIM_ADMIN = None
    _TEST_HF = None
    _TEST_LOCATION_REFERENCE = None
    _TEST_PRACTITIONER_REFERENCE = None

    def setUp(self):
        self._TEST_CLAIM_ADMIN = PractitionerTestMixin().create_test_imis_instance()
        self._TEST_PRACTITIONER_REFERENCE = "Practitioner/" + self._TEST_CLAIM_ADMIN.uuid

        self._TEST_HF = LocationTestMixin().create_test_imis_instance()
        self._TEST_LOCATION_REFERENCE = "Location/" + self._TEST_HF.uuid

    def create_test_imis_instance(self):
        self.setUp()
        self._TEST_CLAIM_ADMIN.health_facility = self._TEST_HF
        return self._TEST_CLAIM_ADMIN

    def verify_imis_instance(self, imis_obj):
        self.assertEqual(self._TEST_HF.code, imis_obj.health_facility.code)

    def create_test_fhir_instance(self):
        fhir_practitioner_role = PractitionerRole()
        location_reference = Reference()
        location_reference.reference = self._TEST_LOCATION_REFERENCE
        fhir_practitioner_role.location = [location_reference]
        practitioner_reference = Reference()
        practitioner_reference.reference = self._TEST_PRACTITIONER_REFERENCE
        fhir_practitioner_role.practitioner = practitioner_reference
        return fhir_practitioner_role

    def verify_fhir_instance(self, fhir_obj):
        self.assertEqual(self._TEST_LOCATION_REFERENCE, fhir_obj.location[0].reference)
        self.assertEqual(self._TEST_PRACTITIONER_REFERENCE, fhir_obj.practitioner.reference)
