import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User

class LoginTestSelenium(LiveServerTestCase):

  def createUserInDB(self):
        user = User()
        user.username = 'Prueba2k22'
        user.email = 'prueba2k22@gmail.com'
        user.set_password('prueba')
        user.save()


  def testLogin(self):
        selenium = webdriver.Chrome()
        selenium.get('http://localhost:8000/account/login/')

        time.sleep(5)
    
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userEmail.send_keys('prueba2k22@gmail.com')
        userPass.send_keys('1234',Keys.ENTER)

        time.sleep(5)

        assert 'prueba2k22@gmail.com' in selenium.page_source

   
  def testLoginWithWrongPassword(self):
        selenium = webdriver.Chrome()
        selenium.get('http://localhost:8000/account/login/')

        time.sleep(5)

        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userEmail.send_keys('prueba2k22@gmail.com')
        userPass.send_keys('contraseñaErronea',Keys.ENTER)

        time.sleep(5)

        assert 'Usuario o contraseña incorrecta' in selenium.page_source