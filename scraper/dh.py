from __future__ import annotations
from utils import * 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
from bs4 import BeautifulSoup

class DH(CommandBot):
    BASE_URL: str = "http://dh.stjohns.hk/accounts/login"
    CATALOGUE: dict(dict) = {
        "login" : {
           "username"       : "id_username", 
            "password"      : "id_password", 
            "submit-bttn"   : "btn btn-success", 
        }, 
        "dish"  : {
            "dish-card"     : "col-sm-4",
            "view-details"  : "btn btn-success",
        }, 
        "checkout" : {
            "quantity"      : "list-group-item list-group-item-light text-center text-dark",
            "submit-bttn"   : "btn btn-primary"
        },
        "dishes"            : "text-center", 
        "add-to-cart"       : "btn btn-success btn-md my-0 p",
        "receipt"           : "text-center"
    }
    is_ordering = False


    def __init__(self) -> None:
        CommandBot.__init__(self)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)


    def start_browser(self, header: bool = True) -> None:
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
            print("xxxxxxxx Error starting driver xxxxxxxx \n {}".format(e))


    def quit_browser(self)-> None:
        try:
            self.browser.quit()
        except Exception as e:
            print("xxxxxxxx Error quitting browser xxxxxxxx \n {}".format(e))
    

    def get_info(self):
        self.initiate_bot_handlers()


    def initiate_bot_handlers(self) -> None:
        try: 
            handlers: dict = {
                "start"  : CommandHandler("start", self.start),
                "menu"   : CommandHandler("menu", self.get_menu),
                "order"  : CommandHandler("order", self.order_food),
                "cancel" : CommandHandler("cancel", self.cancel),
                "read"   : MessageHandler(Filters.text & (~Filters.command), self.read),
                "unknown": MessageHandler(Filters.command, self.unknown)
            }

            for _, value in handlers.items():
                self.dispatcher.add_handler(value)
            
            self.updater.start_polling()

        except Exception as e:
            print("xxxxxxxx Error initiating handlers xxxxxxxx \n {}".format(e))
    

    def login(self) -> BeautifulSoup:
        try: 
            self.browser.get(self.BASE_URL)

            username = self.browser.find_element_by_xpath(
                "//input[@id='{}']".format(
                    self.CATALOGUE["login"]["username"]
                )
            )
            username.send_keys(DH_USERNAME)
            
            password = self.browser.find_element_by_xpath(
                "//input[@id='{}']".format(
                    self.CATALOGUE["login"]["password"]
                )
            )
            password.send_keys(DH_PASSWORD)

            login = self.browser.find_element_by_xpath(
                "//input[@class='{}']".format(
                    self.CATALOGUE["login"]["submit-bttn"]
                )
            ) 
            login.click()

            html = self.browser.page_source
            return BeautifulSoup(html, features="html.parser")

        except Exception as e:
            print("xxxxxxxx Error logging in xxxxxxxx \n {}".format(e))


    def get_menu(self, update: Update, context: CallbackContext): 
        self.start_browser()
        self.login_soup = self.login()
        (self.menu, msg) = self.get_menu_helper(self.login_soup)
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=msg
        )
        self.is_ordering = True


    def order_food(self, update: Update, context: CallbackContext):
        self.receipt = self.order_food_helper(self.login_soup)
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=self.receipt
        )


    def start(self, update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Ready!"
        )


    def read(self, update: Update, context: CallbackContext):
        if (self.is_ordering):
            self.item_no = int(update.message.text)


    def cancel(self, update: Update, context: CallbackContext):
        self.updater.stop()
        self.quit_browser()


    def unknown(self, update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Sorry, I didn't understand the command."
        )        
    

    def get_menu_helper(self, soup: BeautifulSoup) -> tuple[list, str]: 
        def compose_msg(menu: list) -> str:
            return "\n".join(menu)

        def formatter(number: int, string: str) -> str:
            return "{}. {} \n".format(str(number), string)

        def helper() -> list:
            dishes = soup.find_all(
                "h5", 
                class_ = "{}".format(
                    self.CATALOGUE["dishes"]
                )
            )
            menu = [
                dish.find("a", recursive=False).get_text() 
                for dish in dishes 
                if dish.find("a", recursive=False) != None
            ]
            return [
                formatter(idx, item)
                for idx, item in enumerate(menu, 1)
            ]
        
        try:
            menu = helper()
            msg = compose_msg(menu)
            return (menu, msg)

        except Exception as e:
            print("xxxxxxxx Error getting menu xxxxxxxx \n {}".format(e))
    

    def order_food_helper(self, soup: BeautifulSoup) -> BeautifulSoup:
        def confirm_quantity() -> bool:
            html = self.browser.page_source
            checkout_soup = BeautifulSoup(html, features="html.parser")
            quantity = checkout_soup.find_all(
                "li",
                class_ = "{}".format(
                    self.CATALOGUE["checkout"]["quantity"]
                )
            )[3]
        
            return int(quantity.get_text().strip()[-1]) == 1

        try:
            if (self.is_ordering and self.item_no):
                dish_card = soup.find_all(
                    "div", 
                    class_ = "{}".format(
                        self.CATALOGUE["dish"]["dish-card"]
                    )
                )[self.item_no-1]             

                view_details = dish_card.find(
                    "a", 
                    class_ = "{}".format(
                        self.CATALOGUE["dish"]["view-details"]
                    )
                )

                if (view_details != None):
                    view_details_bttn = self.browser.find_element_by_xpath(
                        "//a[@href='{}'][@class='{}']".format(
                            view_details.get("href"),
                            self.CATALOGUE["dish"]["view-details"]
                        )
                    )
                    view_details_bttn.click()

                    add_to_cart = self.browser.find_element_by_xpath(
                        "//a[@class='{}']".format(
                            self.CATALOGUE["add-to-cart"]
                        ) 
                    )
                    add_to_cart.click()

                    if (confirm_quantity()):
                        checkout = self.browser.find_element_by_xpath(
                            "//a[@class='{}']".format(
                                self.CATALOGUE["checkout"]["submit-bttn"]
                            )
                        )
                        print(checkout)
                        #checkout.click()
                    
                    self.is_ordering = False
                    return self.get_receipt()
                
                else: 
                    return "SOLD OUT!! {}".format(self.menu[self.item_no-1])
 
        except Exception as e:
            print("xxxxxxxx Error ordering food xxxxxxxx \n {}".format(e))   


    def get_receipt(self) -> str:
        return (
            self.browser.find_element_by_xpath(
                "//h1[@class='{}']".format(
                    self.CATALOGUE["receipt"]
                )
            ).get_text()
        )
