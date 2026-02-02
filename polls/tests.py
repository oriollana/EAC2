from django.test import TestCase
# Create your tests here.
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User

class MySeleniumTests(StaticLiveServerTestCase):
    # carregar una BD de test
    #fixtures = ['testdb.json',]
 
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        user = User.objects.create_user("admin", "isard@isardvdi.com", "admin123")
        user.is_superuser = True
        user.is_staff = True
        user.save()
 
    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        cls.selenium.quit()
        super().tearDownClass()
 
    def test_login(self):
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
 
        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )
 
        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('admin123')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()
 
        # testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
        self.assertEqual( self.selenium.title , "Site administration | Django site admin" )

        #Accedim a questions
        self.selenium.find_element(By.XPATH,'//a[text()="Questions"]').click()
        self.selenium.find_element(By.XPATH,'//a[contains(text(), "Add question")]').click()
        #primera pregunta
        question_input = self.selenium.find_element(By.NAME,"question_text")
        question_input.send_keys('pregunta1')
        self.selenium.find_element(By.XPATH,'//a[text()="Today"]').click()
        self.selenium.find_element(By.XPATH,'//a[text()="Now"]').click()
        self.selenium.find_element(By.XPATH,'//input[@value="Save and add another"]').click()

        #segona pregunta
        question_input = self.selenium.find_element(By.NAME,"question_text")
        question_input.send_keys('pregunta2')
        self.selenium.find_element(By.XPATH,'//a[text()="Today"]').click()
        self.selenium.find_element(By.XPATH,'//a[text()="Now"]').click()
        self.selenium.find_element(By.XPATH,'//input[@value="Save"]').click()

        #Accedim a choices
        self.selenium.find_element(By.XPATH,'//a[text()="Choices"]').click()
        self.selenium.find_element(By.XPATH,'//a[contains(text(), "Add choice")]').click()

        #Choices de la primera pregunta
        self.selenium.find_element(By.XPATH,'//select[@id="id_question"]//option[text()="pregunta1"]').click()
        choice_input = self.selenium.find_element(By.NAME,"choice_text")
        choice_input.send_keys('choice1')
        self.selenium.find_element(By.XPATH,'//input[@value="Save and add another"]').click()
 
        self.selenium.find_element(By.XPATH,'//select[@id="id_question"]//option[text()="pregunta1"]').click()
        choice_input = self.selenium.find_element(By.NAME,"choice_text")
        choice_input.send_keys('choice2')
        self.selenium.find_element(By.XPATH,'//input[@value="Save and add another"]').click()

        #Choices de la segona pregunta
        self.selenium.find_element(By.XPATH,'//select[@id="id_question"]//option[text()="pregunta2"]').click()
        choice_input = self.selenium.find_element(By.NAME,"choice_text")
        choice_input.send_keys('choice3')
        self.selenium.find_element(By.XPATH,'//input[@value="Save and add another"]').click()
 
        self.selenium.find_element(By.XPATH,'//select[@id="id_question"]//option[text()="pregunta2"]').click()
        choice_input = self.selenium.find_element(By.NAME,"choice_text")
        choice_input.send_keys('choice4')
        self.selenium.find_element(By.XPATH,'//input[@value="Save"]').click()

        #Verificació
        self.selenium.find_element(By.XPATH,'//a[text()="Choices"]').click()
        choices = ["choice1","choice2","choice3","choice4"]
        text_web = self.selenium.find_element(By.TAG_NAME, "body").text
        self.assertTrue(all(p in text_web for p in choices))
