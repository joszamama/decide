import time
import selenium
from selenium import webdriver
from django.test import LiveServerTestCase
from base.tests import BaseTestCase
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
import requests

BASEURL = 'https://localhost:8000/account/login/' #Introducir URL del login

BASEURLSINSSL = 'http://localhost:8000/account/login/' 

BASEURLSIGN_NOSSL = 'http://localhost:8000/account/signup/' 

BASEURLSIGN = 'https://localhost:8000/account/signup/'

PROFILE_WEB = 'https://localhost:8000/account/profile/' #Introducir URL de login correcto

UPDATE_WEB = 'https://localhost:8000/account/update/'

#Variables para LoginRSTestSelenium ----------------------------------------------
USER_TWITCH = 'ProjectTrys' #Introducir usuario de Twitch para las pruebas
PASSWORD_TWITCH = 'Cpa3q7MtgyHJhCn' #Introducir contraseña de Twitch para las pruebas

USER_TWITTER = 'pruebaproyectos00@gmail.com' #Introducir usuario de Twitter para las pruebas
PASSWORD_TWITTER = '3Db5hz6rQcZ6mSb' #Introducir contraseña de Twitter para las pruebas

USER_GOOGLE = 'decide.99.mulhacen@gmail.com' #Introducir usuario de Google para las pruebas
PASSWORD_GOOGLE = '#RxCNYkEwoGy' #Introducir contraseña de Google para las pruebas
#----------------------------------------------------------------------------------

#Estos tests deben realizarse obligatoriamente usando https------------------------

class LoginRegisterTestSelenium(LiveServerTestCase):

        def test_a_login_sin_registro(self):
            selenium = webdriver.Chrome()
            selenium.get(BASEURL)

            acceptButton=selenium.find_element_by_id('details-button')
            acceptButton.click()
            time.sleep(2)
                
            goButton=selenium.find_element_by_id('proceed-link')
            goButton.click()
            time.sleep(2)

            time.sleep(5)
        
            userEmail = selenium.find_element_by_name('email')
            userPass = selenium.find_element_by_name('password')

            userEmail.send_keys('l@gmail.com')
            userPass.send_keys('galaroza',Keys.ENTER)

            time.sleep(5)

            assert 'account/login' in selenium.current_url

        def test_b_signup(self):
            selenium = webdriver.Chrome()
            selenium.get(BASEURLSIGN)

            acceptButton=selenium.find_element_by_id('details-button')
            acceptButton.click()
            time.sleep(2)
                
            goButton=selenium.find_element_by_id('proceed-link')
            goButton.click()
            time.sleep(2)

            userUser = selenium.find_element_by_name('username')
            userEmail = selenium.find_element_by_name('email')
            userPass = selenium.find_element_by_name('password')

            userUser.send_keys('l')
            userEmail.send_keys('l@gmail.com')
            userPass.send_keys('galaroza',Keys.ENTER)

            time.sleep(5)

            assert 'correctamente' in selenium.page_source
        
        def test_c_signup_registrado(self):
            selenium = webdriver.Chrome()
            selenium.get(BASEURLSIGN)

            acceptButton=selenium.find_element_by_id('details-button')
            acceptButton.click()
            time.sleep(2)
                
            goButton=selenium.find_element_by_id('proceed-link')
            goButton.click()
            time.sleep(2)

            userUser = selenium.find_element_by_name('username')
            userEmail = selenium.find_element_by_name('email')
            userPass = selenium.find_element_by_name('password')

            userUser.send_keys('l')
            userEmail.send_keys('l@gmail.com')
            userPass.send_keys('galaroza',Keys.ENTER)

            time.sleep(5)

            assert 'ya ha sido registrado' in selenium.page_source
            
        def test_d_singup_vacio(self):
            selenium = webdriver.Chrome()
            selenium.get(BASEURLSIGN)

            acceptButton=selenium.find_element_by_id('details-button')
            acceptButton.click()
            time.sleep(2)
                
            goButton=selenium.find_element_by_id('proceed-link')
            goButton.click()
            time.sleep(2)
        
            userEmail = selenium.find_element_by_name('email')
            userPass = selenium.find_element_by_name('password')

            userEmail.send_keys('')
            userPass.send_keys('',Keys.ENTER)

            time.sleep(5)

            assert 'account/signup' in selenium.current_url    


        def test_e_Login(self):
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

                userEmail.send_keys('l@gmail.com')
                userPass.send_keys('galaroza',Keys.ENTER)

                time.sleep(5)

                assert ('l@gmail.com' in selenium.page_source) and (PROFILE_WEB in selenium.current_url)

    
        def test_f_LoginWithWrongPassword(self):
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

                userEmail.send_keys('l@gmail.com')
                userPass.send_keys('contraseñaErronea',Keys.ENTER)

                time.sleep(5)

                assert ('Usuario o contraseña incorrecta' in selenium.page_source)and (BASEURL in selenium.current_url)


        def test_g_LoginWithNoFields(self):
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

        def test_h_validation_email(self):
            selenium = webdriver.Chrome()
            selenium.get(BASEURLSIGN)

            acceptButton=selenium.find_element_by_id('details-button')
            acceptButton.click()
            time.sleep(2)
                
            goButton=selenium.find_element_by_id('proceed-link')
            goButton.click()
            time.sleep(2)
        
            userUser = selenium.find_element_by_name('username')
            userEmail = selenium.find_element_by_name('email')
            userPass = selenium.find_element_by_name('password')

            userUser.send_keys('l')
            userEmail.send_keys('l.com')
            userPass.send_keys('galaroza',Keys.ENTER)

            time.sleep(5)

            assert 'account/signup' in selenium.current_url

        def test_i_validation_password(self):
            selenium = webdriver.Chrome()
            selenium.get(BASEURLSIGN)

            acceptButton=selenium.find_element_by_id('details-button')
            acceptButton.click()
            time.sleep(2)
                
            goButton=selenium.find_element_by_id('proceed-link')
            goButton.click()
            time.sleep(2)
        
            userUser = selenium.find_element_by_name('username')
            userEmail = selenium.find_element_by_name('email')
            userPass = selenium.find_element_by_name('password')

            userUser.send_keys('l')
            userEmail.send_keys('l@gmail.com')
            userPass.send_keys('g',Keys.ENTER)

            time.sleep(10)

            assert 'account/signup' in selenium.current_url

    
class LoginRSTestSelenium(LiveServerTestCase):             
  
     
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
    
class LoginGoogleOAuthTestSelenium(LiveServerTestCase): 

    def testAccederGoogle(self):
        selenium = webdriver.Chrome()
        selenium.get(BASEURL)
            
        acceptButton=selenium.find_element_by_id('details-button')
        acceptButton.click()
        time.sleep(2)
            
        goButton=selenium.find_element_by_id('proceed-link')
        goButton.click()
        time.sleep(2)

        googleButton = selenium.find_element_by_name('googleButton')
        googleButton.click()
        time.sleep(2) 

        username = selenium.find_element_by_id('identifierId')
        username.send_keys(USER_GOOGLE,Keys.ENTER)
        time.sleep(2) 

        userPass = selenium.find_element_by_name('password')
        userPass.send_keys(PASSWORD_GOOGLE,Keys.ENTER)
        time.sleep(2) 

        assert PROFILE_WEB in selenium.current_url #Cambiar URL

    def testAccederGoogleWrongEmail(self):
        selenium = webdriver.Chrome()
        selenium.get(BASEURL)
            
        acceptButton=selenium.find_element_by_id('details-button')
        acceptButton.click()
        time.sleep(2)
            
        goButton=selenium.find_element_by_id('proceed-link')
        goButton.click()
        time.sleep(2)

        googleButton = selenium.find_element_by_name('googleButton')
        googleButton.click()
        time.sleep(2) 

        username = selenium.find_element_by_id('identifierId')
        username.send_keys('error',Keys.ENTER)
        time.sleep(2) 

        assert 'No se ha podido encontrar tu cuenta de Google' in selenium.page_source

    def testAccederGoogleWrongPass(self):
        selenium = webdriver.Chrome()
        selenium.get(BASEURL)
            
        acceptButton=selenium.find_element_by_id('details-button')
        acceptButton.click()
        time.sleep(2)
            
        goButton=selenium.find_element_by_id('proceed-link')
        goButton.click()
        time.sleep(2)

        googleButton = selenium.find_element_by_name('googleButton')
        googleButton.click()
        time.sleep(2) 

        username = selenium.find_element_by_id('identifierId')
        username.send_keys(USER_GOOGLE,Keys.ENTER)
        time.sleep(2) 

        userPass = selenium.find_element_by_name('password')
        userPass.send_keys('error',Keys.ENTER)
        time.sleep(2) 

        assert 'Contraseña incorrecta. Vuelve a intentarlo o selecciona "¿Has olvidado tu contraseña?" para cambiarla.' in selenium.page_source


class UpdateTestSelenium(LiveServerTestCase):

    def test_a_signup(self):
        selenium = webdriver.Chrome()
        selenium.get(BASEURLSIGN)

        acceptButton=selenium.find_element_by_id('details-button')
        acceptButton.click()
        time.sleep(2)
                
        goButton=selenium.find_element_by_id('proceed-link')
        goButton.click()
        time.sleep(2)

        userUser = selenium.find_element_by_name('username')
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userUser.send_keys('dani')
        userEmail.send_keys('danirc2001@gmail.com')
        userPass.send_keys('contraseña',Keys.ENTER)

        assert 'correctamente' in selenium.page_source

    def test_b_signup(self):
        selenium = webdriver.Chrome()
        selenium.get(BASEURLSIGN)

        acceptButton=selenium.find_element_by_id('details-button')
        acceptButton.click()
        time.sleep(2)
                
        goButton=selenium.find_element_by_id('proceed-link')
        goButton.click()
        time.sleep(2)

        userUser = selenium.find_element_by_name('username')
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userUser.send_keys('dani2')
        userEmail.send_keys('danirc2000@gmail.com')
        userPass.send_keys('contraseña',Keys.ENTER)

        assert 'correctamente' in selenium.page_source

    def test_update_user(self):
        selenium = webdriver.Chrome()
        selenium.get(BASEURL)
       
        acceptButton=selenium.find_element_by_id('details-button')
        acceptButton.click()
        time.sleep(2)
            
        goButton=selenium.find_element_by_id('proceed-link')
        goButton.click()
        time.sleep(2)
        
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')
        userEmail.send_keys('danirc2001@gmail.com')
        userPass.send_keys('contraseña',Keys.ENTER)
        
        
        selenium.get(UPDATE_WEB)
        userPass = selenium.find_element_by_name('password')

        userPass.send_keys('contraseñaActualizada',Keys.ENTER)

        time.sleep(5)
        assert 'cambiados correctamente' in selenium.page_source

        
    
    def test_update_user_exist(self):
        selenium = webdriver.Chrome()
        selenium.get(BASEURL)

        acceptButton=selenium.find_element_by_id('details-button')
        acceptButton.click()
        time.sleep(2)
            
        goButton=selenium.find_element_by_id('proceed-link')
        goButton.click()
        time.sleep(2)
        
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userEmail.send_keys('danirc2001@gmail.com')
        userPass.send_keys('contraseñaActualizada',Keys.ENTER)
        
        
        selenium.get(UPDATE_WEB)
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')

        userEmail.clear()

        userEmail.send_keys('danirc2000@gmail.com')
        userPass.send_keys('contraseñaActualizada',Keys.ENTER)

        time.sleep(5)

        assert 'ya existe en la BD' in selenium.page_source


    def test_update_user_field_empty(self):
        selenium = webdriver.Chrome()
        selenium.get(BASEURL)
       
        acceptButton=selenium.find_element_by_id('details-button')
        acceptButton.click()
        time.sleep(2)
            
        goButton=selenium.find_element_by_id('proceed-link')
        goButton.click()
        time.sleep(2)
        
        userEmail = selenium.find_element_by_name('email')
        userPass = selenium.find_element_by_name('password')
        userEmail.send_keys('danirc2001@gmail.com')
        userPass.send_keys('contraseñaActualizada',Keys.ENTER)
        
        
        selenium.get(UPDATE_WEB)
        userPass = selenium.find_element_by_name('password')

        userPass.send_keys('',Keys.ENTER)

        time.sleep(5)
        assert '' in selenium.page_source

#Los test pertenecientes a la clase LoginSinSelenium y AccesoVotacionProfileSelenium deberan ejecutarse con http (runserver)----------------------------------

# class LoginSinSelenium(LiveServerTestCase,BaseTestCase):

#     def test_a_signup(self):
#             selenium = webdriver.Chrome()
#             selenium.get(BASEURLSIGN_NOSSL)

#             userUser = selenium.find_element_by_name('username')
#             userEmail = selenium.find_element_by_name('email')
#             userPass = selenium.find_element_by_name('password')

#             userUser.send_keys('pablo')
#             userEmail.send_keys('pablo@gmail.com')
#             userPass.send_keys('galaroza',Keys.ENTER)

#             time.sleep(5)

#             assert 'correctamente' in selenium.page_source

    
#     def test_b_login(self):
#             URL = BASEURLSINSSL

#             client = requests.session()

#             client.get(URL)  
#             if 'csrftoken' in client.cookies:
#                 csrftoken = client.cookies['csrftoken']
#             else:
#                 csrftoken = client.cookies['csrf']

#             login_data = dict(email='pablo@gmail.com', password='galaroza', csrfmiddlewaretoken=csrftoken, next='/')
#             r = client.post(URL, data=login_data, headers=dict(Referer=URL))
#             self.assertEqual(r.status_code, 200)

# class AccesoVotacionProfileSelenium(LiveServerTestCase):

#     def test_a_signup(self):
#             selenium = webdriver.Chrome()
#             selenium.get(BASEURLSIGN_NOSSL)

#             userUser = selenium.find_element_by_name('username')
#             userEmail = selenium.find_element_by_name('email')
#             userPass = selenium.find_element_by_name('password')

#             userUser.send_keys('prueba')
#             userEmail.send_keys('prueba@gmail.com')
#             userPass.send_keys('galaroza',Keys.ENTER)

#             time.sleep(5)

#             assert 'correctamente' in selenium.page_source
#     #Para hacer uso de este test debe crear una votación, censar un usuario
#     #en ella y colocar sus credenciales
#     # def test_acceso_votacion(self):
#     #     selenium = webdriver.Chrome()
#     #     selenium.get(BASEURLSINSSL)

#     #     userEmail = selenium.find_element_by_name('email')
#     #     userPass = selenium.find_element_by_name('password')

#     #     userEmail.send_keys('l@gmail.com')
#     #     userPass.send_keys('galaroza',Keys.ENTER)

#     #     time.sleep(5)

#     #     acceptButton=selenium.find_element_by_name('acceder')
#     #     acceptButton.click()
#     #     time.sleep(2)

#     #     assert 'Username' in selenium.page_source
        

#     def test_user_without_voting(self):
#         selenium = webdriver.Chrome()
#         selenium.get(BASEURLSINSSL)
    
#         userEmail = selenium.find_element_by_name('email')
#         userPass = selenium.find_element_by_name('password')

#         userEmail.send_keys('prueba@gmail.com')
#         userPass.send_keys('galaroza',Keys.ENTER)

# --------------------------------------------------------------------------------------------------------------------------------------------