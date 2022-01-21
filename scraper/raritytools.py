import pandas as pd
import datetime 
from utils import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from bs4 import BeautifulSoup
from time import sleep 

class RarityTools:
    BASE_URL = "https://rarity.tools/upcoming"

    def __init__(self) -> None:
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.start_browser()

    def start_browser(self, header: bool = True):
        options = Options()
        # options.headless = header
        # options.add_extension('buster.crx') # Extention to solve captchas
        # options.add_experimental_option('excludeSwitches', ['enable-automation']) #Remove "chrome is controlled by automated testsoftware"
        # options.add_argument('window-size=1146,671') # Change window size
        options.add_argument("--incognito")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
        try:
            self.browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(), options=options)
        except Exception as e:
            print("RarityTools: Error creating Chrome instance - {}".format(e))

    def quit_browser(self):
        try:
            self.browser.quit()
        except Exception as e:
            print("RarityTools: Error quitting browser".format(e))

    def get_info(self):
        CATALOGUE = {
            "cards" : "relative flex flex-row justify-center m-auto flex-nowrap", 
            "sales" : "text-left text-gray-800",
            "first_cell" : "block pt-3 pb-6 lg:table-cell",
            "third_cell" : "block text-right lg:table-cell lg:align-center -mt-0.5 lg:mt-0",
            "fourth_cell" : "block clear-both mb-4 lg:mb-0 lg:table-cell lg:align-center"
        }
        cards_dict = dict()

        self.browser.get(self.BASE_URL)
        sleep(3)

        DOC_HEIGHT = self.browser.execute_script("return document.body.scrollHeight")
        SCROLL_INC = 300
        END = 0

        while END < DOC_HEIGHT:
            try:
                self.browser.execute_script("window.scrollTo(0, {});".format(END))
                sleep(2.5)
                html = self.browser.page_source
                soup = BeautifulSoup(html, features="html.parser")
                sleep(2.5)
                cards = list(soup.find_all('div', class_ = CATALOGUE["cards"]))
            
                for i in range(0, 2):
                    sales = list(cards[i].find_all('tr', class_ = CATALOGUE["sales"]))
                    for j in range(0, len(sales)):
                        try:
                            property = dict()

                            first_cell = list(sales[j].find('td', class_ = CATALOGUE["first_cell"]))
                            property["Name"] = first_cell[0].get_text().strip()
                            property["Description"] = first_cell[2].get_text().strip()

                            second_cell = sales[j].find_all('a')
                            property["Discord"] = second_cell[0].get('href')
                            property["Twitter Link"] = second_cell[1].get('href')
                            property["Twitter Handle"] = second_cell[1].get_text().strip()
                            property["Website"] = second_cell[2].get('href')

                            third_cell = list(sales[j].find('td', class_ = CATALOGUE["third_cell"]))
                            property["Mint Price"] = third_cell[0].get_text().strip()
                            property["Quantity"] = third_cell[2].get_text().strip()[:third_cell[2].get_text().strip().find(' ')]

                            fourth_cell = list(sales[j].find('td', class_ = CATALOGUE["fourth_cell"]))
                            property["Sale Date"] = self.date_formatter(fourth_cell, property["Name"])

                        except Exception:
                            sleep(2.5)
                        
                        else:
                            print("===== NO ERROR WITH {}".format(property["Name"]))
                        
                        finally: 
                            if property["Name"] not in cards_dict:
                                cards_dict[property["Name"]] = property

            except StaleElementReferenceException:
                sleep(2.5)
            
            else: 
                print("***** SCROLLING AT {}. Dictionary Size: {}".format(END, len(cards_dict)))
            
            finally:
                END += SCROLL_INC
        
        df = pd.DataFrame(cards_dict.values(), columns = ["Name", "Description", "Mint Price", "Quantity", "Sale Date" ,"Discord", "Twitter Link", "Twitter Handle", "Website"])
        df.to_csv("raritytools.csv", encoding='utf-8', index=False)

                
    def date_formatter(self, fourth_cell, SALE_NAME):
        content = [k.get_text().strip() for k in fourth_cell if k.get_text().strip() != '']
        if content[-1] == 'Today':
            date = datetime.datetime.now().strftime("%A, %B %dth %Y")
            Bot().send_message("SALE TODAY! {}".format(SALE_NAME))
        elif content[-1] == 'Tomorrow':
            date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%A, %B %dth %Y")
            Bot().send_message("SALE TOMORROW! {}".format(SALE_NAME))
        elif content[-1] == 'Yesterday':
            date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%A, %B %dth %Y")
        else: 
            date = content[-1]

        return date