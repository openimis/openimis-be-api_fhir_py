from api_fhir.models.quantity import Quantity

class Count(Quantity):

    resource_type = "Count"

    def __init__(self):
      super(Count, self).__init__()

    class Meta:
        app_label = 'api_fhir'
