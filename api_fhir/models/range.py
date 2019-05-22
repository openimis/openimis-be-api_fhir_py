from api_fhir.models import Element


class Range(Element):

    resource_type = "Range"

    def __init__(self):
        self.high = None  # Type `Quantity` (represented as `dict` in JSON).

        self.low = None  # Type `Quantity` (represented as `dict` in JSON).

        super(Range, self).__init__()

    class Meta:
        app_label = 'api_fhir'
