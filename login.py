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

    def webgui_login(self, username=Inputs.username, password=Inputs.password):
        self.driver.implicitly_wait(15)
        if not self.is_webgui_logged_in():
            logger.debug("Attempting to log in via WEBGUI")
            try:
                try:
                    self.driver.find_element(By.XPATH,"//div[@class='loginForm']")
                except:
                    logger.error("IPv4 not found: Renewing the interface")
                    os.popen("ipconfig /renew")
                    time.sleep(30)
                try:
                    # Enter username and password
                    self.driver.find_element(By.ID, 'tf1_userName').send_keys(username)
                    self.driver.find_element(By.ID, 'tf1_password').send_keys(password)
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
                            logger.info("Login Successful")
                    except:
                        check_error = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/p').text
                        if 'invalid' in check_error.lower():
                            self.driver.find_element(By.ID, 'tf1_userName').send_keys(Inputs.username)
                            self.driver.find_element(By.ID, 'tf1_password').send_keys('PR@shant2301')
                            self.driver.find_element(By.NAME, 'button.login.users.dashboard').click()
                except Exception as e:
                    logger.error(e)


            except Exception as e:
                logger.error("Error occurred while attempting to log in via WEBGUI: %s", str(e))

            finally:
                try:
                    self.driver.find_element(By.XPATH, '//*[@id="tf1_forcedLoginContent"]/div/a').click()
                except Exception as e:
                    logger.warning("Error occurred while closing the login popup")


            time.sleep(5)
            return False

    def acs_login(self):


        # Open the second website in the new tab
        # driver.get('http://192.168.29.1')
        # login.webgui_login()
        # utils.search_gui("wan")
        # options = webdriver.ChromeOptions()
        # options.add_argument('ignore-certificate-errors')
        # # options.add_argument("--start-maximized")
        # driver = webdriver.Chrome(chrome_options=options)

        self.driver.get(Inputs.acs_url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.driver.find_element(by=By.ID, value="txtName").send_keys(Inputs.acs_user)
        self.driver.find_element(by=By.ID, value="txtPassword").send_keys(Inputs.acs_pwd)
        if self.driver.find_element(by=By.ID, value="btnLogin_btn"):
            self.driver.find_element(by=By.ID, value="btnLogin_btn").click()
        print("Logged into ACS successfully")
        print("searching for ONT serial number : " + Inputs.serial_number)
        time.sleep(10)
        self.driver.find_element(by=By.XPATH, value='//*[@id="lmi1"]').click()
        try:
            self.driver.find_element(by=By.XPATH, value='//*[@id="lmi1"]').click()
        except:
            print('element not found')
        self.driver.switch_to.frame("frmDesktop")
        time.sleep(3)
        self.driver.find_element(By.ID, 'tbDeviceID').send_keys(Inputs.serial_number)
        self.driver.find_element(By.ID, 'btnSearch_btn').click()
        try:
            self.driver.find_element(By.ID, 'btnSearch_btn').click()
        except:
            print("element not found")
        time.sleep(10)
        return self.driver