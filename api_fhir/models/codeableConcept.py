from api_fhir.models.element import Element


class CodeableConcept(Element):

    resource_type = "CodeableConcept"

    def __init__(self):
        self.coding = None  # List of `Coding` items (represented as `dict` in JSON)

        self.text = None  # Type `str`

        super(CodeableConcept, self).__init__()

    class Meta:
        app_label = 'api_fhir'
