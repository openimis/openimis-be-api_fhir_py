import os
from unittest import mock

from api_fhir.converters import PractitionerRoleConverter
from api_fhir.models import FHIRBaseObject
from api_fhir.tests import PractitionerRoleTestMixin


class PractitionerRoleConverterTestCase(PractitionerRoleTestMixin):

    __TEST_PRACTITIONER_ROLE_JSON_PATH = "/test/test_practitionerRole.json"

    def set_up(self):
        super(PractitionerRoleConverterTestCase, self).set_up()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self._test_practitioner_role_json_representation = open(dir_path + self.__TEST_PRACTITIONER_ROLE_JSON_PATH).read()

    def test_to_fhir_obj(self):
        self.set_up()
        imis_claim_admin = self.create_test_imis_instance()
        fhir_practitioner_role = PractitionerRoleConverter.to_fhir_obj(imis_claim_admin)
        self.verify_fhir_instance(fhir_practitioner_role)

    @mock.patch('location.models.HealthFacility.objects')
    @mock.patch('claim.models.ClaimAdmin.objects')
    def test_to_imis_obj(self, mock_claim_admin, mock_hf):
        self.set_up()
        mock_hf.filter().first.return_value = self._TEST_HF
        mock_claim_admin.filter().first.return_value = self._TEST_CLAIM_ADMIN

        fhir_practitioner_role = self.create_test_fhir_instance()
        imis_claim_admin = PractitionerRoleConverter.to_imis_obj(fhir_practitioner_role, None)
        self.verify_imis_instance(imis_claim_admin)

    def test_create_object_from_json(self):
        self.set_up()
        fhir_practitioner_role = FHIRBaseObject.loads(self._test_practitioner_role_json_representation, 'json')
        self.verify_fhir_instance(fhir_practitioner_role)

    def test_fhir_object_to_json(self):
        self.set_up()
        fhir_practitioner_role = self.create_test_fhir_instance()
        actual_representation = fhir_practitioner_role.dumps(format_='json')
        self.assertEqual(self._test_practitioner_role_json_representation, actual_representation)
