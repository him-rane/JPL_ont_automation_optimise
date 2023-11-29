import datetime
import logging
import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import  subprocess

from selenium.common.exceptions import NoSuchElementException

import time
import os

import locators
from logger_util import logger
from login import login

class Utils:

    def __init__(self, driver_):
        self.driver = driver_

    # RUN COMMANDS
    @staticmethod
    def cmd_line(cmd):
        return str(os.popen(cmd).read().split("/n")[0])


    def find_element(self, xpath_='',css_selector_='', id_=''):
        locators = [
            (By.XPATH, xpath_),
            (By.CSS_SELECTOR, css_selector_),
            (By.ID, id_)
        ]
        time.sleep(1)
        # try:
        #     self.driver.find_element(By.XPATH, "//div[@class='nav-side-menu']")
        # except:
        #     logger.error("Login status : FALSE")
        #     logger.warning("Try To Login Again")
        #     obj=login(self.driver)
        #     obj.webgui_login()

        for locator_type, locator_value in locators:
            try:
                element = self.driver.find_element(locator_type, locator_value)
                locator_used = f"{locator_type}='{locator_value}'"
                logger.debug(f"Element found using locator: {locator_used}")
                return element
            except NoSuchElementException as e:
                logger.error(f"Element not found using locator: {locator_type}='{locator_value}': {e}")
            except Exception as e:
                logger.error(
                    f"An error occurred while locating the element using locator: {locator_type}='{locator_value}': {e}")

        logger.warning(
            f"Element not found using any of the provided locators: {', '.join([f'{loc[0]}={loc[1]}' for loc in locators])}")
        return None



    #SEARC IN WEBGUI
    def search_gui(self, value):
        try:
            logger.debug(f"Searching for the keyword: '{value}'")

            # Find the search bar element and interact with it
            search_bar = self.find_element("//input[@id='menu1']")
            search_bar.click()
            search_bar.send_keys(value)
            search_bar.send_keys(Keys.ENTER)

            # Find search results
            search_results = self.driver.find_elements(By.XPATH, "//ul[@id='menuList']/li/a")

            # Click on the first result matching the keyword
            for result in search_results:
                if value.lower() in result.text.lower():
                    result.click()
                    time.sleep(3)
                    logger.debug(f"Found and clicked on the result containing '{value}'")
                    break
            else:
                logger.warning(f"No search result found for keyword: '{value}'")
        except Exception as e:
            logger.error(f"Error occurred while searching for the keyword: '{value}': {str(e)}")

    #CHECK FERWARE VERSION
    def get_firmware_version(self):
        logger.debug("Retrieving Firmware Version...")
        try:
            if self.find_element('//*[@id="breadCrumb"]').text != "Dashboard":
                self.find_element('//*[@id="mainMenu1"]').click()

            firmware_version=self.find_element(*locators.firmware_version_sidebar).text
            logger.info("Firmware Version "+firmware_version)
            return firmware_version
        except Exception as e:
            logger.error(f"Error occurred while retrieving Firmware Version: {str(e)}")
            return "-1"


    #LOGOUT USING WEBGUI
    def logout_gui(self):
        logger.debug("Trying logout from WEBGUI")
        try:
            self.find_element(*locators.DashboardMenu_Logout_Dropdown).click()
            self.find_element(*locators.DashboardMenu_Logout_Dropdown_Logout).click()
            self.find_element(*locators.DashboardMenu_Logout_Dropdown_Logout_OK).click()
        except Exception as e:

            logger.error(e)

    #CHECK FOR LOGIN IN WEBGUI
    def isLogin_webgui(self):
        logger.info("Checking for login status")
        try:
            self.driver.find_element(By.XPATH,"//div[@class='nav-side-menu']")
            logger.info("Logged in webgui")
            return True
        except:
            try:
                self.driver.find_element(By.XPATH,"//div[@class='content-topBlock']")
                logger.info("Logged in webgui")
                return True
            except:
                logger.warning("Not Logged in webgui")
                return False


    #CHECK GPON STATUS 01-05
    def get_GPON_state(self):
        try:
            logger.debug("Checking GPON status")

            self.search_gui("WAN Information")

            # Find and retrieve the GPON status
            GPON_state = self.find_element(*locators.gpon_status_WAN_Information).text
            logger.info(f"GPON Status: {GPON_state}")

            return GPON_state
        except Exception as e:
            logger.error("Error occurred while checking GPON status: %s", str(e))
            return -1

    #CHECK IPV4 FROM WEBGUI
    def get_ipv4(self):
        logger.debug("Checking WAN IPv4 Address")
        try:
            if self.find_element('//*[@id="breadCrumb"]',"#breadCrumb",'breadCrumb').text=="Dashboard":
                ipv4=self.find_element(*locators.ipv4_address_daseboard).text
                logger.info("WAN IPv4 Address : " + ipv4)
                return ipv4
            else :
                self.find_element('//*[@id="mainMenu1"]').click()
                return self.get_ipv4()
        except Exception as e:
            logger.error("Error occurred while retrieving WAN IPv4 Address: %s", str(e))
            return ""

    #CHECK IPV6 FROM WEGUI
    def get_ipv6(self):
        logger.debug("Checking WAN IPv6 Address")
        try:
            if self.find_element('//*[@id="breadCrumb"]').text == "Dashboard":
                ipv6 = self.find_element(*locators.Dashboard_WAN_IPv6_1).text
                if 'fe80' in ipv6:
                    ipv6 = self.find_element(*locators.Dashboard_WAN_IPv6_2).text
                logger.info("WAN IPv6 Address : " + ipv6)
                return ipv6.split('/')[0]
            else:
                self.find_element('//*[@id="mainMenu1"]').click()
                return self.get_ipv6()

        except Exception as e:
            logger.critical("Error occurred while fetching IPv6 Address: %s", str(e))
            return -1

    def get_wan_port(self):
        try:
            logger.debug("Getting WAN Port Configuration")

            # Search for WAN Port Configuration
            self.search_gui('WAN Port Configuration')

            # Find and retrieve the WAN port value
            wan_port_element = self.find_element("//input[@id='tf1_vlanId']")
            wan_port = wan_port_element.get_attribute("value")

            if wan_port:
                logger.info("WAN Port Configuration found: %s", wan_port)
                return wan_port
            else:
                logger.warning("WAN Port Configuration not found or empty")
                return None

        except Exception as e:
            logger.error("Error occurred while retrieving WAN Port Configuration: %s", str(e))
            return None
    #accept the alert
    def accept_alert(self):
        try:
            time.sleep(3)
            self.driver.switch_to.alert.accept()
            logger.debug("Alert Accepted")
            time.sleep(5)
        except:
            pass
    def get_serial_number(self):
        try:
            logger.debug("Getting Serial Number ")
            serial_number = self.find_element("/html/body/div[1]/div[1]/div[2]/p[2]/span").text

            if serial_number:
                logger.info(f"Serial Number found: {serial_number}")
                return serial_number
            else:
                logger.warning("Serial Number not found")
                return None
        except Exception as e:
            logger.error(f"Error occurred while retrieving Serial Number: {str(e)}")
            return None

    def get_dbglog(self):
        logger.error('Taking DBG log after an issue')
        self.driver.get('http://192.168.29.1/dbglog.cgi')
        logger.debug('dbglog taken at: {}'.format(datetime.datetime.now()))
        time.sleep(45)

    def website_check(self):
        logger.debug('Checking Internet Connectivity')
        from selenium import webdriver
        tempDriver = webdriver.Chrome()

        success_count = 0

        urls = ['https://www.youtube.com/watch?v=VVsC2fD1BjA',
                'http://www.softwareqatest.com/qatweb1.html',
                'https://www.facebook.com']

        for url in urls:
            try:
                tempDriver.execute_script("window.open('');")
                tempDriver.switch_to.window(tempDriver.window_handles[-1])
                tempDriver.get(url)
                title = tempDriver.title

                if title != '':
                    success_count += 1
                if "youtube.com" in url:
                    body_element = tempDriver.find_element(By.XPATH,"//body")
                    body_element.send_keys(Keys.SPACE)
                time.sleep(10)
            except Exception as e:
                logger.error(f"An error occurred while checking website: {str(e)}")

        time.sleep(5)
        if success_count > 0:
            logger.info('Internet access is successful for at least one website')
            return True
        else:
            logger.error('Unable to access the Internet')
            return False


    def ping_ipv4_from_lan_client(self):
        logger.debug('Checking IPv4 Connectivity with Ping')
        command = 'cmd /c ping google.com -4 -n 10'
        ipv4 = 0

        try:
            cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            out = cmd.communicate()
            output = str(out[0])

            if 'time' and 'TTL' in output:
                logger.info('IPv4 Ping is successful')
                return True
            else:
                ping_fail_check_1 = 'could not find host'
                ping_fail_check_2 = 'Request timed out'
                if ('time' not in output) and (ping_fail_check_1 in output or ping_fail_check_2 in output):
                    logger.error('Ping IPv4 Failed')
                    return False

        except Exception as e:
            logger.error(f'Error: {str(e)}')
            return False

    def ping_ipv6_from_lan_client(self):
        logger.debug('Checking IPv6 Connectivity with Ping')
        command = 'cmd /c ping google.com -6 -n 10'

        try:
            cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            out = cmd.communicate()
            output = str(out[0])

            if 'time' in output and 'ms' in output:
                logger.info('IPv6 Ping is successful')
                return True
            else:
                ping_fail_check_1 = 'unreachable'
                ping_fail_check_2 = 'Request timed out'
                ping_fail_check_3 = 'could not find'
                if ('time' not in output) and (ping_fail_check_1 in output or ping_fail_check_2 in output or ping_fail_check_3 in output):
                    logger.error('Ping IPv6 Failed')
                    return False

        except Exception as e:
            logger.error(f'Error: {str(e)}')
            return False

