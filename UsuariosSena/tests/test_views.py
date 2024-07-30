import unittest
from django.test import Client, TestCase
from django.urls import reverse
from UsuariosSena.models import UsuariosSena, Prestamo, EntregaConsumible
from UsuariosSena.forms import UserLoginForm

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('login_view')
        self.user = UsuariosSena.objects.create_user(
            numeroIdentificacion='1234567890',
            email='testuser@example.com',
            password='password'
        )

    def test_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'indexLogin.html')
        self.assertIsInstance(response.context['form'], UserLoginForm)

    def test_login_view_post_valid(self):
        data = {
            'numeroIdentificacion': '1234567890',
            'password': 'password',
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('homedash'))

    def test_login_view_post_invalid(self):
        data = {
            'numeroIdentificacion': 'wronguser',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, 'Invalid username or password')

class HomeDashViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('homedash')
        self.user = UsuariosSena.objects.create_user(
            numeroIdentificacion='1234567890',
            email='testuser@example.com',
            password='password'
        )
        self.client.login(numeroIdentificacion='1234567890', password='password')

    def test_homedash_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'superAdmin/basedashboard.html')
        self.assertIn('Prestamos', response.context)
        self.assertIn('Entregas', response.context)
        self.assertIn('usuarios', response.context)

import pytest
from django.urls import reverse
from django.test import Client
from UsuariosSena.models import UsuariosSena
from UsuariosSena.forms import UserLoginForm

@pytest.mark.django_db
class TestLoginView:
    def setup_method(self):
        self.client = Client()
        self.url = reverse('login_view')
        self.user = UsuariosSena.objects.create_user(
            numeroIdentificacion='1234567890',
            email='testuser@example.com',
            password='password'
        )

    def test_login_view_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert 'indexLogin.html' in [t.name for t in response.templates]
        assert isinstance(response.context['form'], UserLoginForm)

    def test_login_view_post_valid(self):
        data = {
            'numeroIdentificacion': '1234567890',
            'password': 'password',
        }
        response = self.client.post(self.url, data)
        assert response.status_code == 302
        assert response.url == reverse('homedash')

   
@pytest.mark.django_db
class TestHomeDashView:
    def setup_method(self):
        self.client = Client()
        self.url = reverse('homedash')
        self.user = UsuariosSena.objects.create_user(
            numeroIdentificacion='1234567890',
            email='testuser@example.com',
            password='password'
        )
        self.client.login(numeroIdentificacion='1234567890', password='password')

    def test_homedash_view(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert 'superAdmin/basedashboard.html' in [t.name for t in response.templates]
        assert 'Prestamos' in response.context
        assert 'Entregas' in response.context
        assert 'usuarios' in response.context
