from api_fhir.models import Quantity


class Distance(Quantity):

    class Meta:
        app_label = 'api_fhir'
