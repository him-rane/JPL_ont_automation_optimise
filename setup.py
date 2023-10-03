from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from logger_util import logger


from selenium import webdriver
from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
options.add_argument("--start-maximized")

class Setup:
    def get_driver(self):
        logger.debug("Initializing Chrome WebDriver")

        try:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            # from selenium import webdriver

            # Correct way to initialize a WebDriver (e.g., for Chrome)
            # driver = webdriver.Chrome('C:\\Users\\ontvi\\OneDrive\\Desktop\\chromedriver-win64\\chromedriver.exe')

            # driver = webdriver.Chrome("")
            driver.implicitly_wait(15)
            driver.maximize_window()
            driver.get("http://192.168.29.1")

            return  driver
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            logger.exception(e)
            return e
