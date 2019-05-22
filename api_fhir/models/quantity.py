from api_fhir.models.element import Element


class Quantity(Element):

    resource_type = "Quantity"

    def __init__(self):
        self.code = None  # Type `str`.

        self.comparator = None  # Type `str` (< | <= | >= | >).

        self.system = None  # Type `str`.

        self.unit = None  # Type `str`.

        self.value = None  # Type `float`.

        super(Quantity, self).__init__()

    class Meta:
        app_label = 'api_fhir'
