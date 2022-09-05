import pandas as pd 
from utils.settings import * 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from bs4 import BeautifulSoup
from time import sleep 

class OpenSea:
    BASE_URL = "https://opensea.io/rankings"

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
            print("OpenSea: Error creating Chrome instance - {}".format(e))

    def quit_browser(self):
        try:
            self.browser.quit()
        except Exception as e:
            print("OpenSea: Error quitting browser".format(e))
        
    def get_info(self):
        CATALOGUE = {
            "collections" : "styles__StyledLink-sc-l6elh8-0 ekTmzq Blockreact__Block-sc-1xf18x6-0 Flexreact__Flex-sc-1twd32i-0 Itemreact__ItemBase-sc-1idymv7-0 styles__FullRowContainer-sc-12irlp3-0 Gweql jYqxGr dCVDRE lcvzZN fresnel-greaterThanOrEqual-xl",
            "name" : "Overflowreact__OverflowContainer-sc-10mm0lu-0 gjwKJf Ranking--collection-name-overflow", 
            "change24h" : "Blockreact__Block-sc-1xf18x6-0 Flexreact__Flex-sc-1twd32i-0 kDdlpz jYqxGr",
            "change7d" : "Blockreact__Block-sc-1xf18x6-0 Flexreact__Flex-sc-1twd32i-0 dBFmez jYqxGr",
            "volume_and_floor_price" : "Blockreact__Block-sc-1xf18x6-0 Flexreact__Flex-sc-1twd32i-0 gctoET jYqxGr",
            "owners_and_items" : "Blockreact__Block-sc-1xf18x6-0 Textreact__Text-sc-1w94ul3-0 styles__StatText-sc-12irlp3-3 cfzgBZ heRNcW",
            "button" : "Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 fTomoL hJoTEY"
        }
        collections_dict = dict()

        self.browser.get(self.BASE_URL)
        
        DOC_HEIGHT = self.browser.execute_script("return document.body.scrollHeight")
        SCROLL_INC = 300
        END = 0
        
        while len(collections_dict) < 200:
            try:
                self.browser.execute_script("window.scrollTo(0, {});".format(END))
                sleep(2.5)
                html = self.browser.page_source
                soup = BeautifulSoup(html, features="html.parser")
                sleep(2.5)
                collections = list(soup.find_all('a', class_ = CATALOGUE["collections"]))

                for collection in collections:
                    property = dict()
                    try:
                        # name       = div "Blockreact__Block-sc-1xf18x6-0 FeatureTablereact__FeatureTableCell-sc-128zm2t-0 kTMXQF Ranking--collection-info Ranking--collection-info" -> div "Blockreact__Block-sc-1xf18x6-0 cIYIHz" -> span "Blockreact__Block-sc-1xf18x6-0 Textreact__Text-sc-1w94ul3-0 kORiTM hLiYFE" -> div "Overflowreact__OverflowContainer-sc-10mm0lu-0 gjwKJf Ranking--collection-name-overflow"
                        property["Name"] = collection.find('div', class_ = CATALOGUE["name"]).get_text()

                        # change24h  = div "Blockreact__Block-sc-1xf18x6-0 FeatureTablereact__FeatureTableCell-sc-128zm2t-0 fKDNjL" -> div "Blockreact__Block-sc-1xf18x6-0 Flexreact__Flex-sc-1twd32i-0 kDdlpz jYqxGr" -> span "Blockreact__Block-sc-1xf18x6-0 Textreact__Text-sc-1w94ul3-0 styles__StatText-sc-12irlp3-3 hvnhhf PZsOM" -> div "Overflowreact__OverflowContainer-sc-10mm0lu-0 gjwKJf"
                        property["Change24h"] = collection.find('div', class_ = CATALOGUE["change24h"]).get_text()

                        # change7d   = div "Blockreact__Block-sc-1xf18x6-0 FeatureTablereact__FeatureTableCell-sc-128zm2t-0 fKDNjL" -> div "Blockreact__Block-sc-1xf18x6-0 Flexreact__Flex-sc-1twd32i-0 dBFmez jYqxGr" -> span "Blockreact__Block-sc-1xf18x6-0 Textreact__Text-sc-1w94ul3-0 styles__StatText-sc-12irlp3-3 fYGUmW bepxLZ" -> div "Overflowreact__OverflowContainer-sc-10mm0lu-0 gjwKJf"
                        property["Change7d"] = collection.find('div', class_ = CATALOGUE["change7d"]).get_text()

                        # volume     = div "Blockreact__Block-sc-1xf18x6-0 FeatureTablereact__FeatureTableCell-sc-128zm2t-0 fKDNjL" -> div "Blockreact__Block-sc-1xf18x6-0 Flexreact__Flex-sc-1twd32i-0 gctoET jYqxGr" -> span "Blockreact__Block-sc-1xf18x6-0 Textreact__Text-sc-1w94ul3-0 styles__StatText-sc-12irlp3-3 cfzgBZ heRNcW" -> div "Overflowreact__OverflowContainer-sc-10mm0lu-0 gjwKJf"
                        # floorprice = div "Blockreact__Block-sc-1xf18x6-0 FeatureTablereact__FeatureTableCell-sc-128zm2t-0 fKDNjL" -> div "Blockreact__Block-sc-1xf18x6-0 Flexreact__Flex-sc-1twd32i-0 gctoET jYqxGr" -> span "Blockreact__Block-sc-1xf18x6-0 Textreact__Text-sc-1w94ul3-0 styles__StatText-sc-12irlp3-3 cfzgBZ heRNcW" -> div "Overflowreact__OverflowContainer-sc-10mm0lu-0 gjwKJf"
                        first_container = list(collection.find_all('div', class_ = CATALOGUE["volume_and_floor_price"]))
                        property["Volume"] = first_container[0].get_text()
                        property["Floor Price"] = first_container[1].get_text()

                        # owners     = div "Blockreact__Block-sc-1xf18x6-0 FeatureTablereact__FeatureTableCell-sc-128zm2t-0 fKDNjL" -> p    "Blockreact__Block-sc-1xf18x6-0 Textreact__Text-sc-1w94ul3-0 styles__StatText-sc-12irlp3-3 cfzgBZ heRNcW"
                        # item       = div "Blockreact__Block-sc-1xf18x6-0 FeatureTablereact__FeatureTableCell-sc-128zm2t-0 fKDNjL" -> p    "Blockreact__Block-sc-1xf18x6-0 Textreact__Text-sc-1w94ul3-0 styles__StatText-sc-12irlp3-3 cfzgBZ heRNcW"
                        second_container = list(collection.find_all('p', class_ = CATALOGUE["owners_and_items"]))
                        property["Owners"] = second_container[-2].get_text()
                        property["Items"] = second_container[-1].get_text()

                    except Exception: 
                        sleep(2.5)
                    
                    else: 
                        print("===== NO ERROR WITH {}".format(property["Name"]))

                    finally: 
                        if property["Name"] not in collections_dict:
                            collections_dict[property["Name"]] = property

            except StaleElementReferenceException:
                sleep(2.5)
            
            else:
                print("***** SCROLLING AT {}. Dictionary Size: {}".format(END, len(collections_dict)))

            finally:
                END += SCROLL_INC

                if END >= DOC_HEIGHT and len(collections_dict) >= 100 and len(collections_dict) < 200:
                    self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    sleep(3)
                    button = self.browser.find_element_by_xpath("//button[@class='{}']".format(CATALOGUE["button"]))
                    button.click()
                    END = 0
                    sleep(5)
        
        df = pd.DataFrame(collections_dict.values(), columns = ["Name", "Volume", "Change24h", "Change7d", "Floor Price", "Owners", "Items"])
        df = df.sort_values(by = ["Name"])
        df.to_csv("opensea.csv", encoding='utf-8', index=False)