import os
import time

from selenium import webdriver
from webdriver_auto_update.webdriver_auto_update import WebdriverAutoUpdate
from logger_util import logger

# Path to store chromedriver
driver_directory = "C:\\Users\\ontvi\\AppData\\Local\\Programs\\Python\\Python310\\Scripts"
chromedriver_path = os.path.join(driver_directory, "chromedriver.exe")

class Setup:
    def update_driver(self):
        logger.info("Updating Chromedriver")
        driver_manager = WebdriverAutoUpdate(driver_directory)
        driver_manager.main()

    def get_driver(self):
        logger.debug("Initializing Chrome WebDriver")
        try:
            # Ensure the chromedriver is up-to-date
            options = webdriver.ChromeOptions()
            options.add_argument('ignore-certificate-errors')
            options.add_argument("--start-maximized")

            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(15)
            driver.get("http://192.168.29.1")
            return driver
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            logger.exception(e)
            return e