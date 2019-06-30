from claim import ClaimSubmitService, ClaimSubmit, ClaimItemSubmit, ClaimServiceSubmit
from claim.models import ClaimDiagnosisCode, ClaimAdmin
from django.http import HttpResponse
from django.utils.translation import gettext
from insuree.models import Insuree
from location.models import HealthFacility

from api_fhir.converters.claimConverter import ClaimConverter
from api_fhir.serializers import BaseFHIRSerializer


class ClaimSerializer(BaseFHIRSerializer):

    fhirConverter = ClaimConverter()

    def create(self, validated_data):
        icd_code = ClaimDiagnosisCode.objects.get(pk=validated_data.get('icd_id')).code
        icd1_code = None
        if validated_data.get('icd_1'):
            icd1_code = ClaimDiagnosisCode.objects.get(pk=validated_data.get('icd_1')).code
        icd2_code = None
        if validated_data.get('icd_2'):
            icd2_code = ClaimDiagnosisCode.objects.get(pk=validated_data.get('icd_2')).code
        icd3_code = None
        if validated_data.get('icd_3'):
            icd3_code = ClaimDiagnosisCode.objects.get(pk=validated_data.get('icd_3')).code
        icd4_code = None
        if validated_data.get('icd_4'):
            icd4_code = ClaimDiagnosisCode.objects.get(pk=validated_data.get('icd_4')).code
        insuree_chf_code = Insuree.objects.get(pk=validated_data.get('insuree_id')).chf_id
        health_facility_code = HealthFacility.objects.get(pk=validated_data.get('health_facility_id')).code
        claim_admin_code = ClaimAdmin.objects.get(pk=validated_data.get('admin_id')).code
        items = ClaimSerializer.build_claim_submit_items(validated_data.get('items'))
        services = ClaimSerializer.build_claim_submit_services(validated_data.get('services'))
        claim_submit = ClaimSubmit(date=validated_data.get('date_claimed'),
                                   code=validated_data.get('code'),
                                   icd_code=icd_code,
                                   icd_code_1=icd1_code,
                                   icd_code_2=icd2_code,
                                   icd_code_3=icd3_code,
                                   icd_code_4=icd4_code,
                                   total=validated_data.get('claimed'),
                                   start_date=validated_data.get('date_from'),
                                   end_date=validated_data.get('date_to'),
                                   insuree_chf_id=insuree_chf_code,
                                   health_facility_code=health_facility_code,
                                   claim_admin_code=claim_admin_code,
                                   visit_type=validated_data.get('visit_type'),
                                   guarantee_no=validated_data.get('guarantee_id'),
                                   item_submits=items,
                                   service_submits=services
                                   )
        request = self.context.get("request")
        ClaimSubmitService(request.user).submit(claim_submit)
        return HttpResponse(gettext('Claim submit created'))

    @classmethod
    def build_claim_submit_items(cls, imis_items):
        items = []
        if imis_items:
            for item in imis_items:
                submit_item = ClaimItemSubmit(item.item.code, item.qty_provided, item.price_asked)
                items.append(submit_item)
        return items

    @classmethod
    def build_claim_submit_services(cls, imis_services):
        services = []
        if imis_services:
            for service in imis_services:
                submit_item = ClaimServiceSubmit(service.service.code, service.qty_provided, service.price_asked)
                services.append(submit_item)
        return services

    class Meta:
        app_label = 'api_fhir'
