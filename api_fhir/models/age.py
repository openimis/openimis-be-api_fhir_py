from api_fhir.models import Quantity


class Age(Quantity):

    class Meta:
        app_label = 'api_fhir'
