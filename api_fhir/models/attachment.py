from api_fhir.models.element import Element


class Attachment(Element):

    resource_type = "Attachment"

    def __init__(self):
        self.contentType = None  # Type `str`.

        self.creation = None  # Type `FHIRDate` (represented as `str` in JSON).

        self.data = None  # Type `str` (Data inline, base64ed)

        self.hash = None  # Type `str` (Hash of the data (sha-1, base64ed)

        self.language = None  # Type `str`.

        self.size = None  # Type `int`.

        self.title = None  # Type `str`.

        self.url = None  # Type `str`.

        super(Attachment, self).__init__()

    class Meta:
        app_label = 'api_fhir'
