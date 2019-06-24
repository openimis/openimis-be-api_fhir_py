from api_fhir.models import Quantity


class Money(Quantity):

    class Meta:
        app_label = 'api_fhir'
