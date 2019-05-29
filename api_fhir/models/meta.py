from api_fhir.models.element import Element


class Meta(Element):

    resource_type = "Meta"

    def __init__(self):
        self.lastUpdated = None  # Type `FHIRDate` (represented as `str` in JSON)

        self.profile = None  # List of `str` items.

        self.security = None  # List of `Coding` items (represented as `dict` in JSON).

        self.tag = None  # List of `Coding` items (represented as `dict` in JSON).

        self.versionId = None  # Type `str`.

        super(Meta, self).__init__()

    class Meta:
        app_label = 'api_fhir'
