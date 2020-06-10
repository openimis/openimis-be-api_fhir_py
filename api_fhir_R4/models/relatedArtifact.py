from api_fhir_R4.models import Element, Property
from enum import Enum


class RelatedArtifact(Element):

    type = Property('type', str, required=True)
    label = Property('label', str)
    display = Property('display', str)
    citation = Property('citation', str)
    url = Property('url', str)
    document = Property('document', 'Attachment')
    resource = Property('resource', str)  # canonical 'Any'


class RelatedArtifactType(Enum):

    DOCUMENTATION = 'documentation'
    JUSTIFICATION = 'justification'
    CITATION = 'citation'
    PREDECESSOR = 'predecessor'
    SUCCESSOR = 'successor'
    DERIVED_FROM = 'derived-from'
    DEPENDS_ON = 'depends-on'
    COMPOSED_OF = 'composed-of'