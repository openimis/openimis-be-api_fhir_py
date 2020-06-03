from api_fhir_R4.models import Element, Property


class Attachment(Element):

    contentType = Property('contentType', str)
    language = Property('language', str)
    data = Property('data', str)  # Data inline, base64ed
    url = Property('url', str)
    size = Property('size', int)
    hash = Property('hash', str)  # Hash of the data (sha-1, base64ed
    title = Property('title', str)
    creation = Property('creation', 'FHIRDate')

