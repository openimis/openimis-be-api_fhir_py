from rest_framework.test import APITestCase

from api_fhir.models import Location
from api_fhir.tests import GenericFhirAPITestMixin, FhirApiReadTestMixin, FhirApiCreateTestMixin, \
    FhirApiUpdateTestMixin, FhirApiDeleteTestMixin


class LocationAPITests(GenericFhirAPITestMixin, FhirApiReadTestMixin, FhirApiCreateTestMixin, FhirApiUpdateTestMixin,
                       FhirApiDeleteTestMixin, APITestCase):

    base_url = '/api_fhir/Location/'
    _test_json_path = "/test/test_location.json"
    _TEST_EXPECTED_NAME = "UPDATED_NAME"

    def setUp(self):
        super(LocationAPITests, self).setUp()

    def verify_updated_obj(self, updated_obj):
        self.assertTrue(isinstance(updated_obj, Location))
        self.assertEqual(self._TEST_EXPECTED_NAME, updated_obj.name)

    def update_resource(self, data):
        data['name'] = self._TEST_EXPECTED_NAME
