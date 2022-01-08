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

class RegisterTestSelenium(LiveServerTestCase, BaseTestCase):
    def test_singup(self):
        selenium = webdriver.Chrome()
        selenium.get('http://localhost:8000/account/signup/')

        userUser = selenium.find_element_by_name('username')
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userUser.send_keys('l')
        userEmail.send_keys('l@gmail.com')
        userPass.send_keys('galaroza',Keys.ENTER)

        time.sleep(5)

        assert 'correctamente' in selenium.page_source
    
    def test_singup_registrado(self):
        selenium = webdriver.Chrome()
        selenium.get('http://localhost:8000/account/signup/')

        userUser = selenium.find_element_by_name('username')
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userUser.send_keys('l')
        userEmail.send_keys('l@gmail.com')
        userPass.send_keys('galaroza',Keys.ENTER)

        time.sleep(5)

        assert 'ya ha sido registrado' in selenium.page_source
        
    def test_singup_vacio(self):
        selenium = webdriver.Chrome()
        selenium.get('http://localhost:8000/account/signup/')
      
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userEmail.send_keys('')
        userPass.send_keys('',Keys.ENTER)

        time.sleep(5)

        assert 'account/signup' in selenium.current_url    

    def test_login_sin_registro(self):
        selenium = webdriver.Chrome()
        selenium.get('http://localhost:8000/account/login/')

        time.sleep(5)
      
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userEmail.send_keys('l@gmail.com')
        userPass.send_keys('galaroza',Keys.ENTER)

        time.sleep(5)

        assert 'account/login' in selenium.current_url


    def test_u_login(self):
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

    def test_validation_email(self):
        selenium = webdriver.Chrome()
        selenium.get('http://localhost:8000/account/signup/')
      
        userUser = selenium.find_element_by_name('username')
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userUser.send_keys('l')
        userEmail.send_keys('l@gmail.com')
        userPass.send_keys('galaroza',Keys.ENTER)

        time.sleep(5)

        assert 'account/signup' in selenium.current_url

    def test_validation_password(self):
        selenium = webdriver.Chrome()
        selenium.get('http://localhost:8000/account/signup/')
      
        userUser = selenium.find_element_by_name('username')
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userUser.send_keys('l')
        userEmail.send_keys('l@gmail.com')
        userPass.send_keys('g',Keys.ENTER)

        time.sleep(10)

        assert 'account/signup' in selenium.current_url