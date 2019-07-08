from api_fhir.models import Element, Property


class Attachment(Element):

    contentType = Property('contentType', str)
    creation = Property('creation', 'FHIRDate')
    data = Property('data', str)  # Data inline, base64ed
    hash = Property('hash', str)  # Hash of the data (sha-1, base64ed
    language = Property('language', str)
    size = Property('size', int)
    title = Property('title', str)
    url = Property('url', str)
