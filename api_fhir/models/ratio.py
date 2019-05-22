from api_fhir.models import Element


class Ratio(Element):

    resource_type = "Ratio"

    def __init__(self):
        self.denominator = None  # Type `Quantity` (represented as `dict` in JSON).

        self.numerator = None  # Type `Quantity` (represented as `dict` in JSON).

        super(Ratio, self).__init__()

    class Meta:
        app_label = 'api_fhir'
