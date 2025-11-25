from rest_framework.permissions import BasePermission

class UserDocumentPermission(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.groups.filter(name='admin').exists():
            return True

        if request.user.groups.filter(name="editor").exists():
            return request.method in ('POST', 'PUT', 'PATCH', 'GET')

        if request.user.groups.filter(name="viewer").exists():
            return request.method in ('GET', 'HEAD', 'OPTIONS')

        return False