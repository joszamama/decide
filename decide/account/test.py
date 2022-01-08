import time
from django.test import LiveServerTestCase
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User

BASEURL='https://localhost:8000/account/login/'

PROFILE_WEB = 'https://localhost:8000/account/profile/'

USER_TWITCH = 'ProjectTrys' #Introducir usuario de Twitch para las pruebas
PASSWORD_TWITCH = 'Cpa3q7MtgyHJhCn' #Introducir contraseña de Twitch para las pruebas

class LoginRSTestSelenium(LiveServerTestCase):                  #Estos tests deben realizarse usando https.
  
     
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