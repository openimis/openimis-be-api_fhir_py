from api_fhir.models import Element


class Signature(Element):

    resource_type = "Signature"

    def __init__(self):
        self.blob = None  # Type `str`.

        self.contentType = None  # Type `str`.

        self.onBehalfOfReference = None  #Type `FHIRReference` referencing `Practitioner, RelatedPerson, Patient, Device, Organization` (represented as `dict` in JSON).

        self.onBehalfOfUri = None  # Type `str`.

        self.type = None  # List of `Coding` items (represented as `dict` in JSON).

        self.when = None  # Type `FHIRDate` (represented as `str` in JSON).

        self.whoReference = None  # Type `Reference` referencing `Practitioner, RelatedPerson, Patient, Device, Organization` (represented as `dict` in JSON).

        self.whoUri = None  # Type `str`.

        super(Signature, self).__init__()

    class Meta:
        app_label = 'api_fhir'
