from api_fhir.models import Quantity


class Duration(Quantity):

    class Meta:
        app_label = 'api_fhir'

