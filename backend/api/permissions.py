from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Permissão base para garantir que o usuário
    só acesse seus próprios dados.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user