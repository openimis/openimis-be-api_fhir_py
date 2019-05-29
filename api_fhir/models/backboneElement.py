from api_fhir.models.element import Element


class BackboneElement(Element):

    resource_type = "BackboneElement"

    def __init__(self):
        self.modifierExtension = None  # List of `Extension` items (represented as `dict` in JSON).

        super(BackboneElement, self).__init__()

    class Meta:
        app_label = 'api_fhir'
