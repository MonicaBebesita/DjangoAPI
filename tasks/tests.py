# tasks/tests.py

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task

class TaskAPITests(APITestCase):
    def setUp(self):
        # Crear dos usuarios para las pruebas
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        # Crear una tarea para el usuario 1
        self.task1 = Task.objects.create(title="Tarea de user1", user=self.user1)

    def test_list_tasks_authenticated(self):
        """
        Asegura que un usuario autenticado puede listar sus propias tareas.
        """
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Tarea de user1')

    def test_list_tasks_unauthenticated(self):
        """
        Asegura que un usuario no autenticado no puede listar tareas.
        """
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task(self):
        """
        Asegura que un usuario autenticado puede crear una nueva tarea.
        """
        self.client.force_authenticate(user=self.user2)
        data = {'title': 'Nueva Tarea', 'description': 'Descripción de la tarea'}
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        # Verifica que la tarea se asignó al usuario correcto
        self.assertEqual(Task.objects.last().user, self.user2)

    def test_title_validation(self):
        """
        Asegura que el título debe tener al menos 3 caracteres.
        """
        self.client.force_authenticate(user=self.user1)
        data = {'title': 'ab'}
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_user_cannot_access_other_user_task(self):
        """
        Asegura que un usuario no puede ver, actualizar o eliminar la tarea de otro.
        """
        self.client.force_authenticate(user=self.user2)
        
        # GET (detalle)
        response_get = self.client.get(f'/api/tasks/{self.task1.id}/')
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)
        
        # PUT
        data = {'title': 'Título actualizado'}
        response_put = self.client.put(f'/api/tasks/{self.task1.id}/', data)
        self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)

        # DELETE
        response_delete = self.client.delete(f'/api/tasks/{self.task1.id}/')
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)
