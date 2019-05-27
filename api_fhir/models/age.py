from api_fhir.models.quantity import Quantity


class Age(Quantity):

    resource_type = "Age"

    def __init__(self):
        super(Age, self).__init__()

    class Meta:
        app_label = 'api_fhir'
