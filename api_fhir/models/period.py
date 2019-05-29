from api_fhir.models.element import Element


class Period(Element):

    resource_type = "Period"

    def __init__(self):
        self.end = None  # Type `FHIRDate` (represented as `str` in JSON).

        self.start = None  # Type `FHIRDate` (represented as `str` in JSON).

        super(Period, self).__init__()

    class Meta:
        app_label = 'api_fhir'
