from rest_framework import status
from rest_framework.test import APITestCase

from api_fhir.converters import LocationConverter
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
    _TEST_UPDATED_LOCATION_CODE = "newCode"
    _TEST_UPDATED_LOCATION_NAME = "newLocation"
    _TEST_LEGAL_FORM = "G"
    _TEST_ADMIN_USER_ID = 1

    def setUp(self):
        super(PractitionerRoleAPITests, self).setUp()

    def verify_updated_obj(self, updated_obj):
        self.assertTrue(isinstance(updated_obj, PractitionerRole))
        self.assertEqual(self._TEST_UPDATED_LOCATION_CODE,
                         LocationConverter.get_resource_id_from_reference(updated_obj.location[0]))
        self.assertEqual(self._TEST_UPDATED_LOCATION_NAME,
                         LocationConverter.get_imis_obj_by_fhir_reference(updated_obj.location[0]).name)

    def update_resource(self, data):
        new_location = self._create_and_save_hf()
        new_location.name = self._TEST_UPDATED_LOCATION_NAME
        new_location.code = self._TEST_UPDATED_LOCATION_CODE
        new_location.save()
        data['location'][0] = LocationConverter.build_fhir_resource_reference(new_location).toDict()

    def create_dependencies(self):
        self._create_and_save_hf()
        self._create_and_save_claim_admin()

    def _create_and_save_hf(self):
        imis_hf = LocationTestMixin().create_test_imis_instance()
        imis_hf.id = None
        imis_hf.validity_from = TimeUtils.now()
        imis_hf.offline = False
        imis_hf.audit_user_id = self._TEST_ADMIN_USER_ID
        imis_hf.code = self._TEST_LOCATION_CODE
        imis_hf.save()
        return imis_hf

    def _create_and_save_claim_admin(self):
        claim_admin = PractitionerTestMixin().create_test_imis_instance()
        claim_admin.id = None
        claim_admin.audit_user_id = self._TEST_ADMIN_USER_ID
        claim_admin.code = self._TEST_CLAIM_ADMIN_CODE
        claim_admin.save()
        return claim_admin

    def verify_deleted_response(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        practitioner_role = self.get_fhir_obj_from_json_response(response)
        self.assertTrue(isinstance(practitioner_role, PractitionerRole))
        self.assertEqual(0, len(practitioner_role.location))

