from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base.tests import BaseTestCase


class AdminTestCase(StaticLiveServerTestCase):

   
    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()            
    
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()
        

    def test_simpleCorrectLogin(self):                    
        self.driver.get(f'{self.live_server_url}/account/login')
        self.driver.find_element_by_id('id_username').send_keys("ja@gmail.com")
        self.driver.find_element_by_id('id_password').send_keys("ja",Keys.ENTER)
        
        #print(self.driver.current_url)
        #In case of a correct loging, a element with id 'user-tools' is shown in the upper right part
        self.assertTrue(len(self.driver.find_elements_by_id('user-tools'))==1) 