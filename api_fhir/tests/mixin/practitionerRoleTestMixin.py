from api_fhir.configurations import GeneralConfiguration
from api_fhir.models import PractitionerRole, Reference
from api_fhir.utils import TimeUtils
from mixin.dbIdTestMixin import DbIdTestMixin
from mixin.genericTestMixin import GenericTestMixin
from mixin.locationTestMixin import LocationTestMixin
from mixin.practitionerTestMixin import PractitionerTestMixin


class PractitionerRoleTestMixin(GenericTestMixin, DbIdTestMixin):

    _TEST_CLAIM_ADMIN = None
    _TEST_CLAIM_ADMIN_ID = None
    _TEST_HF = None
    _TEST_HF_ID = None
    _TEST_LOCATION_REFERENCE = None
    _TEST_PRACTITIONER_REFERENCE = None

    def get_test_db_id(self):
        return self.__TEST_CLAIM_ADMIN_ID

    def set_up(self):
        imis_claim_admin = PractitionerTestMixin().create_test_imis_instance()
        imis_claim_admin.validity_from = TimeUtils.now()
        imis_claim_admin.audit_user_id = 1
        imis_claim_admin.save()
        self._TEST_CLAIM_ADMIN = imis_claim_admin
        self._TEST_CLAIM_ADMIN_ID = imis_claim_admin.id
        self._TEST_PRACTITIONER_REFERENCE = "Practitioner/" + str(self._TEST_CLAIM_ADMIN_ID)

        imis_hf = LocationTestMixin().create_test_imis_instance()
        imis_hf.offline = GeneralConfiguration.get_default_value_of_location_offline_attribute()
        imis_hf.care_type = GeneralConfiguration.get_default_value_of_location_care_type()
        imis_hf.validity_from = TimeUtils.now()
        imis_hf.audit_user_id = 1
        imis_hf.save()
        self._TEST_HF = imis_hf
        self._TEST_HF_ID = imis_hf.id
        self._TEST_LOCATION_REFERENCE = "Location/" + str(self._TEST_HF_ID)

    def create_test_imis_instance(self):
        self.set_up()
        self._TEST_CLAIM_ADMIN.health_facility = self._TEST_HF
        return self._TEST_CLAIM_ADMIN

    def verify_imis_instance(self, imis_obj):
        self.assertEqual(self._TEST_HF_ID, imis_obj.health_facility.id)

    def create_test_fhir_instance(self):
        self.set_up()
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
