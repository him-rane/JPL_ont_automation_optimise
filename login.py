import os
import time
from selenium.webdriver.common.by import By
from logger_util import logger
import Inputs

class login:
    def __init__(self, driver):
        self.driver = driver

    def is_webgui_logged_in(self):
        logger.debug("Checking login status")
        try:
            self.driver.find_element(By.XPATH, "//div[@class='nav-side-menu']")
            logger.debug("Logged in to the web GUI: True")
            return True
        except:
            logger.debug("Not logged in to the web GUI: False")
            return False

    def webgui_login(self, username='admin', password='P@ssw0rd'):
        self.driver.implicitly_wait(15)
        if not self.is_webgui_logged_in():
            try:
                logger.debug("Attempting to log in via WEBGUI")

                # Attempt to renew the IPv4 interface if not available
                try:
                    self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/form/div")
                except:
                    logger.error("IPv4 not found: Renewing the interface")
                    os.popen("ipconfig /renew")
                    time.sleep(30)

                # Enter username and password
                self.driver.find_element(By.ID, 'tf1_userName').send_keys(Inputs.username)
                self.driver.find_element(By.ID, 'tf1_password').send_keys(Inputs.password)
                self.driver.find_element(By.NAME, 'button.login.users.dashboard').click()

                # Handle invalid login attempts
                try:
                    check_error = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/p').text
                    if 'invalid' in check_error.lower():
                        self.driver.find_element(By.ID, 'tf1_userName').send_keys(Inputs.username)
                        self.driver.find_element(By.ID, 'tf1_password').send_keys(Inputs.default_password)
                        self.driver.find_element(By.NAME, 'button.login.users.dashboard').click()
                        self.driver.find_element(By.XPATH, '//*[@id="tf1_adminPassword"]').send_keys(
                            Inputs.password)
                        self.driver.find_element(By.XPATH, '//*[@id="tf1_cnfAdminPassword"]').send_keys(
                            Inputs.password)
                        self.driver.find_element(By.XPATH, '//*[@id="tf1_guestPassword"]').send_keys(
                            Inputs.password)
                        self.driver.find_element(By.XPATH, '//*[@id="tf1_cnfGuestPassword"]').send_keys(
                            Inputs.password)
                        self.driver.find_element(By.XPATH, '//*[@id="tf1_frmchangePassword"]/div[9]/input[1]').click()
                        self.driver.find_element(By.ID, 'tf1_userName').send_keys(Inputs.username)
                        self.driver.find_element(By.ID, 'tf1_password').send_keys(Inputs.password)
                        self.driver.find_element(By.NAME, 'button.login.users.dashboard').click()
                except:
                    check_error = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/p').text
                    if 'invalid' in check_error.lower():
                        self.driver.find_element(By.ID, 'tf1_userName').send_keys(Inputs.username)
                        self.driver.find_element(By.ID, 'tf1_password').send_keys('PR@shant2301')
                        self.driver.find_element(By.NAME, 'button.login.users.dashboard').click()

            except Exception as e:
                logger.error("Error occurred while attempting to log in via WEBGUI: %s", str(e))

            finally:
                try:
                    self.driver.find_element(By.XPATH, '//*[@id="tf1_forcedLoginContent"]/div/a').click()
                except Exception as e:
                    logger.error("Error occurred while closing the login popup: %s", str(e))

            time.sleep(5)
            return False
