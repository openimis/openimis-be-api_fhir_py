from api_fhir.models import Quantity


class Count(Quantity):

    class Meta:
        app_label = 'api_fhir'
