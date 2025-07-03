from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwner
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        Esta vista debe devolver una lista de todas las tareas
        para el usuario autenticado actualmente.
        """
        return self.request.user.tasks.all().order_by('-created_at')

    def perform_create(self, serializer):
        """
        Asigna el usuario autenticado al crear una nueva tarea.
        """
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Listar todas las tareas del usuario autenticado",
        description="Recupera una lista de todas las tareas asociadas al usuario que ha iniciado sesión. Solo se muestran las tareas que pertenecen al usuario.",
        responses={
            status.HTTP_200_OK: TaskSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: {"description": "No autenticado. Se requiere un token JWT válido."}
        },
        examples=[
            OpenApiExample(
                "Ejemplo de respuesta exitosa",
                value=[
                    {"id": 1, "title": "Comprar leche", "description": "No olvidar la lista de compras", "completed": False, "created_at": "2023-10-27T10:00:00Z", "user": "user1"},
                    {"id": 2, "title": "Enviar informe", "description": "Informe mensual a gerencia", "completed": True, "created_at": "2023-10-26T15:30:00Z", "user": "user1"}
                ],
                response_only=True,
                media_type="application/json",
                status_codes=["200"]
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Crear una nueva tarea",
        description="Crea una nueva tarea para el usuario autenticado. El usuario se asigna automáticamente.",
        request=TaskSerializer,
        responses={
            status.HTTP_201_CREATED: TaskSerializer,
            status.HTTP_400_BAD_REQUEST: {"description": "Datos de entrada inválidos. El título debe tener al menos 3 caracteres."},
            status.HTTP_401_UNAUTHORIZED: {"description": "No autenticado. Se requiere un token JWT válido."}
        },
        examples=[
            OpenApiExample(
                "Ejemplo de solicitud para crear una tarea",
                request_only=True,
                media_type="application/json",
                value={"title": "Organizar escritorio", "description": "Clasificar documentos y limpiar"}
            ),
            OpenApiExample(
                "Ejemplo de respuesta de tarea creada",
                value={"id": 3, "title": "Organizar escritorio", "description": "Clasificar documentos y limpiar", "completed": False, "created_at": "2023-10-27T11:00:00Z", "user": "user1"},
                response_only=True,
                media_type="application/json",
                status_codes=["201"]
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Recuperar una tarea específica",
        description="Obtiene los detalles de una tarea específica por su ID. Solo accesible si la tarea pertenece al usuario autenticado.",
        responses={
            status.HTTP_200_OK: TaskSerializer,
            status.HTTP_401_UNAUTHORIZED: {"description": "No autenticado."},
            status.HTTP_404_NOT_FOUND: {"description": "Tarea no encontrada o no pertenece al usuario autenticado."}
        },
        parameters=[
            OpenApiParameter(
                name="pk",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID de la tarea a recuperar.",
                required=True,
            ),
        ],
        examples=[
            OpenApiExample(
                "Ejemplo de respuesta exitosa",
                value={"id": 1, "title": "Comprar leche", "description": "No olvidar la lista de compras", "completed": False, "created_at": "2023-10-27T10:00:00Z", "user": "user1"},
                response_only=True,
                media_type="application/json",
                status_codes=["200"]
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar parcialmente una tarea",
        description="Actualiza uno o más campos de una tarea existente. La tarea debe pertenecer al usuario autenticado.",
        request=TaskSerializer(partial=True),
        responses={
            status.HTTP_200_OK: TaskSerializer,
            status.HTTP_400_BAD_REQUEST: {"description": "Datos de entrada inválidos."},
            status.HTTP_401_UNAUTHORIZED: {"description": "No autenticado."},
            status.HTTP_404_NOT_FOUND: {"description": "Tarea no encontrada o no pertenece al usuario autenticado."}
        },
        parameters=[
            OpenApiParameter(
                name="pk",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID de la tarea a actualizar.",
                required=True,
            ),
        ],
        examples=[
            OpenApiExample(
                "Ejemplo de solicitud para marcar tarea como completada",
                request_only=True,
                media_type="application/json",
                value={"completed": True}
            ),
            OpenApiExample(
                "Ejemplo de respuesta de tarea actualizada",
                value={"id": 1, "title": "Comprar leche", "description": "No olvidar la lista de compras", "completed": True, "created_at": "2023-10-27T10:00:00Z", "user": "user1"},
                response_only=True,
                media_type="application/json",
                status_codes=["200"]
            )
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar completamente una tarea",
        description="Reemplaza todos los campos de una tarea existente con los datos proporcionados. La tarea debe pertenecer al usuario autenticado.",
        request=TaskSerializer,
        responses={
            status.HTTP_200_OK: TaskSerializer,
            status.HTTP_400_BAD_REQUEST: {"description": "Datos de entrada inválidos."},
            status.HTTP_401_UNAUTHORIZED: {"description": "No autenticado."},
            status.HTTP_404_NOT_FOUND: {"description": "Tarea no encontrada o no pertenece al usuario autenticado."}
        },
        parameters=[
            OpenApiParameter(
                name="pk",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID de la tarea a actualizar.",
                required=True,
            ),
        ],
        examples=[
            OpenApiExample(
                "Ejemplo de solicitud de actualización completa",
                request_only=True,
                media_type="application/json",
                value={"title": "Nueva tarea completa", "description": "Descripción actualizada", "completed": False}
            ),
            OpenApiExample(
                "Ejemplo de respuesta de tarea actualizada completamente",
                value={"id": 1, "title": "Nueva tarea completa", "description": "Descripción actualizada", "completed": False, "created_at": "2023-10-27T10:00:00Z", "user": "user1"},
                response_only=True,
                media_type="application/json",
                status_codes=["200"]
            )
        ]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Eliminar una tarea",
        description="Elimina una tarea específica por su ID. La tarea debe pertenecer al usuario autenticado.",
        responses={
            status.HTTP_204_NO_CONTENT: {"description": "Tarea eliminada exitosamente."},
            status.HTTP_401_UNAUTHORIZED: {"description": "No autenticado."},
            status.HTTP_404_NOT_FOUND: {"description": "Tarea no encontrada o no pertenece al usuario autenticado."}
        },
        parameters=[
            OpenApiParameter(
                name="pk",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID de la tarea a eliminar.",
                required=True,
            ),
        ],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)