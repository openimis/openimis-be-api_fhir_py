from api_fhir.models.element import Element


class SampledData(Element):

    resource_type = "SampledData"

    def __init__(self):
        self.data = None  # Type `str` ("E" | "U" | "L").

        self.dimensions = None  # Type `int`.

        self.factor = None  # Type `float`.

        self.lowerLimit = None  # Type `float`.

        self.origin = None  # Type `Quantity` (represented as `dict` in JSON).

        self.period = None  # Type `float`.

        self.upperLimit = None  # Type `float`.

        super(SampledData, self).__init__()

    class Meta:
        app_label = 'api_fhir'
