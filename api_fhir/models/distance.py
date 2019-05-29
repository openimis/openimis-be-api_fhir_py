from api_fhir.models.quantity import Quantity


class Distance(Quantity):

    resource_type = "Distance"

    def __init__(self):
        super(Distance, self).__init__()

    class Meta:
        app_label = 'api_fhir'
