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
import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class RegisterTestSelenium(LiveServerTestCase):
    def test_add_user(self):
        selenium = webdriver.Chrome()
        selenium.get('http://localhost:8000/account/signup/')

        userUser = selenium.find_element_by_name('username')
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userUser.send_keys('l')
        userEmail.send_keys('l@gmail.com')
        userPass.send_keys('l',Keys.ENTER)

        time.sleep(5)

        assert 'correctamente' in selenium.page_source
    
    def test_add_user_registered(self):
        selenium = webdriver.Chrome()
        selenium.get('http://localhost:8000/account/signup/')

        userUser = selenium.find_element_by_name('username')
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userUser.send_keys('l')
        userEmail.send_keys('l@gmail.com')
        userPass.send_keys('l',Keys.ENTER)

        time.sleep(5)

        assert 'ya ha sido registrado' in selenium.page_source

class LoginTestUnit(BaseTestCase):
    def test_login(self):
        URL = 'http://localhost:8000/account/login/'

        client = requests.session()

        client.get(URL)  
        if 'csrftoken' in client.cookies:
            csrftoken = client.cookies['csrftoken']
        else:
            csrftoken = client.cookies['csrf']

        login_data = dict(email='l@gmail.com', password='l', csrfmiddlewaretoken=csrftoken, next='/')
        r = client.post(URL, data=login_data, headers=dict(Referer=URL))
        self.assertEqual(r.status_code, 200)
