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

class UpdateTestSelenium(LiveServerTestCase):
    def test_update_user(self):
        selenium = webdriver.Chrome()
        selenium.get('http://localhost:8000/account/login/')
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userEmail.send_keys('danirc2001@gmail.com')
        userPass.send_keys('aa',Keys.ENTER)
        
        
        selenium.get('http://localhost:8000/account/update/')
        userPass = selenium.find_element_by_name('password')

        userPass.send_keys('aa',Keys.ENTER)

        time.sleep(5)
        assert 'cambiados correctamente' in selenium.page_source

        
    
    def test_update_user_exist(self):
        selenium = webdriver.Chrome()
        selenium.get('http://localhost:8000/account/login/')
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userEmail.send_keys('danirc2001@gmail.com')
        userPass.send_keys('aa',Keys.ENTER)
        
        
        selenium.get('http://localhost:8000/account/update/')
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userEmail.clear()

        userEmail.send_keys('danirc2000@gmail.com')
        userPass.send_keys('aa',Keys.ENTER)

        time.sleep(5)

        assert 'ya existe en la BD' in selenium.page_source