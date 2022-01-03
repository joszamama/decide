from django.http import request
from django.utils import timezone
from django.conf import settings
from django.test import TestCase

import random
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from base import mods
from base.tests import BaseTestCase
from account import views
from account.forms import UserForm
import requests
import sys

class AccountTestCase(BaseTestCase):

    # def test_add_user_empty(self):
    #     usuarios = User.objects.count()
    #     user = User()
    #     user.username = 'prueba'
    #     user.email = 'prueba'
    #     user.set_password('prueba')
    #     user.save()
    #     self.assertEqual(usuarios, User.objects.count() - 1)

    # def setUp(self):
    #     usuarios = User.objects.count()
    #     user = User()
    #     user.username = 'prueba'
    #     user.email = 'prueba'
    #     user.set_password('prueba')
    #     user.save()

    # def tearDown(self):
    #     self.client = None

    def test_add_user_empty(self):
        usuarios = User.objects.count()
        # form_data = {'email': '', 'password': ''}
        # resp = requests.post('http://localhost:8000/account/login/', cookie=csrftoken, data=form_data)
        # self.assertEqual(resp.status_code, 400)
        URL = 'http://localhost:8000/account/signup/'

        client = requests.session()

        # Retrieve the CSRF token first
        client.get(URL)  # sets cookie
        if 'csrftoken' in client.cookies:
            # Django 1.6 and up
            csrftoken = client.cookies['csrftoken']
        else:
            # older versions
            csrftoken = client.cookies['csrf']

        data = dict(username='prueba', email='prueba@gmail.com', password='p', csrfmiddlewaretoken=csrftoken, next='/')
        r = client.post(URL, data=data, headers=dict(Referer=URL))
        self.assertEqual(usuarios, User.objects.count())

    def test_login(self):
        # form_data = {'email': '', 'password': ''}
        # resp = requests.post('http://localhost:8000/account/login/', cookie=csrftoken, data=form_data)
        # self.assertEqual(resp.status_code, 400)
        URL = 'http://localhost:8000/account/login/'

        client = requests.session()

        # Retrieve the CSRF token first
        client.get(URL)  # sets cookie
        if 'csrftoken' in client.cookies:
            # Django 1.6 and up
            csrftoken = client.cookies['csrftoken']
        else:
            # older versions
            csrftoken = client.cookies['csrf']

        login_data = dict(email='ja@gmail.com', password='ja', csrfmiddlewaretoken=csrftoken, next='/')
        r = client.post(URL, data=login_data, headers=dict(Referer=URL))
        self.assertEqual(r.status_code, 200)