from claim.models import ClaimAdmin
from django.utils.translation import gettext

from api_fhir.converters import PractitionerRoleConverter
from api_fhir.exceptions import FHIRRequestProcessException
from api_fhir.serializers import BaseFHIRSerializer


class PractitionerRoleSerializer(BaseFHIRSerializer):

    fhirConverter = PractitionerRoleConverter()

    def create(self, validated_data):
        claim_admin_id = validated_data.get('id')
        claim_admin = None
        if claim_admin_id:
            claim_admin = ClaimAdmin.objects.get(pk=claim_admin_id)
        if not claim_admin:
            raise FHIRRequestProcessException([gettext('Missing Practitioner for id {}').format(claim_admin_id)])
        claim_admin.health_facility_id = validated_data.get('health_facility_id', claim_admin.health_facility_id)
        claim_admin.save()
        return claim_admin

    def update(self, instance, validated_data):
        instance.health_facility_id = validated_data.get('health_facility_id', instance.health_facility_id)
        instance.audit_user_id = self.get_audit_user_id()
        instance.save()
        return instance
