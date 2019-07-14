from rest_framework import status
from rest_framework.test import APITestCase

from api_fhir.converters import PractitionerConverter
from api_fhir.models import PractitionerRole
from api_fhir.tests import GenericFhirAPITestMixin, FhirApiReadTestMixin, FhirApiUpdateTestMixin, \
    FhirApiCreateTestMixin, LocationTestMixin, PractitionerTestMixin, FhirApiDeleteTestMixin
from api_fhir.utils import TimeUtils


class PractitionerRoleAPITests(GenericFhirAPITestMixin, FhirApiReadTestMixin, FhirApiCreateTestMixin,
                               FhirApiUpdateTestMixin, FhirApiDeleteTestMixin, APITestCase):

    base_url = '/api_fhir/PractitionerRole/'
    _test_json_path = "/test/test_practitionerRole.json"
    _TEST_LOCATION_CODE = "12345678"
    _TEST_CLAIM_ADMIN_CODE = "1234abcd"
    _TEST_UPDATED_CLAIM_ADMIN_CODE = "newCode"
    _TEST_ADMIN_USER_ID = 1

    def setUp(self):
        super(PractitionerRoleAPITests, self).setUp()

    def verify_updated_obj(self, updated_obj):
        self.assertTrue(isinstance(updated_obj, PractitionerRole))
        self.assertEqual(self._TEST_UPDATED_CLAIM_ADMIN_CODE,
                         PractitionerConverter.get_resource_id_from_reference(updated_obj.practitioner))

    def update_resource(self, data):
        new_practitioner = self._create_and_save_claim_admin(self._TEST_UPDATED_CLAIM_ADMIN_CODE)
        data['practitioner'] = PractitionerConverter.build_fhir_resource_reference(new_practitioner).toDict()

    def create_dependencies(self):
        self._create_and_save_hf()
        self._create_and_save_claim_admin(self._TEST_CLAIM_ADMIN_CODE)

    def _create_and_save_hf(self):
        imis_hf = LocationTestMixin().create_test_imis_instance()
        imis_hf.validity_from = TimeUtils.now()
        imis_hf.offline = False
        imis_hf.audit_user_id = self._TEST_ADMIN_USER_ID
        imis_hf.code = self._TEST_LOCATION_CODE
        imis_hf.save()
        return imis_hf

    def _create_and_save_claim_admin(self, claim_admin_code):
        claim_admin = PractitionerTestMixin().create_test_imis_instance()
        claim_admin.audit_user_id = self._TEST_ADMIN_USER_ID
        claim_admin.code = claim_admin_code
        claim_admin.save()
        return claim_admin

    def verify_deleted_response(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        practitioner_role = self.get_fhir_obj_from_json_response(response)
        self.assertTrue(isinstance(practitioner_role, PractitionerRole))
        self.assertEqual(0, len(practitioner_role.location))

