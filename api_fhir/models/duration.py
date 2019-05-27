from api_fhir.models.quantity import Quantity


class Duration(Quantity):

    resource_type = "Duration"

    def __init__(self):
        super(Duration, self).__init__()

    class Meta:
        app_label = 'api_fhir'

