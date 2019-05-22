from api_fhir.models.element import Element


class Annotation(Element):

    resource_type = "Annotation"

    def __init__(self):
        self.authorReference = None  # Type `Reference` (represented as `dict` in JSON).

        self.authorString = None  # Type `str`.

        self.text = None  # Type `str`.

        self.time = None  # Type `FHIRDate` (represented as `str` in JSON).

        super(Annotation, self).__init__()

    class Meta:
        app_label = 'api_fhir'
