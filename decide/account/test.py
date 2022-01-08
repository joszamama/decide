import time
import selenium
from selenium import webdriver
from django.test import LiveServerTestCase
from base.tests import BaseTestCase
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User


BASEURL = 'https://localhost:8000/account/login/' #Introducir URL del login

PROFILE_WEB = 'https://localhost:8000/account/profile/' #Introducir URL de login correcto

#Variables para LoginRSTestSelenium
USER_TWITCH = '' #Introducir usuario de Twitch para las pruebas
PASSWORD_TWITCH = '' #Introducir contraseña de Twitch para las pruebas

USER_TWITTER = '' #Introducir usuario de Twitter para las pruebas
PASSWORD_TWITTER = '' #Introducir contraseña de Twitter para las pruebas

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


class LoginRSTestSelenium(LiveServerTestCase):                  #Estos tests deben realizarse obligatoriamente usando https.
  
     
    def testAccederFacebook(self):
        selenium = webdriver.Chrome()
        selenium.get(BASEURL)
            
        acceptButton=selenium.find_element_by_id('details-button')
        acceptButton.click()
        time.sleep(2)
            
        goButton=selenium.find_element_by_id('proceed-link')
        goButton.click()
        time.sleep(3)

        facebookButton = selenium.find_element_by_name('facebookButton')
        facebookButton.click()
        time.sleep(3)  

        assert 'https://www.facebook.com/login.php' in selenium.current_url

    def testAccederTwitch(self):
        selenium = webdriver.Chrome()
        selenium.get(BASEURL)
            
        acceptButton=selenium.find_element_by_id('details-button')
        acceptButton.click()
        time.sleep(2)
            
        goButton=selenium.find_element_by_id('proceed-link')
        goButton.click()
        time.sleep(3)

        twitchButton = selenium.find_element_by_name('twitchButton')
        twitchButton.click()
        time.sleep(3) 

        username = selenium.find_element_by_id('login-username')
        userPass = selenium.find_element_by_id('password-input')

        username.send_keys(USER_TWITCH)
        userPass.send_keys(PASSWORD_TWITCH,Keys.ENTER)

        time.sleep(3)  

        assert ('Introduce el código que encontrarás en la aplicación de autenticación o solicítalo mediante un SMS.' in selenium.page_source) and ('https://www.twitch.tv/login' in selenium.current_url)

    def testAccederTwitter(self):
        selenium = webdriver.Chrome()
        selenium.get(BASEURL)
            
        acceptButton=selenium.find_element_by_id('details-button')
        acceptButton.click()
        time.sleep(2)
            
        goButton=selenium.find_element_by_id('proceed-link')
        goButton.click()
        time.sleep(3)

        twitterButton = selenium.find_element_by_name('twitterButton')
        twitterButton.click()
        time.sleep(3)  

        username = selenium.find_element_by_id('username_or_email')
        userPass = selenium.find_element_by_id('password')

        username.send_keys(USER_TWITTER)
        userPass.send_keys(PASSWORD_TWITTER,Keys.ENTER)
        time.sleep(3)

        assert (PROFILE_WEB in selenium.current_url) and (USER_TWITTER in selenium.page_source)

