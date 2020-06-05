from api_fhir.models import FHIRBaseObject
from claim import ClaimSubmitService, ClaimSubmit, ClaimSubmitError
from claim.apps import ClaimConfig
from claim.models import Claim
from claim.services import submit_claim
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from api_fhir.configurations import GeneralConfiguration
from api_fhir.converters import ClaimResponseConverter
from api_fhir.converters.claimConverter import ClaimConverter
from api_fhir.serializers import BaseFHIRSerializer


class ClaimSerializer(BaseFHIRSerializer):

    fhirConverter = ClaimConverter()

    def create(self, validated_data):
        request = self.context.get("request")
        if not request.user or not request.user.has_perms(ClaimConfig.gql_mutation_create_claims_perms):
            return HttpResponseForbidden()

        if GeneralConfiguration.get_claim_submit_legacy():
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
                                       item_submits=validated_data.get('items'),
                                       service_submits=validated_data.get('services'),
                                       comment=validated_data.get('explanation')
                                       )
            ClaimSubmitService(request.user).submit(claim_submit)
            return self.create_claim_response(validated_data.get('code'))
        else:
            audit_user_id = self.get_audit_user_id()
            data = self.initial_data
            data["resourceType"] = "Claim"
            if isinstance(data, dict):
                data = FHIRBaseObject.fromDict(data)
            claim = self.fhirConverter.to_imis_obj(data, audit_user_id, submit_itemsvc=False)
            # the items and services are in submit_items and submit_services as they are not created in DB. Let's do it.
            if claim.submit_items:
                items = claim.submit_items
                del claim.submit_items
            else:
                items = None
            if claim.submit_services:
                services = claim.submit_services
                del claim.submit_services
            else:
                services = None
            claim.status = Claim.STATUS_ENTERED
            claim.audit_user_id = audit_user_id
            claim.save()
            for item in items:
                # TODO: identify the item.item corresponding to the Product in the correct location
                claim.items.add(item, bulk=False)
            for service in services:
                # TODO: identify the service.service corresponding to the Product in the correct location
                claim.services.add(service, bulk=False)

            errors = submit_claim(claim, self.get_audit_user_id())
            if len(errors) > 0:
                raise ClaimSubmitError(claim.rejection_reason)
            else:
                return self.create_claim_response(validated_data.get('code'))

    def create_claim_response(self, claim_code):
        claim = get_object_or_404(Claim, code=claim_code)
        return ClaimResponseConverter.to_fhir_obj(claim)
