from rest_framework.permissions import DjangoModelPermissions


class FHIRApiPermissions(DjangoModelPermissions):

    permissions_get = ['%(app_label)s.view_%(model_name)s']
    permissions_post = ['%(app_label)s.add_%(model_name)s']
    permissions_put = ['%(app_label)s.change_%(model_name)s']
    permissions_patch = ['%(app_label)s.change_%(model_name)s']
    permissions_delete = ['%(app_label)s.delete_%(model_name)s']

    def __init__(self):
        self.perms_map['GET'] = self.permissions_get
        self.perms_map['POST'] = self.permissions_post
        self.perms_map['PUT'] = self.permissions_put
        self.perms_map['PATCH'] = self.permissions_patch
        self.perms_map['DELETE'] = self.permissions_delete
