from api_fhir.models.element import Element


class Reference(Element):

    resource_type = "Reference"

    def __init__(self):
        self.display = None  # Type `str`.

        self.identifier = None  # Type `Identifier` (represented as `dict` in JSON).

        self.reference = None  # Type `str`.

        self.type = None  # Type `str` (e.g. "Patient").

        super(Reference, self).__init__()

    class Meta:
        app_label = 'api_fhir'
