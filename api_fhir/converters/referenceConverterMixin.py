import inspect

from api_fhir.exceptions import FHIRRequestProcessException
from api_fhir.models import Reference


class ReferenceConverterMixin(object):

    @classmethod
    def get_reference_obj_id(cls, obj):
        raise NotImplementedError('`get_imis_object_id()` must be implemented.')  # pragma: no cover

    @classmethod
    def get_fhir_resource_type(cls):
        raise NotImplementedError('`get_fhir_resource_type()` must be implemented.')  # pragma: no cover

    @classmethod
    def get_imis_obj_by_fhir_reference(cls, reference, errors=None):
        raise NotImplementedError('`get_imis_object_by_fhir_reference()` must be implemented.')  # pragma: no cover

    @classmethod
    def build_fhir_resource_reference(cls, obj):
        reference = Reference()
        resource_type = cls.__get_fhir_resource_type_as_string()
        resource_id = cls.__get_imis_object_id_as_string(obj)
        reference.reference = resource_type + '/' + resource_id
        return reference

    @classmethod
    def get_resource_id_from_reference(cls, reference):
        resource_id = None
        if reference:
            reference = reference.reference
            if isinstance(reference, str) and '/' in reference:
                path, resource_id = reference.rsplit('/', 1)
        if resource_id is None:
            raise FHIRRequestProcessException(['Could not fetch id from reference: {}'])
        return resource_id

    @classmethod
    def __get_imis_object_id_as_string(cls, obj):
        resource_id = cls.get_reference_obj_id(obj)
        if not isinstance(resource_id, str):
            resource_id = str(resource_id)
        return resource_id

    @classmethod
    def __get_fhir_resource_type_as_string(cls):
        resource_type = cls.get_fhir_resource_type()
        if inspect.isclass(resource_type):
            resource_type = resource_type.__name__
        if not isinstance(resource_type, str):
            resource_type = str(resource_type)
        return resource_type
