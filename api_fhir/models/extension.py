from api_fhir.models.element import Element


class Extension(Element):

    resource_type = "Extension"

    def __init__(self):
        self.url = None  # Type `str`

        self.valueAddress = None  # Type `Address` (represented as `dict` in JSON).

        self.valueAge = None  # Type `Age` (represented as `dict` in JSON).

        self.valueAnnotation = None  # Type `Annotation` (represented as `dict` in JSON).

        self.valueAttachment = None  # Type `Attachment` (represented as `dict` in JSON).

        self.valueBase64Binary = None  # Type `str`.

        self.valueBoolean = None  # Type `bool`.

        self.valueCode = None  # Type `str`.

        self.valueCodeableConcept = None  # Type `CodeableConcept` (represented as `dict` in JSON).

        self.valueCoding = None  # Type `Coding` (represented as `dict` in JSON).

        self.valueContactPoint = None  # Type `ContactPoint` (represented as `dict` in JSON).

        self.valueCount = None  # Type `Count` (represented as `dict` in JSON).

        self.valueDate = None  # Type `FHIRDate` (represented as `str` in JSON).

        self.valueDateTime = None  # Type `FHIRDate` (represented as `str` in JSON).

        self.valueDecimal = None  # Type `float`.

        self.valueDistance = None  # Type `Distance` (represented as `dict` in JSON).

        self.valueDuration = None  # Type `Duration` (represented as `dict` in JSON).

        self.valueHumanName = None  # Type `HumanName` (represented as `dict` in JSON).

        self.valueId = None  # Type `str`.

        self.valueIdentifier = None  # Type `Identifier` (represented as `dict` in JSON).

        self.valueInstant = None  # Type `FHIRDate` (represented as `str` in JSON).

        self.valueInteger = None  # Type `int`.

        self.valueMarkdown = None  # Type `str`.

        self.valueMeta = None  # Type `Meta` (represented as `dict` in JSON).

        self.valueMoney = None  # Type `Money` (represented as `dict` in JSON).

        self.valueOid = None  # Type `str`.

        self.valuePeriod = None  # Type `Period` (represented as `dict` in JSON).

        self.valuePositiveInt = None  # Type `int`.

        self.valueQuantity = None  # Type `Quantity` (represented as `dict` in JSON).

        self.valueRange = None  # Type `Range` (represented as `dict` in JSON).

        self.valueRatio = None  # Type `Ratio` (represented as `dict` in JSON).

        self.valueReference = None  # Type `Reference` (represented as `dict` in JSON).

        self.valueSampledData = None  # Type `SampledData` (represented as `dict` in JSON).

        self.valueSignature = None  # Type `Signature` (represented as `dict` in JSON).

        self.valueString = None  # Type `str`.

        self.valueTime = None  # Type `FHIRDate` (represented as `str` in JSON).

        self.valueTiming = None  # Type `Timing` (represented as `dict` in JSON).

        self.valueUnsignedInt = None  # Type `int`.

        self.valueUri = None  # Type `str`.

        super(Extension, self).__init__()

    class Meta:
        app_label = 'api_fhir'
