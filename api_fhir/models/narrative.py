from api_fhir.models import Element


class Narrative(Element):

    resource_type = "Narrative"

    def __init__(self):
        self.div = None  # Type `str`.

        self.status = None  # Type `str`. (generated | extensions | additional | empty)

        super(Narrative, self).__init__()

    class Meta:
        app_label = 'api_fhir'
