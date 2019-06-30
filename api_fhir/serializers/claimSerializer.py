from claim import ClaimSubmitService, ClaimSubmit
from django.http import HttpResponse
from django.utils.translation import gettext

from api_fhir.converters.claimConverter import ClaimConverter
from api_fhir.serializers import BaseFHIRSerializer


class ClaimSerializer(BaseFHIRSerializer):

    fhirConverter = ClaimConverter()

    def create(self, validated_data):
        claim_submit = ClaimSubmit(date=validated_data.get('date_claimed'),
                                   code=validated_data.get('code'),
                                   icd_code=validated_data.get('icd_code'),
                                   icd_code_1=validated_data.get('icd1_code'),
                                   icd_code_2=validated_data.get('icd2_code'),
                                   icd_code_3=validated_data.get('icd3_code'),
                                   icd_code_4=validated_data.get('icd4_code'),
                                   total=validated_data.get('claimed'),
                                   start_date=validated_data.get('date_from'),
                                   end_date=validated_data.get('date_to'),
                                   insuree_chf_id=validated_data.get('insuree_chf_code'),
                                   health_facility_code=validated_data.get('health_facility_code'),
                                   claim_admin_code=validated_data.get('claim_admin_code'),
                                   visit_type=validated_data.get('visit_type'),
                                   guarantee_no=validated_data.get('guarantee_id'),
                                   item_submits=validated_data.get('submit_items'),
                                   service_submits=validated_data.get('submit_services')
                                   )
        request = self.context.get("request")
        ClaimSubmitService(request.user).submit(claim_submit)
        return HttpResponse(gettext('Claim submit created'))

    class Meta:
        app_label = 'api_fhir'
