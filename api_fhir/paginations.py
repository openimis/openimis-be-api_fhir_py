from api_fhir.configurations import GeneralConfiguration
from api_fhir.models import Bundle, BundleEntry, BundleType, BundleLink
from api_fhir.models.bundle import BundleLinkRelation

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class FhirBundleResultsSetPagination(PageNumberPagination):

    page_size = GeneralConfiguration.get_default_response_page_size()
    page_query_param = 'page-offset'
    page_size_query_param = '_count'

    def get_paginated_response(self, data):
        return Response(self.build_bundle_set(data).toDict())

    def build_bundle_set(self, data):
        bundle = Bundle()
        bundle.type = BundleType.SEARCHSET.value
        bundle.total = self.page.paginator.count
        self.build_bundle_links(bundle)
        self.build_bundle_entry(bundle, data)
        return bundle

    def build_bundle_links(self, bundle):
        self.build_bundle_link(bundle, BundleLinkRelation.SELF.value, self.request.build_absolute_uri())
        next_link = self.get_next_link()
        if next_link:
            self.build_bundle_link(bundle, BundleLinkRelation.NEXT.value, next_link)
        previous_link = self.get_previous_link()
        if previous_link:
            self.build_bundle_link(bundle, BundleLinkRelation.PREVIOUS.value, previous_link)


    def build_bundle_link(self, bundle, relation, url):
        self_link = BundleLink()
        self_link.relation = relation
        self_link.url = url
        bundle.link.append(self_link)

    def build_bundle_entry(self, bundle, data):
        for obj in data:
            entry = BundleEntry()
            entry.fullUrl = self.build_full_url_for_resource(obj)
            entry.resource = obj
            bundle.entry.append(entry)

    def build_full_url_for_resource(self, fhir_object):
        url = None
        resource_pk = self.get_object_pk(fhir_object)
        if resource_pk:
            url = self.request.build_absolute_uri()
            url = self.exclude_query_parameter_from_url(url)
            url = url + resource_pk
        return url

    def get_object_pk(self, fhir_object):
        pk_id = None
        if isinstance(fhir_object, dict):
            pk_id = fhir_object.get('id')
        return str(pk_id) if pk_id else None

    def exclude_query_parameter_from_url(self, url):
        try:
            from urllib.parse import urlparse  # Python 3
        except ImportError:
            from urlparse import urlparse  # Python 2
        o = urlparse(url)
        return o._replace(query=None).geturl()