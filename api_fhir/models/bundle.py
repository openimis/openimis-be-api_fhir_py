from enum import Enum

from api_fhir.models import Resource, Property, BackboneElement


class BundleLink(BackboneElement):

    relation = Property('relation', str, required=True)
    url = Property('url', str, required=True)


class BundleEntrySearch(BackboneElement):

    mode = Property('mode', str)
    score = Property('score', float)


class BundleEntryRequest(BackboneElement):

    method = Property('method', str, required=True)
    url = Property('url', str, required=True)
    ifNoneMatch = Property('ifNoneMatch', str)
    ifModifiedSince = Property('ifModifiedSince', 'FHIRDate')
    ifMatch = Property('ifMatch', str)
    ifNoneExist = Property('ifNoneExist', str)


class BundleEntryResponse(BackboneElement):

    status = Property('status', str, required=True)
    location = Property('location', str)
    etag = Property('etag', str)
    lastModified = Property('lastModified', 'FHIRDate')
    outcome = Property('outcome', 'Resource')


class BundleEntry(BackboneElement):

    link = Property('link', 'BundleLink', count_max='*')
    fullUrl = Property('fullUrl', str)
    resource = Property('resource', 'Resource')
    search = Property('search', 'BundleEntrySearch')
    request = Property('request', 'BundleEntryRequest')
    response = Property('response', 'BundleEntryResponse')


class Bundle(Resource):

    identifier = Property('identifier', 'Identifier')
    type = Property('type', str, required=True)
    total = Property('total', int)
    link = Property('link', 'BundleLink', count_max='*')
    entry = Property('entry', 'BundleEntry', count_max='*')
    signature = Property('signature', 'Signature')


class BundleType(Enum):
    DOCUMENT = "document"
    MESSAGE = "message"
    TRANSACTION = "transaction"
    TRANSACTION_RESPONSE = "transaction-response"
    BATCH = "batch"
    BATCH_RESPONSE = "batch-response"
    HISTORY = "history"
    SEARCHSET = "searchset"
    COLLECTION = "collection"

class BundleLinkRelation(Enum):
    SELF = "self"
    NEXT = "next"
    PREVIOUS = "previous"
    LAST = "last"
    FIRST = "first"
