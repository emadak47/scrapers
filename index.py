from utils import * 
from scraper import scrapers

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    for key, value in scrapers.items():
        try:
            scraper = value()
        except Exception as e:
            print("****** Error starting scrapper: {} \n {}".format(key, e))
        
        try:
            scraper.get_info()
        except Exception as e:
            print("****** Error while scraping {} \n {}".format(key, e))
        finally:
            print("====== Scraper {} done ======".format(key))

        # try:
        #     scraper.quit_browser()        
        # except Exception as e:
        #     print("****** Error quitting browser: {} \n {}".format(key, e))


if __name__ == "__main__":
    main() 