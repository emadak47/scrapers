from utils.settings import * 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from bs4 import BeautifulSoup
from time import sleep

class GYM:
    BASE_URL = "https://fcbooking.cse.hku.hk/Form/SignUp"

    def __init__(self) -> None:
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.start_browser()

    def start_browser(self, header: bool = True):
        options = Options()
        # options.headless = header
        # options.add_extension('buster.crx') # Extention to solve captchas
        options.add_experimental_option('excludeSwitches', ['enable-automation']) #Remove "chrome is controlled by automated testsoftware"
        # options.add_argument('window-size=1146,671') # Change window size
        options.add_argument("--incognito")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
        try:
            self.browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(), options=options)
        except Exception as e:
            print("GYM: Error creating Chrome instance - {}".format(e))


    def quit_browser(self):
        try:
            self.browser.quit()
        except Exception as e:
            print("GYM: Error quitting browser".format(e))
        
    
    def get_info(self):
        self.browser.get(self.BASE_URL)

        self.send_keys()
        self.select_session()
        self.check_radio()
        self.recaptcha()
        # self.submit_bttn()


    def send_keys(self, CATALOGUE = {
        "email" : "Email",
        "name"  : "FirstName",
        "UID"   : "MemberID"
    }):
        email = self.browser.find_element_by_xpath("//input[@id='{}']".format(CATALOGUE["email"]))
        email.send_keys("u3566296@connect.hku.hk")

        name = self.browser.find_element_by_xpath("//input[@id='{}']".format(CATALOGUE["name"]))
        name.send_keys("Emad Akhras")
    
        uid = self.browser.find_element_by_xpath("//input[@id='{}']".format(CATALOGUE["UID"]))
        uid.send_keys("3035662962")
    

    def select_session(self, CATALOGUE = {
        "center" : "CenterID",
        "date"   : "DateList",
        "time"   : "SessionTime"
    }):
        centerSelect = Select(self.browser.find_element_by_xpath("//select[@id='{}']".format(CATALOGUE["center"])))
        centerSelect.select_by_value("10002")

        dateSelect = Select(self.browser.find_element_by_xpath("//select[@id='{}']".format(CATALOGUE["date"])))
        #dateSelect.select_by_value()

        timeSelect = Select(self.browser.find_element_by_xpath("//select[@id='{}']".format(CATALOGUE["time"])))
        #timeSelect.select_by_value()
    
    
    def check_radio(self):
        vaccine = self.browser.find_element_by_css_selector("input[type='radio'][value='true'][id='vacine_t']") # vaccination
        self.browser.execute_script("arguments[0].click();", vaccine)
        for item in range(1, 9):
            id = "Q{}_f".format(item)
            declaration_item = self.browser.find_element_by_css_selector("input[type='radio'][id='{}']".format(id)) #declaration items 
            self.browser.execute_script("arguments[0].click();", declaration_item)

        final_declaration = self.browser.find_element_by_css_selector("input[type='checkbox'][id='dataCollection']") #final declaration 
        self.browser.execute_script("arguments[0].click();", final_declaration)


    def recaptcha(self):
        recaptcha = self.browser.find_element_by_css_selector("div[class='g-recaptcha']")
        outer_iframe = recaptcha.find_element_by_tag_name('iframe')
        outer_iframe.click()
        # if recaptcha pops up images, 
        # https://medium.com/analytics-vidhya/how-to-bypass-recaptcha-v3-with-selenium-python-7e71c1b680fc

    
    def submit_bttn(self):
        self.browser.find_elements_by_xpath("//button[@id='{}']".format("sbmtBtn")).click()