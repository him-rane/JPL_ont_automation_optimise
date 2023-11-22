from selenium import webdriver

import locators
from Utils import Utils
from selenium.webdriver.common.keys import Keys
import time
from login import login

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

    def get_driver():
        logger.debug("Initializing Chrome WebDriver")
        try:
            # Ensure the chromedriver is up-to-date
            options = webdriver.ChromeOptions()
            options.add_argument('ignore-certificate-errors')
            options.add_argument("--start-maximized")

            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(15)
            return driver
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            logger.exception(e)
            return e


# Initialize the WebDriver (assuming Chrome in this example)
driver=Setup.get_driver()
driver.get("http://192.168.29.1")
time.sleep(10)

driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])

driver.get("https://10.64.218.26/cpeadmin/Default.aspx")
time.sleep(10)
time.sleep(10)








# # Open the first website in the first tab
# driver.get('http://192.168.29.1')
# login=login(driver)
# login.webgui_login()
# login.acs_login()
#
# driver.execute_script("window.open('');")
# driver.switch_to.window(driver.window_handles[1])
#
# # Open the second website in the new tab
# driver.get('http://192.168.29.1')
# login.webgui_login()
# utils.search_gui("wan")
# # Perform operations on the second tab
# # For example, print the title of the second tab
# print(driver.title)
#
# # Switch back to the first tab
# driver.switch_to.window(driver.window_handles[0])
# print(utils.get_serial_number())
# time.sleep(10)
#
# # Perform operations on the first tab
# # For example, print the title of the first tab
# print(driver.title)
# driver.switch_to.window(driver.window_handles[1])
# utils.find_element(*locators.SecurityMenu).click()
# utils.find_element(*locators.SecurityMenu_FirewallSubMenu).click()
#
# # Close the browser
# driver.quit()

