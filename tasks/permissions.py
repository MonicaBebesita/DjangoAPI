from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):

    """
    Permiso personalizado para permitir solo a los dueños de un objeto editarlo
    """
    def has_object_permission(self, request, view, obj):

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
             return True

        # El permiso de escritura solo se concede al dueño de la tarea
        return obj.user == request.user