from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status 


@extend_schema(
    summary="Obtener Token de Acceso JWT y Refresh Token",
    description="Permite a un usuario autenticarse con sus credenciales (username y password) y obtener un par de tokens JWT: un token de acceso (access token) y un token de refresco (refresh token). El access token se utiliza para autenticar futuras solicitudes a la API.",
    request={"application/json": {"username": "string", "password": "string"}},
    responses={
        status.HTTP_200_OK: {
            "description": "Autenticación exitosa. Tokens generados.",
            "examples": {
                "application/json": {
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Credenciales inválidas. Usuario o contraseña incorrectos."
        }
    },
    examples=[
        OpenApiExample(
            "Ejemplo de solicitud de token",
            request_only=True,
            media_type="application/json",
            value={"username": "tu_usuario", "password": "tu_contraseña"}
        )
    ]
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(
    summary="Refrescar Token de Acceso JWT",
    description="Utiliza un refresh token válido para obtener un nuevo access token. Esto es útil para mantener la sesión del usuario sin necesidad de que se autentique repetidamente con sus credenciales.",
    request={"application/json": {"refresh": "string"}},
    responses={
        status.HTTP_200_OK: {
            "description": "Token de acceso refrescado exitosamente.",
            "examples": {
                "application/json": {
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Token de refresco inválido o expirado."
        }
    },
    examples=[
        OpenApiExample(
            "Ejemplo de solicitud de refresco de token",
            request_only=True,
            media_type="application/json",
            value={"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
        )
    ]
)
class CustomTokenRefreshView(TokenRefreshView):
    pass


urlpatterns = [
    path('admin/', admin.site.urls),

    # Endpoints de la API de Tareas
    path('api/', include('tasks.urls')),

    # Endpoints de Autenticación JWT con descripciones personalizadas
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    # Endpoints de Documentación (Swagger/OpenAPI)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]