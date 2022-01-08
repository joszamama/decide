import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from base.tests import BaseTestCase

BASEURL = 'https://localhost:8000/account/login/'

PROFILE_WEB = 'https://localhost:8000/account/profile/'

class LoginTestSelenium(LiveServerTestCase):

      def testLogin(self):
            selenium = webdriver.Chrome()
            selenium.get(BASEURL)

            acceptButton=selenium.find_element_by_id('details-button')
            acceptButton.click()
            time.sleep(2)
            
            goButton=selenium.find_element_by_id('proceed-link')
            goButton.click()
            time.sleep(3)
      
            userEmail = selenium.find_element_by_name('email')
            userPass = selenium.find_element_by_name('password')

            userEmail.send_keys('prueba2k22@gmail.com')
            userPass.send_keys('1234',Keys.ENTER)

            time.sleep(5)

            assert ('prueba2k22@gmail.com' in selenium.page_source) and (PROFILE_WEB in selenium.current_url)

   
      def testLoginWithWrongPassword(self):
            selenium = webdriver.Chrome()
            selenium.get(BASEURL)

            acceptButton=selenium.find_element_by_id('details-button')
            acceptButton.click()
            time.sleep(2)
            
            goButton=selenium.find_element_by_id('proceed-link')
            goButton.click()
            time.sleep(3)

            userEmail = selenium.find_element_by_name('email')
            userPass = selenium.find_element_by_name('password')

            userEmail.send_keys('prueba2k22@gmail.com')
            userPass.send_keys('contraseñaErronea',Keys.ENTER)

            time.sleep(5)

            assert ('Usuario o contraseña incorrecta' in selenium.page_source)and (BASEURL in selenium.current_url)


      def testLoginWithNoFields(self):
            selenium = webdriver.Chrome()
            selenium.get(BASEURL)

            acceptButton=selenium.find_element_by_id('details-button')
            acceptButton.click()
            time.sleep(2)
            
            goButton=selenium.find_element_by_id('proceed-link')
            goButton.click()
            time.sleep(3)
      
            userEmail = selenium.find_element_by_name('email')
            userPass = selenium.find_element_by_name('password')

            userEmail.send_keys('')
            userPass.send_keys('',Keys.ENTER)

            time.sleep(5)

            assert BASEURL in selenium.current_url