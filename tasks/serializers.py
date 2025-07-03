from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    # El usuario se asigna automáticamente desde la vista, por eso es solo lectura
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'user']

    def validate_title(self, value):

        """
        Valida que el título tenga al menos 3 caracteres
        """

        if len(value) < 3:
            raise serializers.ValidationError("El título debe tener al menos 3 caracteres.")
        return value