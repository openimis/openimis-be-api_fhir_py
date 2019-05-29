from api_fhir.models.element import Element


class Coding(Element):

    resource_type = "Coding"

    def __init__(self):
        self.code = None  # Type `str`.

        self.display = None  # Type `str`.

        self.system = None  # Type `str`.

        self.userSelected = None  # Type `bool`.

        self.version = None  # Type `str`.

        super(Coding, self).__init__()

    class Meta:
        app_label = 'api_fhir'
