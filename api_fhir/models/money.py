from api_fhir.models.quantity import Quantity


class Money(Quantity):

    resource_type = "Money"

    def __init__(self):
        super(Money, self).__init__()

    class Meta:
        app_label = 'api_fhir'
