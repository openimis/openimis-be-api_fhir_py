from insuree.models import Gender
from rest_framework.test import APITestCase

from api_fhir.models import Patient
from api_fhir.tests import GenericFhirAPITestMixin, FhirApiReadTestMixin, FhirApiCreateTestMixin, \
    FhirApiUpdateTestMixin, FhirApiDeleteTestMixin


class PatientAPITests(GenericFhirAPITestMixin, FhirApiReadTestMixin, FhirApiCreateTestMixin, FhirApiUpdateTestMixin,
                      FhirApiDeleteTestMixin, APITestCase):

    base_url = '/api_fhir/Patient/'
    _test_json_path = "/test/test_patient.json"
    _TEST_GENDER_CODE = 'M'
    _TEST_EXPECTED_NAME = "UPDATED_NAME"

    def setUp(self):
        super(PatientAPITests, self).setUp()

    def verify_updated_obj(self, updated_obj):
        self.assertTrue(isinstance(updated_obj, Patient))
        self.assertEqual(self._TEST_EXPECTED_NAME, updated_obj.name[0].family)

    def update_resource(self, data):
        data['name'][0]['family'] = self._TEST_EXPECTED_NAME

    def create_dependencies(self):
        gender = Gender()
        gender.code = self._TEST_GENDER_CODE
        gender.save()
