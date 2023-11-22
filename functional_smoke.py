from datetime import datetime
import os
import subprocess
from ftplib import FTP
import telnetlib
from telnetlib import EC
from selenium import webdriver

from pyotp import random
from selenium import webdriver

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import Inputs
import locators
import setup
from logger_util import logger
from device_health import device_health
from Utils import Utils
import time
from login import login
from selenium.webdriver.common.action_chains import ActionChains
from setup import Setup


class functional_smoke:
    def __init__(self, driver):

        self.driver = driver
        self.utils = Utils(driver)
        self.login = login(driver)
        self.device_health = device_health(driver)

    def reboot(self):
            # go to Administration >> Maintenance >> Reboot
        self.utils.find_element(*locators.DashboardMenu).click()
        self.utils.find_element(*locators.AdministrationMenu).click()
        self.utils.find_element(*locators.AdministrationMenu_MaintenanceSubMenu).click()
        self.utils.find_element(*locators.Maintenance_BackupReboot_RebootButton).click()

        self.utils.accept_alert()

        logger.debug('Reseting Device (Estimated Time: 200 Seconds)')
        time.sleep(200)
    def factory_reset(self):
        logger.info("Factory Reseting the Device")
        self.utils.find_element(*locators.DashboardMenu).click()
        self.utils.find_element(*locators.AdministrationMenu).click()
        self.utils.find_element(*locators.AdministrationMenu_MaintenanceSubMenu).click()
        self.utils.find_element(*locators.Maintenance_BackupReboot_DefaultButton).click()
        self.utils.accept_alert()
        logger.debug('Reseting Device (Estimated Time: 300 Seconds)')
        time.sleep(300)
    def restore(self,restore_file_location):
        logger.debug(f"Restoring the the device: {restore_file_location} ")
        self.utils.find_element(*locators.DashboardMenu).click()
        self.utils.find_element(*locators.AdministrationMenu).click()
        self.utils.find_element(*locators.AdministrationMenu_MaintenanceSubMenu).click()
        restore_path = self.utils.find_element(*locators.Maintenance_BackupReboot_FileInput)
        restore_path.send_keys(restore_file_location)
        time.sleep(5)
        self.utils.find_element(*locators.Maintenance_BackupReboot_FileInputBtn).click()
        self.utils.accept_alert()
        time.sleep(200)
        self.login.webgui_login()
    def backup(self):
        logger.info("Taking BACKUP of Device")
        self.utils.find_element(*locators.DashboardMenu).click()
        self.utils.find_element(*locators.AdministrationMenu).click()
        self.utils.find_element(*locators.AdministrationMenu_MaintenanceSubMenu).click()
        self.utils.find_element(*locators.Maintenance_BackupReboot_BackupButton).click()
        self.utils.accept_alert()


    def TC_Functional_Smoke_4(self):
        logger.debug('Validating MAC Address after Reboot and Reset')
        try:
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            wan_mac_address = self.utils.find_element(*locators.mac_address_daseboard).text
            logger.debug(f'WAN MAC Address before Reboot: {wan_mac_address}')

            # go to Administration >> Maintenance >> Reboot
            self.utils.find_element(*locators.AdministrationMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_MaintenanceSubMenu).click()
            self.utils.find_element(*locators.Maintenance_BackupReboot_RebootButton).click()

            try:
                self.driver.switch_to.alert.accept()
            except:
                pass

            logger.debug('Rebooting Device (Estimated Time: 300 Seconds)')
            time.sleep(300)

            logger.debug('Reboot Process Complete')

            self.login.webgui_login()

            wan_mac_address_after_reboot = self.utils.find_element(*locators.mac_address_daseboard).text
            logger.debug(f'WAN MAC Address after Reboot: {wan_mac_address_after_reboot}')

            success = 0
            if wan_mac_address == wan_mac_address_after_reboot:
                logger.info('WAN MAC Address after Reboot is the same')
            else:
                logger.error('WAN MAC Address has changed after Reboot')
                self.utils.get_dbglog()
                return False

            self.utils.find_element(*locators.AdministrationMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_MaintenanceSubMenu).click()
            self.utils.find_element(*locators.Maintenance_BackupReboot_DefaultButton).click()

            time.sleep(5)
            # Accept the alert for Reset
            try:
                self.driver.switch_to.alert.accept()
            except:
                pass

            logger.debug('Reseting Device (Estimated Time: 300 Seconds)')
            time.sleep(300)

            self.login.webgui_login()

            wan_mac_address_after_reset = self.utils.find_element(*locators.mac_address_daseboard).text
            logger.debug(f'WAN MAC Address after Reset: {wan_mac_address_after_reset}')

            if wan_mac_address == wan_mac_address_after_reset:
                logger.info('WAN MAC Address after Factory Reset is same')
            else:
                logger.error('WAN MAC Address has changed after Factory Reset')
                self.utils.get_dbglog()
                return False

            logger.info('TC_Functional_Smoke_002 completed successfully.')
            return True
        except Exception as e:
            logger.error("Error occurred while executing TC_Functional_Smoke_002: %s", str(e))
            return False
    def TC_Functional_Sanity_5(self):
        logger.info("DHCP: Validate Functionality of dhcp server with limit IP address pool")
        try:
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            def get_lan_client_ip():
                command = 'cmd /c ipconfig'
                cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                out = cmd.communicate()
                output = str(out[0])
                data = output.split('\\r\\n')
                lan_client_ip = ''
                for ip in data:
                    if 'IPv4 Address' in ip:
                        lan_client_ip = ip.split(':')[-1].strip()

                return lan_client_ip

            ip = get_lan_client_ip()
            last_number = ip.split('.')[-1]

            end_ip = int(last_number) - 5
            if end_ip < 15:
                end_ip = 100

            start_ip = end_ip - 10

            start_ip_address = '192.168.29.{}'.format(start_ip)
            end_ip_address = '192.168.29.{}'.format(end_ip)

            self.login.webgui_login()
            logger.debug('Configuring Limit for LAN IP')
            # go to Network Menu
            self.utils.find_element(*locators.NetworkMenu).click()
            self.utils.find_element(*locators.NetworkMenu_LanSubMenu).click()

            self.utils.find_element(*locators.LANIPv4Config_StartIP).clear()
            self.utils.find_element(*locators.LANIPv4Config_StartIP).send_keys(start_ip_address)

            self.utils.find_element(*locators.LANIPv4Config_EndIP).clear()
            self.utils.find_element(*locators.LANIPv4Config_EndIP).send_keys(end_ip_address)

            self.utils.find_element(*locators.LANIPv4Config_DomainName).clear()
            self.utils.find_element(*locators.LANIPv4Config_DomainName).send_keys('TestRange')

            self.utils.find_element(*locators.LANIPv4Config_SaveBtn).click()

            logger.debug('Releasing LAN Client Ip and Renewing IP')
            command = 'cmd /c ipconfig /renew'
            cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

            time.sleep(30)
            new_ip_address = get_lan_client_ip()
            if new_ip_address == '':
                command = 'cmd /c ipconfig /renew'
                cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                new_ip_address = get_lan_client_ip()

            new_ip = int(new_ip_address.split('.')[-1])
            if end_ip > new_ip > start_ip:
                logger.info('LAN IP Limit is successfully validated')
                return True
            else:
                logger.error('LAN Client IP is outside configured limit')
                self.utils.get_dbglog()
                return False
        except Exception as E:
            logger.error(f"Error occur while configuring limit for LAN IP : {str(E)}")
            return False
    def TC_Finctional_Smoke_9(self):
        logger.info("Validate 'Logout' button functionality in web GUI")
        try:
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            self.utils.logout_gui()
            try:
                self.utils.find_element("//div[@class='loginForm']")
                return True
            except Exception as E:
                logger.error("Unable to Logout from web GUI ")
                return False
        except Exception as E:
            logger.error("Error occurred while executing TC_Functional_Smoke_09: %s", str(E))
            return False
    def TC_Functional_Smoke_10(self):
        logger.info('Validating Date & Time functionality in HG')
        try:
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            # Search for "Date & Time Configuration"
            self.utils.search_gui("Date & Time Configuration")

            # Get the current date and time
            current_time = self.utils.find_element(*locators.DateTimeConfiguration_CurrentRouterTime).text
            logger.info(f'Current Date and Time: {current_time}')

            # Change the time zone
            self.utils.find_element(*locators.DateTimeConfiguration_TimeZone).click()
            time.sleep(5)
            self.utils.find_element('//*[@id="tf1_selTimezone"]/option[6]').click()
            time.sleep(10)
            self.utils.find_element(*locators.DateTimeConfiguration_SaveButton).click()
            time.sleep(15)

            # Get the changed date and time
            changed_time = self.utils.find_element(*locators.DateTimeConfiguration_CurrentRouterTime).text
            logger.info(f'Changed Date and Time: {changed_time}')

            # Change back to the current time zone
            logger.debug("Changing back to the current time zone")
            self.utils.find_element(*locators.DateTimeConfiguration_TimeZone).click()
            time.sleep(5)
            self.utils.find_element('//*[@id="tf1_selTimezone"]/option[23]').click()
            time.sleep(10)
            self.utils.find_element(*locators.DateTimeConfiguration_SaveButton).click()
            time.sleep(15)

            # Get the current date and time after reverting
            current_time_after_revert = self.utils.find_element(*locators.DateTimeConfiguration_CurrentRouterTime).text
            logger.info(f'Current Date and Time after reverting: {current_time_after_revert}')

            logger.info('TC_Functional_Smoke_003 completed successfully.')

            return current_time != changed_time

        except Exception as E:
            logger.error("Error occurred while executing TC_Functional_Smoke_003: %s", str(E))
            return False
    def TC_Functional_Smoke_26(self):
        logger.info('Validate Administration User Password management functionality in HG')
        try:
            if not self.device_health.health_check():
                logger.error('Device health check failed. Exiting the test.')
                self.utils.get_dbglog()
                return False

            logger.debug('Navigating to Administration menu')
            self.utils.find_element(*locators.AdministrationMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_UserSubMenu).click()

            user_type = self.utils.find_element(*locators.AdministrationMenu_UserSubMenu_Row1Col2).text
            if user_type.lower().strip() == 'admin':
                user = self.utils.find_element(*locators.AdministrationMenu_UserSubMenu_Row1Col1)
            else:
                user_type = self.utils.find_element(*locators.AdministrationMenu_UserSubMenu_Row2Col2).text
                if user_type.lower().strip() == 'admin':
                    user = self.utils.find_element(*locators.AdministrationMenu_UserSubMenu_Row2Col1)

            action = ActionChains(self.driver)
            action.context_click(user).perform()
            self.utils.find_element('//*[@id="editMenu"]').click()

            logger.debug('Setting a new password')
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Pass).send_keys(
                Inputs.temp_password)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_CfmPass).send_keys(
                Inputs.temp_password)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_SaveBtn).click()

            self.login_as_new_user(Inputs.username, Inputs.temp_password)
            message = self.enable_disable_AP1()

            logger.debug('Going back to Administration menu')
            self.utils.find_element(*locators.AdministrationMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_UserSubMenu).click()

            user_type = self.utils.find_element(*locators.AdministrationMenu_UserSubMenu_Row1Col2).text
            if user_type.lower().strip() == 'admin':
                user = self.utils.find_element(*locators.AdministrationMenu_UserSubMenu_Row1Col1)
            else:
                user_type = self.utils.find_element(*locators.AdministrationMenu_UserSubMenu_Row2Col2).text
                if user_type.lower().strip() == 'admin':
                    user = self.utils.find_element(*locators.AdministrationMenu_UserSubMenu_Row2Col1)

            action = ActionChains(self.driver)
            action.context_click(user).perform()
            self.utils.find_element('//*[@id="editMenu"]').click()

            # Reverting password
            logger.debug('Reverting password')
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Pass).send_keys(Inputs.password)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_CfmPass).send_keys(Inputs.password)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_SaveBtn).click()

            if 'succeeded' in message:
                logger.info('Admin Rights are checked and working fine')
                return True
            else:
                logger.error('Test Case Failed')
                self.utils.get_dbglog()
                return False
        except Exception as E:
            logger.error("Error occurred while executing TC_Functional_Smoke_26: %s", str(E))
            return False
    def TC_Functional_Smoke_27(self):
        logger.info('Validating Guest User & Password management functionality')
        try:
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            self.utils.find_element(*locators.AdministrationMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_UserSubMenu).click()

            user_type = self.utils.find_element(*locators.AdministrationMenu_UserSubMenu_Row1Col2).text
            if user_type.lower().strip() == 'guest':
                user = self.utils.find_element(*locators.AdministrationMenu_UserSubMenu_Row1Col1)
            else:
                user_type = self.utils.find_element(*locators.AdministrationMenu_UserSubMenu_Row2Col2).text
                if user_type.lower().strip() == 'guest':
                    user = self.utils.find_element(*locators.AdministrationMenu_UserSubMenu_Row2Col1)

            action = ActionChains(self.driver)
            action.context_click(user).perform()
            self.utils.find_element('//*[@id="editMenu"]').click()

            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Pass).send_keys(Inputs.temp_password)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_CfmPass).send_keys(Inputs.temp_password)

            button = self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_ToggleBtn)
            button_src = button.get_attribute('src')

            if 'button_off.png' in button_src:
                button.click()

            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_SaveBtn).click()
            self.utils.logout_gui()

            self.login_as_new_user(Inputs.guest, Inputs.temp_password)

            # go to Network
            message = self.enable_disable_AP1()

            self.utils.find_element(*locators.AdministrationMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_UserSubMenu).click()

            user_type = self.utils.find_element('//*[@id="users2"]/td[2]').text
            if user_type.lower().strip() == 'guest':
                user = self.utils.find_element('//*[@id="users2"]/td[1]')
            else:
                user_type = self.utils.find_element('//*[@id="users1"]/td[2]').text
                if user_type.lower().strip() == 'guest':
                    user = self.utils.find_element('//*[@id="users1"]/td[1]')

            action = ActionChains(self.driver)
            action.context_click(user).perform()
            self.utils.find_element('//*[@id="editMenu"]').click()

            logger.debug("Reverting password")
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Pass).send_keys(Inputs.password)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_CfmPass).send_keys(Inputs.password)

            button = self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_ToggleBtn)
            button_src = button.get_attribute('src')

            if 'button_on.png' in button_src:
                button.click()

            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_SaveBtn).click()
            time.sleep(5)

            if 'succeeded' not in message:
                logger.info('Guest Rights are checked and It\'s working fine')
                self.utils.logout_gui()
                return True
            else:
                logger.error('Test Case Failed')
                self.utils.get_dbglog()
                return False
        except Exception as E:
            logger.error("Error occurred while executing TC_Functional_Smoke_27: %s", str(E))
            return False
    def TC_Functional_Smoke_28_1(self):
        logger.info('Validating Custom Admin User & Password management functionality')
        try:
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            self.utils.find_element(*locators.AdministrationMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_UserSubMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_AddNewUser).click()

            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Name).send_keys(Inputs.new_admin)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Pass).send_keys(
                Inputs.temp_password)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_CfmPass).send_keys(
                Inputs.temp_password)
            user_type = Select(self.utils.find_element('//*[@id="tf1_selGroup"]'))
            user_type.select_by_value('admin')
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Desc).send_keys('Test Admin')
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_TimeOut).send_keys('10')
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_SaveBtn).click()
            logger.info('New user with Admin rights is created')

            self.utils.logout_gui()
            self.login_as_new_user(Inputs.new_admin, Inputs.temp_password)
            message = self.enable_disable_AP1()
            self.utils.logout_gui()

            logger.debug('Removing New User after Test case is executed')
            self.login.webgui_login()

            # go to Administration
            self.utils.find_element(*locators.AdministrationMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_UserSubMenu).click()

            new_user = self.utils.find_element('//*[@id="users4"]/td[1]')
            action = ActionChains(self.driver)
            action.context_click(new_user).perform()
            self.utils.find_element('//*[@id="deleteMenu"]').click()

            if 'succeeded' in message:
                logger.info('Admin Rights are checked and Its working fine')
                return True
            else:
                logger.error('Admin Rights are NOT working fine')
                self.utils.get_dbglog()
                return False
        except Exception as e:
            logger.error("Error occurred while executing TC_Functional_Smoke_28_1: %s", str(e))
            return False
    def TC_Functional_Smoke_28_2(self):
        logger.info('Validating Custom Guest User & Password management functionality')
        try:
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            # go to Administration
            self.utils.find_element(*locators.AdministrationMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_UserSubMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_AddNewUser).click()

            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Name).send_keys(Inputs.new_guest)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Pass).send_keys(
                Inputs.temp_password)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_CfmPass).send_keys(
                Inputs.temp_password)

            button = self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_ToggleBtn)
            button_src = button.get_attribute('src')

            if 'button_off.png' in button_src:
                button.click()

            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Desc).send_keys('Test Guest')
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_TimeOut).send_keys('10')
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_SaveBtn).click()
            logger.info('New user with Guest rights is created')

            self.utils.logout_gui()
            self.login_as_new_user(Inputs.new_guest, Inputs.temp_password)

            # go to Network Menu
            message = self.enable_disable_AP1()

            self.utils.logout_gui()

            logger.debug('Removing New User after Test case is executed')
            self.login.webgui_login()
            self.utils.find_element(*locators.AdministrationMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_UserSubMenu).click()

            new_user = self.utils.find_element('//*[@id="users4"]/td[1]')

            action = ActionChains(self.driver)
            action.context_click(new_user).perform()
            self.utils.find_element('//*[@id="deleteMenu"]').click()
            time.sleep(5)

            if 'succeeded' not in message:
                logger.info('Guest Rights are checked and Its working fine')
                return True
            else:
                logger.error('Test Case Failed')
                self.utils.get_dbglog()
                return False
        except Exception as e:
            logger.error("Error occurred while executing TC_Functional_Smoke_28_2: %s", str(e))
            return False
    def TC_Functional_Smoke_32(self):
        logger.info("Validate the maintenance functionality like Reboot from Web GUI - 5 Iterations")
        try:

            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            for i in range(5):
                # Your code here
                logger.debug(f"Reboot Iteration {i}")
                    # go to Administration >> Maintenance >> Reboot
                self.utils.find_element(*locators.AdministrationMenu).click()
                self.utils.find_element(*locators.AdministrationMenu_MaintenanceSubMenu).click()
                self.utils.find_element(*locators.Maintenance_BackupReboot_RebootButton).click()

                self.utils.accept_alert()
                logger.debug('Reseting Device (Estimated Time: 200 Seconds)')
                time.sleep(200)

                if self.device_health.health_check() == False:
                    logger.error('Device health check failed. Exiting the test.')
                    return False

                # self.login.webgui_login()
        except Exception as e:
            logger.error("Error occurred while executing TC_Functional_Smoke_32: %s", str(e))
            return False

    def enable_disable_AP1(self):
        self.utils.find_element(*locators.NetworkMenu).click()
        self.utils.find_element(*locators.NetworkMenu_WirelessSubMenu).click()

        get_ap_status = self.utils.find_element('//*[@id="1"]/td[1]').text
        edit_ap = self.utils.find_element('//*[@id="1"]/td[2]')
        action = ActionChains(self.driver)
        action.context_click(edit_ap).perform()
        time.sleep(5)

        if get_ap_status.lower() == 'disabled':
            self.utils.find_element('//*[@id="enableMenu"]').click()
            self.utils.accept_alert()
        else:
            self.utils.find_element('//*[@id="disableMenu"]').click()
            self.utils.accept_alert()

        try:
            return self.utils.find_element('//*[@id="main"]/div[6]/p').text
        except Exception as E:
            logger.error(E)
            return ""

    def login_as_new_user(self, username, password):
        try:
            try:
                self.utils.find_element(*locators.LoginPage_UserName).send_keys(username)
                self.utils.find_element(*locators.LoginPage_Password).send_keys(password)
                self.utils.find_element(*locators.LoginPage_LoginButton).click()
                time.sleep(5)  # Wait for the page to load

            except Exception as e:
                logger.error(f"Error occurred while logging in with provided credentials: {str(e)}")
                try:
                    # If there was an error, try logging in with default credentials (if available)
                    self.utils.find_element(*locators.LoginPage_UserName).send_keys(Inputs.username)
                    self.utils.find_element(*locators.LoginPage_Password).send_keys(Inputs.password)
                    self.utils.find_element(*locators.LoginPage_LoginButton).click()
                    time.sleep(5)  # Wait for the page to load

                except Exception as e:
                    logger.error(f"Error occurred while logging in with default credentials: {str(e)}")

            finally:
                try:
                    # Handle any pop-up or alert that may appear after login (regardless of success or failure)
                    self.utils.find_element('//*[@id="tf1_forcedLoginContent"]/div/a').click()
                    time.sleep(5)
                except:
                    logger.error("Error occurred while closing the login popup")

            logger.info("Login completed")
        except Exception as E:
            logger.error(f"Error occurred while logging : {str(e)}")

    def static_wan_configuration(self):
        if self.device_health.health_check() == False:
            logger.error('Device health check failed. Exiting the test.')
            return False

        self.utils.search_gui('WAN IPv4 Configuration')
        wan = Select(self.utils.find_element('//*[@id="tf1_ispType"]', '#tf1_ispType'))
        wan.select_by_value('1')

        static_wan_address = '20.15.10.17'
        subnet = '255.255.255.0'
        gateway = '20.15.10.1'
        primary_dns = '1.2.3.4'
        secondary_dns = '1.2.3.5'

        self.utils.find_element('//*[@id="tf1_stIpAddr"]').send_keys(static_wan_address)
        self.utils.find_element('//*[@id="tf1_stIpSnetMask"]').send_keys(subnet)
        self.utils.find_element('//*[@id="tf1_stGwIpAddr"]').send_keys(gateway)
        self.utils.find_element('//*[@id="tf1_primaryDns"]').clear()
        self.utils.find_element('//*[@id="tf1_primaryDns"]').send_keys(primary_dns)
        self.utils.find_element('//*[@id="tf1_secDns"]').clear()
        self.utils.find_element('//*[@id="tf1_secDns"]').send_keys(secondary_dns)
        self.utils.find_element('//*[@id="tf1_frmwanIPv4Config"]/div[35]/input[1]').click()
        self.utils.accept_alert()

        self.utils.search_gui('WAN Port Configuration')
        time.sleep(2)
        self.utils.find_element('//*[@id="tf1_vlanId"]').clear()
        self.utils.find_element('//*[@id="tf1_vlanId"]').send_keys('999')
        time.sleep(5)
        self.utils.find_element("//input[@title='Save']").click()
        self.utils.accept_alert()
        time.sleep(300)

        logger.debug('Checking IPv4 Connectivity with Ping')
        command = 'cmd /c ping 20.15.10.2 -4 -n 10'
        success = 0
        cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out = cmd.communicate()
        output = str(out[0])
        # logger.debug(output)

        if 'time' and 'TTL' in output:
            logger.debug('IPv4 Ping is successful')
            success += 1

        else:
            ping_fail_check_1 = 'could not find host'
            ping_fail_check_2 = 'Request timed out'
            if ('time' not in output) and (ping_fail_check_1 in output) or (ping_fail_check_2 in output):
                logger.debug('Ping IPv4 Failed')
                self.utils.get_dbglog()

        logger.debug('Reverting back to 1015')
        self.login.webgui_login()

        self.utils.search_gui('WAN IPv4 Configuration')
        wan = Select(self.utils.find_element('//*[@id="tf1_ispType"]', '#tf1_ispType'))
        wan.select_by_value('0')
        dns = Select(self.utils.find_element("//select[@id='tf1_dnsServerSource']", 'tf1_dnsServerSource'))
        dns.select_by_value('1')
        self.utils.find_element('//*[@id="tf1_frmwanIPv4Config"]/div[35]/input[1]').click()

        self.utils.search_gui('WAN Port Configuration')
        time.sleep(2)
        self.utils.find_element('//*[@id="tf1_vlanId"]').clear()
        self.utils.find_element('//*[@id="tf1_vlanId"]').send_keys('1015')
        time.sleep(5)
        self.utils.find_element("//input[@title='Save']").click()
        self.utils.accept_alert()
        time.sleep(300)

    def website_check(self, urls):

        from selenium import webdriver

        driver = webdriver.Chrome()

        success_count = 0

        for url in urls:
            try:
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])
                driver.get(url)
                title = driver.title

                if title != '':
                    success_count += 1

                time.sleep(10)
            except Exception as e:
                pass
        time.sleep(5)
        if success_count > 0:
            logger.info('URL access is successful for at least one website')
            return True
        else:
            logger.error('Unable to access any of the URL')
            return False

    def ftp_check(self):
        ftp_files = []
        test_ftp = 0
        try:
            ftp = FTP()
            time.sleep(5)
            ftp.connect(host='10.64.218.26', timeout=30)
            time.sleep(5)
            login_ = ftp.login(user='ftpuser', passwd='Jio@1234')
            time.sleep(5)
            logger.info(login_)
            ftp.retrlines('NLST', ftp_files.append)
            time.sleep(5)
            total_files = len(ftp_files)
            file_index = random.randint(0, total_files)
            fileName = ftp_files[file_index]
            x = ftp.retrbinary("RETR " + fileName, open(fileName, 'wb').write)
            logger.debug(x)
            return True
        except Exception as E:
            logger.error(f"Error occurred while connecting FTP server")
            if 'fail' in str(E):
                return False

    def TC_Functional_Smoke_39(self):
        logger.info("Validate default firewall functionality ")
        try:
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            self.utils.find_element(*locators.SecurityMenu).click()
            self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu).click()
            self.utils.find_element('//*[@id="tf1_frmdefaultPolicy"]/div[3]/p/input').click()
            self.utils.find_element('//*[@id="tf1_frmdefaultPolicy"]/div[5]/input[1]').click()

            if self.utils.ping_ipv4_from_lan_client() == False and self.utils.ping_ipv6_from_lan_client() == False:
                logger.info('Block Always functionality is working fine with ping ipv4 and Ipv6')

            logger.debug('Checking Block Always functionality')

            fails = 0
            urls = ['https://www.youtube.com/watch?v=VVsC2fD1BjA',
                    'https://www.onlinesbi.sbi',
                    'https://www.facebook.com']
            if not self.website_check(urls):
                logger.info(' Block Always functioanality with Youtube streamingn working fine')
            else:
                fails += 1

            logger.debug("Reverting back the changes to Allow Always")
            self.driver.refresh()
            self.utils.find_element("/html/body/div/div/h1/a").click()
            self.login.webgui_login()

            self.utils.find_element(*locators.SecurityMenu).click()
            self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu).click()

            self.utils.find_element('//*[@id="tf1_frmdefaultPolicy"]/div[1]/p/input').click()

            self.utils.find_element('//*[@id="tf1_frmdefaultPolicy"]/div[5]/input[1]').click()

            logger.debug('Checking Allow Always functionality')
            if self.utils.ping_ipv4_from_lan_client() == True:
                logger.info('Allow Always functionality is working fine with ping ipv4')
            else:
                fails += 1
            if self.utils.ping_ipv6_from_lan_client() == True:
                logger.info('Allow Always functionality is working fine with ping Ipv6')
            else:
                fails += 1

            urls = ['https://www.youtube.com/watch?v=VVsC2fD1BjA',
                    'https://www.onlinesbi.sbi',
                    'https://www.facebook.com']
            if self.website_check(urls):
                logger.info(' Allow Always functionality working fine')
            else:
                fails += 1

            if fails==0:
                return True
            else:
                return False
        except Exception as e:
            logger.error("Error occurred while executing TC_Functional_Smoke_39: %s", str(e))
            return False

    def add_firewall_rule(self, service_type='HTTP', action_type='DROP', rule_type='Outbound'):
        self.login.webgui_login()
        self.utils.find_element(*locators.SecurityMenu).click()
        self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu).click()
        try:
            logger.debug(f"Adding IPv4 Firewall Rule for {service_type}")
            self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu_IPv4FirewallRules).click()
            self.utils.find_element(*locators.IPv4FirewallRules_AddNewBtn).click()

            select_service = Select(self.utils.find_element(*locators.IPv4FirewallRulesConfiguration_Service))
            select_service.select_by_value(service_type)

            action = Select(self.utils.find_element(*locators.IPv4FirewallRulesConfiguration_Action))
            action.select_by_value(action_type)

            self.utils.find_element(*locators.IPv4FirewallRulesConfiguration_SaveBtn).click()
            logger.info(f"IPv4 Firewall Rule for {service_type} is added successfully")

        except Exception as E:
            logger.error(f"Error occurred while adding IPv4 rules for {service_type}: {str(E)}")

        try:
            logger.debug(f"Adding IPv6 Firewall Rule for {service_type}")

            self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu_IPv6FirewallRules).click()
            self.utils.find_element(*locators.IPv6FirewallRules_AddNewBtn).click()
            rule = Select(self.utils.find_element(*locators.IPv6FirewallRulesConfiguration_RuleType))
            rule.select_by_value(rule_type)

            select_service = Select(self.utils.find_element(*locators.IPv6FirewallRulesConfiguration_Service))
            select_service.select_by_value(service_type)
            action = Select(self.utils.find_element(*locators.IPv6FirewallRulesConfiguration_Action))
            action.select_by_value(action_type)
            self.utils.find_element(*locators.IPv6FirewallRulesConfiguration_SaveBtn).click()
            logger.info(f"IPv6 Firewall Rule for {service_type} is added successfully")
        except Exception as E:
            logger.error(f"Error occurred while adding IPv6 rules for {service_type}: {str(E)}")

    def delete_firewall_rule(self, service_type='HTTP'):
        self.login.webgui_login()
        self.utils.find_element(*locators.DashboardMenu).click()
        self.utils.find_element(*locators.SecurityMenu).click()
        self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu).click()

        try:
            logger.debug(f"Deleting IPv4 Firewall Rule for {service_type}")
            self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu_IPv4FirewallRules).click()
            total_rules_ = self.utils.find_element(*locators.IPv4FirewallRules_Entries).text
            total_rules = int(total_rules_.split(' ')[-2])
            for rule in range(total_rules):
                firewall_rule = self.utils.find_element('//*[@id="firewallRules{}"]/td[2]'.format(rule + 1))
                if service_type in firewall_rule.text:
                    action = ActionChains(self.driver)
                    action.context_click(firewall_rule).perform()
                    self.utils.find_element(*locators.IPv4FirewallRules_DeleteMenu).click()
                    break
            logger.info(f"IPv4 Firewall Rule for {service_type} is deleted successfully")
        except Exception as E:
            logger.error(f"Error occurred while deleting IPv4 rules for {service_type}: {str(E)}")

        try:
            logger.debug(f"Deleting IPv6 Firewall Rule for {service_type}")
            self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu_IPv6FirewallRules).click()

            total_rules_ = self.utils.find_element(*locators.IPv6FirewallRules_Entries).text
            total_rules = int(total_rules_.split(' ')[-2])
            for rule in range(total_rules):
                firewall_rule = self.utils.find_element('//*[@id="{}"]/td[3]'.format(rule + 1))
                if service_type in firewall_rule.text:
                    action = ActionChains(self.driver)
                    action.context_click(firewall_rule).perform()
                    self.utils.find_element(*locators.IPv6FirewallRules_DeleteMenu).click()
                    break
            logger.info(f"IPv6 Firewall Rule for {service_type} is deleted successfully")
        except:
            logger.error(f"Error occurred while deleting IPv6 rules for {service_type}: {str(E)}")

    def edit_firewall_rule(self, service_type='HTTP', action_type='DROP'):

        self.login.webgui_login()
        self.utils.find_element(*locators.DashboardMenu).click()
        self.utils.find_element(*locators.SecurityMenu).click()
        self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu).click()

        try:
            logger.debug(f"Editing IPv4 Firewall Rule for {service_type}")
            self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu_IPv4FirewallRules).click()
            total_rules_ = self.utils.find_element(*locators.IPv4FirewallRules_Entries).text
            total_rules = int(total_rules_.split(' ')[-2])
            for rule in range(total_rules):
                firewall_rule = self.utils.find_element('//*[@id="firewallRules{}"]/td[2]'.format(rule + 1))
                if service_type in firewall_rule.text:
                    action = ActionChains(self.driver)
                    action.context_click(firewall_rule).perform()
                    self.utils.find_element(*locators.IPv4FirewallRules_EditMenu).click()
                    break

            action = Select(self.utils.find_element(*locators.IPv4FirewallRulesConfiguration_Action))
            action.select_by_value(action_type)
            self.utils.find_element(*locators.IPv4FirewallRulesConfiguration_SaveBtn).click()
            logger.info(f"IPv4 Firewall Rule for {service_type} is edited successfully")
        except Exception as E:
            logger.error(f"Error occurred while editing IPv4 rules for {service_type}: {str(E)}")

        try:
            logger.debug(f"Editing IPv6 Firewall Rule for {service_type}")
            self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu_IPv6FirewallRules).click()

            total_rules_ = self.utils.find_element(*locators.IPv6FirewallRules_Entries).text
            total_rules = int(total_rules_.split(' ')[-2])
            for rule in range(total_rules):
                firewall_rule = self.utils.find_element('//*[@id="{}"]/td[3]'.format(rule + 1))
                if service_type in firewall_rule.text:
                    action = ActionChains(self.driver)
                    action.context_click(firewall_rule).perform()
                    self.utils.find_element(*locators.IPv6FirewallRules_EditMenu).click()
                    break

            action = Select(self.utils.find_element(*locators.IPv6FirewallRulesConfiguration_Action))
            action.select_by_value(action_type)
            self.utils.find_element(*locators.IPv6FirewallRulesConfiguration_SaveBtn).click()
            logger.info(f"IPv6 Firewall Rule for {service_type} is edited successfully")

        except Exception as E:
            logger.error(f"Error occurred while editing IPv6 rules for {service_type}: {str(E)}")

    def TC_Functional_Sanity_002_1(self):
        logger.info('Validating HTTPS Firewall Rule Functionality')
        try:

            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            urls = ['https://accounts.google.com',
                    'https://www.onlinesbi.sbi',
                    'https://www.facebook.com']
            failCount = 0
            if self.website_check(urls) == True:
                logger.info('Default HTTPS Service is running fine')
            else:
                failCount += 1
                logger.error('Default HTTPS Service is not running as expected')
                self.utils.get_dbglog()

            logger.debug('Adding HTTPS Block Firewall Rules')
            self.add_firewall_rule('HTTPS', 'DROP', 'Outbound')
            if self.website_check(urls) == False:
                logger.info('Block Firewall Rule for HTTPS is working as expected')
            else:
                failCount += 1
                logger.error('Block Firewall Rule for HTTPS is not working as expected')
                self.utils.get_dbglog()

            logger.debug('Rechecking HTTP Service after Enabling firewall Rules')
            self.edit_firewall_rule('HTTPS', 'ACCEPT')

            if self.website_check(urls) == True:
                logger.info('Allow Firewall Rule for HTTP is working as expected')
            else:
                failCount += 1
                logger.error('Allow Firewall Rule for HTTP is not working as expected')
                self.utils.get_dbglog()

            logger.debug('Removing the existing Rule')
            self.delete_firewall_rule('HTTPS')

            if failCount == 0:
                return True
            else:
                return True

        except Exception as E:
            logger.error(f"Error occurred while checking HTTPS rules: {str(E)}")
            return False

    def TC_Functional_Sanity_002_2(self):
        logger.debug('Validating HTTP Firewall Rule Functionality')
        try:
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False
            urls = ['http://testhtml5.vulnweb.com',
                    'http://www.softwareqatest.com/qatweb1.html',
                    'http://testasp.vulnweb.com	']
            failCount = 0
            if self.website_check(urls) == True:
                logger.debug('Default HTTP Service is running fine')
            else:
                failCount += 1
                logger.debug('Default HTTP Service is not running as expected')
                self.utils.get_dbglog()

            logger.debug('Adding HTTPS Block Firewall Rules')
            self.add_firewall_rule('HTTP', 'DROP', 'Outbound')
            if self.website_check(urls) == False:
                logger.info('Block Firewall Rule for HTTP is working as expected')
            else:
                failCount += 1
                logger.error('Block Firewall Rule for HTTP is not working as expected')
                self.utils.get_dbglog()

            logger.debug('Rechecking HTTP Service after Enabling firewall Rules')
            self.edit_firewall_rule('HTTP', 'ACCEPT')

            if self.website_check(urls) == True:
                logger.info('Allow Firewall Rule for HTTP is working as expected')
            else:
                failCount += 1
                logger.error('Allow Firewall Rule for HTTP is not working as expected')
                self.utils.get_dbglog()

            logger.debug('Removing the existing Rule')
            self.delete_firewall_rule('HTTP')

            if failCount == 0:
                return True
            else:
                return True
        except Exception as E:
            logger.error(f"Error occurred while checking HTTP rules: {str(E)}")
            return False

    def TC_Functional_Sanity_002_3(self):
        logger.debug('Validating FTP Firewall Rule Functionality')
        try:
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            failCount = 0
            if self.ftp_check() == True:
                logger.debug('Default HTTP Service is running fine')
            else:
                failCount += 1
                logger.debug('Default HTTP Service is not running as expected')
                self.utils.get_dbglog()

            logger.debug('Adding FTP Block Firewall Rules')
            self.add_firewall_rule('FTP', 'DROP', 'Outbound')
            if self.ftp_check() == False:
                logger.debug('Block Firewall Rule for HTTP is working as expected')
            else:
                failCount += 1
                logger.debug('Block Firewall Rule for HTTP is not working as expected')
                self.utils.get_dbglog()

            logger.debug('Rechecking FTP Service after Enabling firewall Rules')
            self.edit_firewall_rule('FTP', 'ACCEPT')

            if self.ftp_check() == True:
                logger.debug('Allow Firewall Rule for HTTP is working as expected')
            else:
                failCount += 1
                logger.debug('Allow Firewall Rule for HTTP is not working as expected')
                self.utils.get_dbglog()

            logger.debug('Removing the existing Rule')
            self.delete_firewall_rule('FTP')
        except Exception as E:
            logger.error(f"Error occurred while checking FTP rules: {str(E)}")
            return False

    def TC_Functional_Smoke_029(self):
        logger.info("Verifying the dashboard page information of ONT")

        try:
            # Check device health
            if not self.device_health.health_check():
                logger.error('Device health check failed. Exiting the test.')
                return False

            success_count = 0

            # Check firmware version
            get_firmware_version = self.utils.get_firmware_version()
            if get_firmware_version == Inputs.latest_firmware:
                logger.info('Firmware version on Dashboard is verified successfully')
                success_count += 1
            else:
                logger.error(
                    'Firmware Version is not the same as required. Please check Input File details or Firmware in the device.')

            # Check model name
            get_model = self.utils.find_element(*locators.Dashboard_ModelName).text
            model_name = Inputs.latest_firmware.split('_')[1]
            if get_model == model_name:
                logger.info('Model Name on Dashboard is verified successfully')
                success_count += 1
            else:
                logger.error('Model name is not the same as required')

            # Check serial number
            get_serial_number = self.utils.get_serial_number()
            if len(get_serial_number) == 15 and get_serial_number != '000000000000000':
                logger.info(f'Serial Number on Dashboard is verified successfully : {get_serial_number}')
                success_count += 1
            else:
                logger.error('Serial number is invalid')

            # Check AP SSID information
            get_ap1_ssid = self.utils.find_element(*locators.Dashboard_ap1_SSID).text
            get_ap4_ssid = self.utils.find_element(*locators.Dashboard_ap4_SSID).text
            if get_ap1_ssid and get_ap4_ssid:
                logger.info(f'Primary AP SSID Information exists on Dashboard : {get_ap1_ssid} And {get_ap4_ssid}')
                success_count += 1
            else:
                logger.info('Primary AP SSID Information is missing on Dashboard')

            # Check WAN MAC Address
            wan_mac_address = self.utils.find_element(*locators.Dashboard_WAN_MacAddress).text
            if wan_mac_address and len(wan_mac_address) == 17:
                logger.info(f'WAN MAC Address Information exists on Dashboard : {wan_mac_address}')
                success_count += 1
            else:
                logger.error('WAN MAC Address Information is missing on Dashboard')

            # Check LAN MAC Address
            lan_mac_address = self.utils.find_element(*locators.Dashboard_LAN_MacAddress).text
            if lan_mac_address and len(lan_mac_address) == 17:
                logger.info(f'LAN MAC Address Information exists on Dashboard : {lan_mac_address}')
                success_count += 1
            else:
                logger.error('LAN MAC Address Information is missing on Dashboard')

            # Check WAN and LAN IP Address
            wan_ip_address = self.utils.find_element(*locators.Dashboard_WAN_IPv4).text
            lan_ip_address = self.utils.find_element(*locators.Dashboard_LAN_IPv4).text
            if wan_ip_address != '0.0.0.0' and lan_ip_address != '0.0.0.0' and wan_ip_address and lan_ip_address:
                logger.info(f'WAN and LAN IP Address Information exists on Dashboard : {wan_ip_address} Ans {lan_ip_address}')
                success_count += 1
            else:
                logger.error('WAN and LAN Address Information are missing on Dashboard')

            # Check WAN and LAN Status
            wan_status = self.utils.find_element(*locators.Dashboard_WAN_Status)
            lan_status = self.utils.find_element(*locators.Dashboard_LAN_Status)
            if wan_status.get_attribute('class') == 'yesNo' and lan_status.get_attribute('class') == 'yesNo':
                logger.info('WAN and LAN Status Information exists on Dashboard')
                success_count += 1
            else:
                logger.error('WAN and LAN Status Information are missing on Dashboard')

            # Check TR-069 Status
            tr69_status = self.utils.find_element(*locators.Dashboard_tr69_Status)
            if tr69_status.get_attribute('class') == 'yesNo':
                logger.info('TR-069 Status Information exists on Dashboard')
                success_count += 1
            else:
                logger.error('TR-069 Status Information is missing on Dashboard')

            # Check WAN IPv6 Information
            wan_ipv6_1 = self.utils.find_element(*locators.Dashboard_WAN_IPv6_1).text
            wan_ipv6_2 = self.utils.find_element(*locators.Dashboard_WAN_IPv6_2).text
            if wan_ipv6_1 and wan_ipv6_2:
                logger.info('WAN IPv6 Information exists on Dashboard')
                success_count += 1
            else:
                logger.error('WAN IPv6 Information is missing on Dashboard')

            # Check LAN IPv6 Information
            lan_ipv6_1 = self.utils.find_element(*locators.Dashboard_LAN_IPv6_1).text
            lan_ipv6_2 = self.utils.find_element(*locators.Dashboard_LAN_IPv6_2).text
            if lan_ipv6_1 and lan_ipv6_2:
                logger.info('LAN IPv6 Information exists on Dashboard')
                success_count += 1
            else:
                logger.error('LAN IPv6 Information is missing on Dashboard')

            if success_count == 11:
                logger.info('All information on the Dashboard is verified successfully.')
                return True
            else:
                logger.error('Verification of Dashboard information failed.')
                self.utils.get_dbglog()
                return False

        except Exception as e:
            logger.error("Error occurred while executing TC_Functional_Smoke_029: %s", str(e))
            return False

    def TC_Functional_Sanity_007(self):
        logger.info("Validate the static IP allocation functionality to WAN side of the ONT")
        try:
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            #Step 1: Configuring IPv4
            self.utils.search_gui('WAN IPv4 Configuration')
            wan = Select(self.utils.find_element(*locators.WanConfigIPv4_SelectMenu))
            wan.select_by_value('1')
            # Configuring Static IPv4
            logger.info('Configuring IP type to Static')
            static_wan_address = '20.15.10.17'
            subnet = '255.255.255.0'
            gateway = '20.15.10.1'
            primary_dns = '1.2.3.4'
            secondary_dns = '1.2.3.5'
            self.utils.find_element(*locators.WanConfigIPv4_IpAddr).send_keys(static_wan_address)
            self.utils.find_element(*locators.WanConfigIPv4_IpSubnetMask).send_keys(subnet)
            self.utils.find_element(*locators.WanConfigIPv4_GatewayIPAddr).send_keys(gateway)
            self.utils.find_element(*locators.WanConfigIPv4_PrimaryDns).clear()
            self.utils.find_element(*locators.WanConfigIPv4_PrimaryDns).send_keys(primary_dns)
            self.utils.find_element(*locators.WanConfigIPv4_SecondaryDns ).clear()
            self.utils.find_element(*locators.WanConfigIPv4_SecondaryDns).send_keys(secondary_dns)
            self.utils.find_element(*locators.WanConfigIPv4_SaveBtn).click()
            self.utils.accept_alert()
            time.sleep(15)

            #Step 2:Configuring IPv6
            self.utils.search_gui('WAN IPv6 Configuration')
            wan = Select(self.utils.find_element(*locators.WanConfigIPv6_SelectMenu))
            wan.select_by_value('ifStatic6')
            static_wan_address_v6 = 'fd00::65'
            prefix = '64'
            gateway_v6 = 'fd00::64'
            primary_dns_v6 = 'fd00::63'
            secondary_dns_v6 = 'fd00::62'
            self.utils.find_element(*locators.WanConfigIPv6_IPv6Addr).send_keys(static_wan_address_v6)
            self.utils.find_element(*locators.WanConfigIPv6_PrefixLen).send_keys(prefix)
            self.utils.find_element(*locators.WanConfigIPv6_Gateway).send_keys(gateway_v6)
            self.utils.find_element(*locators.WanConfigIPv6_PrimaryDns).clear()
            self.utils.find_element(*locators.WanConfigIPv6_PrimaryDns).send_keys(primary_dns_v6)
            self.utils.find_element(*locators.WanConfigIPv6_SecondaryDns).clear()
            self.utils.find_element(*locators.WanConfigIPv6_SecondaryDns).send_keys(secondary_dns_v6)
            self.utils.find_element(*locators.WanConfigIPv6_SaveBtn).click()
            self.utils.accept_alert()
            time.sleep(15)

            # go to Status Menu
            self.utils.find_element(*locators.StatusMenu).click()
            self.utils.find_element(*locators.StatusMenu_DeviceStatus).click()
            self.utils.find_element(*locators.DeviceStatus_WANInfo).click()
            ipv4_after_change = self.utils.find_element( *locators.WanInfo_IPv4Addr).text
            static_ipv4 = ipv4_after_change.split(' ')[0]

            try:
                ipv6_after_change = self.utils.find_element(*locators.WanInfo_IPv6Addr1).text
            except:
                ipv6_after_change = self.utils.find_element( *locators.WanInfo_IPv6Addr2).text

            static_ipv6 = ipv6_after_change.split(' ')[0]

            if static_wan_address_v6 in static_ipv6:
                pass
            else:
                ipv6_after_change = self.utils.find_element( *locators.WanInfo_IPv6Addr2).text

            logger.info(ipv6_after_change)


            if static_ipv4 == static_wan_address:
                logger.info('Static WAN IPv4 Configured Successfully')
            else:
                logger.error('Static WAN IPv4 Configuration Failed')

            if (static_wan_address_v6 in ipv6_after_change):
                logger.info('Static WAN IPv6 Configured Successfully')
            else:
                logger.error('Static WAN IPv6 Configuration Failed')

            ont_state = self.utils.find_element( '//*[@id="main"]/div[6]/div[1]/div/div[17]/p').text


            # Configuring Dynamic WAN IPv4
            self.utils.search_gui('WAN IPv4 Configuration')
            wan = Select(self.utils.find_element(*locators.WanConfigIPv4_SelectMenu))
            wan.select_by_value('0')
            dns = Select(self.driver.find_element(By.ID, 'tf1_dnsServerSource'))
            dns.select_by_value('1')
            self.utils.find_element(*locators.WanConfigIPv4_SaveBtn).click()
            time.sleep(10)

            # Configuring Dynamic IPv6
            logger.debug('Configuring IP type to Dynamic')
            self.utils.search_gui('WAN IPv6 Configuration')
            wan = Select(self.utils.find_element(*locators.WanConfigIPv6_SelectMenu))
            wan.select_by_value('dhcp6c')
            self.utils.find_element( '//*[@id="tf1_dhcpV6SatelessMode2"]').click()
            self.utils.find_element(*locators.WanConfigIPv6_SaveBtn).click()
            time.sleep(10)

            # waiting for changes
            time.sleep(60)
            dynamic_ipv4 = ''
            dynamic_ipv6 = ''

            # go to Status Menu
            self.utils.find_element(*locators.StatusMenu).click()
            self.utils.find_element(*locators.StatusMenu_DeviceStatus).click()
            self.utils.find_element(*locators.DeviceStatus_WANInfo).click()
            try:
                dynamic_ipv4_full = self.utils.find_element( *locators.WanInfo_IPv4Addr).text
                dynamic_ipv4 = dynamic_ipv4_full.split(' ')[0]
                try:
                    dynamic_ipv6_full = self.utils.find_element(*locators.WanInfo_IPv6Addr1).text
                except:
                    dynamic_ipv6_full = self.utils.find_element(*locators.WanInfo_IPv6Addr1).text
                dynamic_ipv6 = dynamic_ipv6_full.split(' ')[0]
                if 'fe80' in dynamic_ipv6:
                    dynamic_ipv6 = self.utils.find_element(*locators.WanInfo_IPv6Addr2).text

                logger.info('WAN IP Addresses after configuration to Dynamic')
                logger.info('Wan Ipv4 Address: {}'.format(dynamic_ipv4))
                logger.info('Wan Ipv6 Address: {}'.format(dynamic_ipv6))

                if dynamic_ipv4 == '0.0.0.0':
                    time.sleep(30)
                    # Retry After 30 Seconds
                    dynamic_ipv4_full = self.utils.find_element( *locators.WanInfo_IPv4Addr).text
                    dynamic_ipv4 = dynamic_ipv4_full.split(' ')[0]

                    try:
                        dynamic_ipv6_full = self.utils.find_element(*locators.WanInfo_IPv6Addr1).text
                    except:
                        dynamic_ipv6_full = self.utils.find_element(*locators.WanInfo_IPv6Addr2).text

                    dynamic_ipv6 = dynamic_ipv6_full.split(' ')[0]
            except Exception as E:
                logger.error(E)

            success = 0
            if static_ipv4 != dynamic_ipv4 and dynamic_ipv4 != '0.0.0.0':
                logger.info('Dynamic IPv4 from WAN Side is received')
                success += 1
            else:
                logger.error('ONT has not received dynamic wan ipv4')

            if static_ipv6 != dynamic_ipv6 and dynamic_ipv6 != '':
                logger.info('Dynamic IPv6 from WAN Side is received')
                success += 1
            else:
                logger.error('ONT has not received dynamic wan ipv6')

            if success == 2:
                return True
            else :
                self.utils.get_dbglog()
                return False
        except Exception as E:
            logger.error(f"Error occurred while configuring the static IP : {str(E)}")
            return False


    def TC_Functional_Sanity_55(self):
        for number in range (5):
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False
            self.factory_reset()
            self.login.webgui_login()

    def set_parameters_before_factory_reset(self):
        # driver = setup.get_driver()
        # network_menu(driver)
        self.utils.find_element(*locators.NetworkMenu).click()
        self.utils.find_element('//*[@id="tf1_network_accessPoints"]').click()

        device_model_ = Inputs.device_model
        list_ap = [1, 4]
        if device_model_ == 'JCO110':
            list_ap = [1]

        ap_status = []
        # Changing AP status to Enable/Disable
        for i in list_ap:
            xp_ = '//*[@id="{}"]/td[1]'.format(i)
            # print(xp_)
            get_ap_status = self.utils.find_element( xp_).text
            # ap_status.append(get_ap_status)

            edit_xpath = '//*[@id="{}"]/td[2]'.format(i)
            edit_ap = self.utils.find_element(edit_xpath)
            action = ActionChains(self.driver)
            action.context_click(edit_ap).perform()
            time.sleep(5)

            if get_ap_status.lower() == 'disabled':
                # print('Enabling AP{}'.format(i))
                self.utils.find_element('//*[@id="enableMenu"]').click()
                self.utils.accept_alert()
            else:
                # print('Disabling AP{}'.format(i))
                self.utils.find_element( '//*[@id="disableMenu"]').click()
                self.utils.accept_alert()

            get_ap_status = self.utils.find_element(xp_).text
            # print(get_ap_status)
            ap_status.append(get_ap_status)
            time.sleep(20)
            # print('after sleep')

        time.sleep(30)

        # go to Dashboard
        self.utils.find_element(*locators.DashboardMenu).click()
        self.utils.find_element(*locators.NetworkMenu).click()

        # go to Network

        self.utils.find_element('//*[@id="tf1_network_accessPoints"]').click()
        self.utils.find_element('//*[@id="main"]/div[6]/ul/li[2]/a').click()

        profile_list = []
        for i in list_ap:
            xp_profile = '//*[@id="{}"]/td[2]'.format(i)
            test_ssid = 'Test' + ' ' + str(i)
            xp_profile_ = self.utils.find_element(xp_profile)
            action = ActionChains(self.driver)
            action.context_click(xp_profile_).perform()
            self.utils.find_element('//*[@id="editMenu"]').click()
            self.utils.accept_alert()
            self.utils.find_element('//*[@id="tf1_txtSSID"]').clear()
            self.utils.find_element('//*[@id="tf1_txtSSID"]').send_keys(test_ssid)
            password_ = '12345678'
           
            self.utils.find_element('//*[@id="tf1_txtWPAPasswd"]').clear()
            self.utils.find_element('//*[@id="tf1_txtWPAPasswd"]').send_keys(password_)

         
            self.utils.find_element( '//*[@id="tf1_txtWPACnfPasswd"]').clear()
            self.utils.find_element( '//*[@id="tf1_txtWPACnfPasswd"]').send_keys(password_)


            self.utils.find_element( '//*[@id="tf1_dialog"]/div[3]/input[2]').click()

            time.sleep(20)
            profile_list.append(self.utils.find_element( xp_profile).text)
        return ap_status, profile_list

    def get_access_point_status(self):
       
        get_access_point_status = []
        get_profile_names = []

        device_model_ = Inputs.device_model
        access_point = [1, 4]
        if device_model_ == 'JCO110':
            access_point = [1]

        self.utils.find_element(*locators.NetworkMenu).click()

        self.utils.find_element( '//*[@id="tf1_network_accessPoints"]').click()

        for ap in access_point:
            xp_ = '//*[@id="{}"]/td[1]'.format(ap)
            get_ap_status = self.utils.find_element( xp_).text
            get_access_point_status.append(get_ap_status)
            xpp_ = '//*[@id="{}"]/td[3]'.format(ap)
            get_profile_name = self.utils.find_element( xpp_).text
            get_profile_names.append(get_profile_name)

        # print(get_access_point_status)
        # print(get_profile_names)

        return get_access_point_status, get_profile_names

    def TC_Functional_Smoke_011_012(self):
        # Step 1: Validating Device Backup and Restore functionality from WEBGUI
        logger.info(" Validating Device Backup and Restore functionality from WEBGUI")
        try:
            # Check device health
            if not self.device_health.health_check():
                logger.error("Device health check failed. Exiting the test.")
                return False

            # Step 2: Configuring Wireless Profiles
            logger.info("Configuring Wireless Profiles")
            wireless_data_before_backup = self.set_parameters_before_factory_reset()

            # Step 3: Obtain device information
            self.utils.find_element(*locators.DashboardMenu).click()
            serial_number = self.utils.find_element("/html/body/div[1]/div[1]/div[2]/p[2]/span").text
            model = self.utils.find_element(*locators.Dashboard_ModelName).text
            backup_file = f"{serial_number}_{model}.enc"

            # Step 4: Adding Port Forwarding Rule
            logger.info("Adding Port Forwarding Rule")
            self.utils.search_gui('Port Forwarding')
            self.utils.find_element('//*[@id="main"]/div[6]/div/div[4]/input[2]').click()
            port_forwarding_configuration = Select(self.driver.find_element(By.ID, 'tf1_selFwAction'))
            port_forwarding_configuration.select_by_value('ACCEPT')
            self.utils.find_element('//*[@id="tf1_txtFwSrcUserDestination"]').send_keys('192.168.29.100')
            self.utils.find_element('//*[@id="tf1_txtinternalPort"]').send_keys('80')
            self.utils.find_element('//*[@id="tf1_dialog"]/div[3]/input[2]').click()
            time.sleep(10)

            # Step 5: Taking Backup from WEBGUI
            self.backup()

            files = os.listdir(Inputs.file_path)
            if backup_file in files:
                logger.info("Backup file found in the given path.")
            else:
                logger.error("Backup file not found.")
                return False

            time.sleep(10)

            # Step 6: Restore Operation
            restore_file_location = os.path.join(Inputs.file_path, backup_file)
            logger.debug("Performing Restore Operation")
            self.factory_reset()
            self.login.webgui_login()
            self.restore(restore_file_location)

            # Step 7: Checking Port Forwarding rule details after Restore
            logger.debug("Checking Port Forwarding rule details after Restore")
            success = 0

            self.utils.search_gui('Port Forwarding')
            time.sleep(2)
            data = self.utils.find_element("//tr[@id='portForwarding1']", '#portForwarding1')
            port_forwarding_status = data.is_displayed()  # Gives True for success

            if port_forwarding_status:
                success += 1

            # Step 8: Checking wireless profiles after Restore
            logger.debug("Checking wireless profiles after Restore")
            wireless_data_after_restore = self.get_access_point_status()
            if wireless_data_before_backup == wireless_data_after_restore:
                success += 1
            else:
                print("Fail")

            # Step 9: Removing Backup File
            logger.debug("Removing Backup File")
            os.remove(os.path.join(Inputs.file_path, backup_file))

            if success != 2:
                self.utils.get_dbglog()
                return False
            else:
                return True
        except Exception as e:
            logger.error("Error occurred while executing TC_Functional_Smoke_011_012: %s", str(e))
            return False

    def TC_Functional_Smoke_36(self):
        logger.info('Validating redirection to login page after Factory Reset from WebGUI')
        try:
            # Perform factory reset
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            self.reboot()

            # Check if redirected to the login page
            try:
                self.utils.find_element(*locators.LoginPage_LoginForm)
                logger.info("WebGUI successfully redirected to the login page after Factory Reset")
                return True
            except:
                logger.error("WebGUI did not redirect to the login page after Factory Reset")
                return False
        except Exception as e:
            logger.error(f"Error occurred during TC_Functional_Smoke_37: {str(e)}")
            return False

    def TC_Functional_Smoke_37(self):
        logger.info('Validating redirection to login page after Factory Reset from WebGUI')
        try:
            # Perform factory reset
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False
            self.factory_reset()

            # Check if redirected to the login page
            try:
                self.utils.find_element("//div[@class='loginForm']", "div[class='loginForm']")
                logger.info("WebGUI successfully redirected to the login page after Factory Reset")
                return True
            except:
                logger.error("WebGUI did not redirect to the login page after Factory Reset")
                return False
        except Exception as e:
            logger.error(f"Error occurred during TC_Functional_Smoke_37: {str(e)}")
            return False

    def TC_Functional_Smoke_33(self):
        logger.info("Password should be change after evey factory reset")
        try:
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            self.factory_reset()

            username = 'admin'
            password = 'P@ssw0rd'

            self.utils.find_element(*locators.LoginPage_UserName).send_keys(username)
            self.utils.find_element(*locators.LoginPage_Password).send_keys(password)

            self.utils.find_element(*locators.LoginPage_LoginButton).click()
            try:
                message = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/p').text
                if 'invalid' in message.lower():
                    logger.debug('Enter Default Password')
            except:
                pass

            display_check = 0
            try:
                self.utils.find_element(*locators.LoginPage_UserName).send_keys(username)
                self.utils.find_element(*locators.LoginPage_Password).send_keys('Jiocentrum')
                self.utils.find_element(*locators.LoginPage_LoginButton).click()
                display_check = self.driver.find_element(By.XPATH, '//*[@id="tf1_adminPassword"]').is_displayed()
                self.driver.find_element(By.XPATH, '//*[@id="tf1_adminPassword"]').send_keys(password)
                self.driver.find_element(By.XPATH, '//*[@id="tf1_cnfAdminPassword"]').send_keys(password)
                self.driver.find_element(By.XPATH, '//*[@id="tf1_guestPassword"]').send_keys(password)
                self.driver.find_element(By.XPATH, '//*[@id="tf1_cnfGuestPassword"]').send_keys(password)
                self.driver.find_element(By.XPATH, '//*[@id="tf1_frmchangePassword"]/div[9]/input[1]').click()
                self.utils.find_element(*locators.LoginPage_UserName).send_keys(username)
                self.utils.find_element(*locators.LoginPage_Password).send_keys(password)
                self.utils.find_element(*locators.LoginPage_LoginButton).click()

            except Exception as E:
                self.utils.find_element(*locators.LoginPage_UserName).send_keys(username)
                self.utils.find_element(*locators.LoginPage_Password).send_keys(password)
                self.utils.find_element(*locators.LoginPage_LoginButton).click()

            finally:
                try:
                    self.driver.find_element(By.XPATH, '//*[@id="tf1_forcedLoginContent"]/div/a').click()
                except Exception as E:
                    pass

            if display_check == True:
                logger.info("Password is changed after Factory Reset")
                return True
            else:
                logger.error("Password is NOT changed after Factory Reset")
                self.utils.get_dbglog()
                return False
        except Exception as e:
            logger.error(f"Error occurred during TC_Functional_Smoke_33: {str(e)}")
            return False

    def TC_Functional_Smoke_020(self):
        logger.info('Validating LAN Side DNS Proxy Functionality')
        try:
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False
            self.utils.search_gui("LAN IPv4 Configuration")
            self.utils.find_element(*locators.LANIPv4Config_DNSServers).click()
            self.utils.find_element('//*[@id="tf1_DnsSvrs"]/option[1]').click()
            self.utils.find_element(*locators.LANIPv4Config_DomainName).clear()
            self.utils.find_element(*locators.LANIPv4Config_DomainName).send_keys('proxy')
            self.utils.find_element(*locators.LANIPv4Config_SaveBtn).click()
            time.sleep(30)
            commands = ['cmd /c ipconfig/release',
                        'ipconfig/renew',
                        'ipconfig/all']
            count = 0
            for command in commands:
                cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                cmd_out = cmd.communicate()
                time.sleep(5)
            dns = []
            lan_status_string = str(cmd_out[0])
            lan_status_string_split = lan_status_string.split(',')
            packets = lan_status_string_split[-1].split('\\r\\n')
            for data in packets:
                packets_ = data.split(':')
                if packets_[0] == '   DNS Servers . . . . . . . . . . . ':
                    dns.append(data)
                    i = packets.index(data)
                    dns.append(packets[i + 1])
                    dns.append(packets[i + 2])
                    break
            logger.info(dns)
            if dns[1].strip() in '192.168.29.1':
                return True
            else:
                return False
        except Exception as E:
            logger.error(f"Error occurred during TC_Functional_Smoke_020: {str(E)}")
            return False

    def TC_Functional_Smoke_021(self):
        logger.info('Validating LAN Side DNS from ISP Functionality')
        try:
            if self.device_health.health_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            self.utils.search_gui("LAN IPv4 Configuration")
            self.utils.find_element(*locators.LANIPv4Config_DNSServers).click()
            self.utils.find_element('//*[@id="tf1_DnsSvrs"]/option[2]').click()
            self.utils.find_element("//input[@id='tf1_dhcpDomainName']",'#tf1_dhcpDomainName','tf1_dhcpDomainName').clear()
            self.utils.find_element("//input[@id='tf1_dhcpDomainName']",'#tf1_dhcpDomainName','tf1_dhcpDomainName').send_keys('isp')
            self.utils.find_element("//input[@title='Save']","input[title='Save']").click()
            time.sleep(30)
            commands = ['cmd /c ipconfig/release',
                        'ipconfig/renew',
                        'ipconfig/all']
            count = 0
            for command in commands:
                cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                cmd_out = cmd.communicate()
                time.sleep(5)
            dns = []
            lan_status_string = str(cmd_out[0])
            lan_status_string_split = lan_status_string.split(',')
            packets = lan_status_string_split[-1].split('\\r\\n')
            for data in packets:
                packets_ = data.split(':')
                # logger.info(packets_)
                if packets_[0] == '   DNS Servers . . . . . . . . . . . ':
                    # logger.info('here')
                    # logger.info(packets_)
                    dns.append(data)
                    i = packets.index(data)
                    dns.append(packets[i + 1])
                    dns.append(packets[i + 2])
                    break
            logger.info(dns)
            if dns[1].strip() not in '192.168.29.1':
                return True
            else:
                return False
        except Exception as E:
            logger.error(f"Error occurred during TC_Functional_Smoke_021: {str(E)}")
            return False

    def TC_Functional_Sanity_046(self):
        logger.info('Starting WAN VLAN ID Change validation from WEBGUI')

        try:
            if not self.device_health.health_check():
                logger.error('Device health check failed. Exiting the test.')
                return False

            current_wan_vlan = self.utils.get_wan_port()
            new_wan_vlan = '200'

            logger.debug(f'Changing WAN VLAN ID from {current_wan_vlan} to {new_wan_vlan}')
            self.utils.find_element(*locators.WANPortConfig_VlanID).clear()
            self.utils.find_element(*locators.WANPortConfig_VlanID).send_keys(new_wan_vlan)
            self.utils.find_element(*locators.WANPortConfig_VlanID_SaveBtn).click()
            self.utils.accept_alert()

            time.sleep(200)

            logger.debug('Checking whether WAN VLAN ID is changed or not')
            self.login.webgui_login()

            changed_vlan = self.utils.get_wan_port()
            logger.info(f'Current WAN VLAN: {changed_vlan}')

            success = 0
            if changed_vlan != current_wan_vlan:
                logger.info('WAN VLAN ID changed successfully')
                success += 1
            else:
                logger.error('WAN VLAN ID did not change')
                self.utils.get_dbglog()
                return False

            logger.debug('Checking WAN IP and related configurations')

            self.utils.find_element(*locators.DashboardMenu).click()
            ipv4_wan_info = self.utils.find_element(*locators.Dashboard_WAN_IPv4).text
            ipv4_wan_ = ipv4_wan_info.split('/')
            ipv4_wan_ip_address = ipv4_wan_[0]
            logger.info(f'WAN IPv4 Address: {ipv4_wan_ip_address}')

            if ipv4_wan_ip_address == '0.0.0.0' and success == 1:
                logger.error('WAN IP in Vlan 200 is not received. Check 200 Server if it is down')

            private_subnet = ipv4_wan_ip_address.split('.')[-2]
            if private_subnet == '200':
                logger.info('Device received WAN IP in Vlan 200')
                success += 1

            if self.utils.ping_ipv4_from_lan_client():
                logger.info('IPv4 Ping to Server is successful')
                success += 1

            logger.debug('Reverting WAN VLAN to Original state')
            self.utils.search_gui('WAN Port Configuration')
            self.utils.find_element(*locators.WANPortConfig_VlanID).clear()
            self.utils.find_element(*locators.WANPortConfig_VlanID).send_keys(current_wan_vlan)
            self.utils.find_element(*locators.WANPortConfig_VlanID_SaveBtn).click()
            self.utils.accept_alert()

            time.sleep(200)

            if success == 3:
                logger.info("Changing behavior of VLAN ID is working as expected")
                return True
            else:
                logger.error("Changing behavior of VLAN ID is NOT working as expected")
                return False

        except Exception as e:
            logger.error(f"Error occurred during TC_Functional_Sanity_046: {str(e)}")
            return False

    def TC_Functional_Smoke_019(self):
        logger.info('Validating Telnet Access for R-Build')
        try:
            if not self.device_health.health_check():
                logger.error('Device health check failed. Exiting the test.')
                return False
            HOST = "192.168.29.1"
            user = 'root'
            success = 0
            iteration = 1
            logger.debug('Checking Telnet Access')
            tn = telnetlib.Telnet()
            try:
                for i in Inputs.telnet_password:
                    tn.open(HOST)
                    time.sleep(5)
                    tn.write(user.encode("ascii") + b"\n")
                    time.sleep(5)
                    password = i
                    tn.write(password.encode("ascii") + b"\n")
                    break
            except Exception as E:
                if 'fail' in str(E).lower():
                    logger.info('Telnet is happening successfully')
                    tn.close()
                    return True
                else:
                    logger.error('Telnet should not be allowed in R build\n Test Case Failed')
                    tn.close()
                    return  False
        except Exception as e:
            logger.error(f"Error occurred during TC_Functional_Smoke_019: {str(e)}")
            return False

    def upgrade_downgrade_from_webgui(self):
        if not self.device_health.health_check():
            logger.error('Device health check failed. Exiting the test.')
            return False

        # print(Inputs.downgrade_image)
        # print(Inputs.downgrade_sign)


        self.login.acs_login()
        print('Found device on ACS')
        self.driver.implicitly_wait(60)
        self.driver.switch_to.default_content()
        try:
            element = WebDriverWait(self.driver, 70).until(presence_of_element_located((By.ID, "lmi5")))
            element.click()
        except:
            try:
                element = WebDriverWait(self.driver, 70).until(presence_of_element_located((By.ID, "lmi5")))
                element.click()
            except:
                print('element not found')
        self.driver.switch_to.frame("frmDesktop")
        time.sleep(2)
        element = WebDriverWait(self.driver, 70).until(presence_of_element_located((By.ID, "txbFind")))
        element.clear()
        time.sleep(2)
        element = WebDriverWait(self.driver, 70).until(presence_of_element_located((By.ID, "txbFind")))
        element.send_keys('Device.DeviceInfo')
        time.sleep(2)
        self.driver.find_element(By.ID, "hlFind_btn").click()
        time.sleep(2)
        print('Navigated to Device.Info')
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.switch_to.frame("frmButtons")
        time.sleep(2)
        self.driver.find_element(By.ID, 'UcDeviceSettingsControls1_btnGetCurrent_btn').click()
        time.sleep(2)
        self.driver.switch_to.default_content()
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[@id="btnAlertOk_btn"]').click()
        time.sleep(60)
        self.driver.switch_to.frame("frmDesktop")
        time.sleep(2)
        for i in range(10, 15):
            parameter_name = self.driver.find_element(By.XPATH,
                                                 '//*[@id="tblParamsTable"]/tbody/tr[' + str(i) + ']/td[1]').text
            if parameter_name == 'X_RJIL_COM_DowngradeEnable':
                break

        downgrade_parameter = self.driver.find_element(By.XPATH,
                                                  '//*[@id="tblParamsTable"]/tbody/tr[' + str(i) + ']/td[2]').text
        if downgrade_parameter == '0':
            print('Downgrade parameter is 0')
            self.driver.switch_to.default_content()
            time.sleep(5)
            self.driver.switch_to.frame("frmButtons")
            time.sleep(3)
            self.driver.find_element(By.ID, "UcDeviceSettingsControls1_btnChange_btn").click()
            time.sleep(3)
            self.driver.switch_to.default_content()
            time.sleep(3)
            self.driver.switch_to.frame("frmDesktop")
            time.sleep(3)
            self.driver.find_element(By.XPATH, '//*[@id="tblParamsTable"]/tbody/tr[' + str(i) + ']/td[2]/input').clear()
            time.sleep(3)
            self.driver.find_element(By.XPATH,
                                '//*[@id="tblParamsTable"]/tbody/tr[' + str(i) + ']/td[2]/input').send_keys('1')
            time.sleep(3)
            self.driver.find_element(By.XPATH,
                                '//*[@id="tblParamsTable"]/tbody/tr[' + str(i + 1) + ']/td[2]/input').clear()
            time.sleep(3)
            a = datetime.now()
            b = datetime.date(a)
            self.driver.find_element(By.XPATH,
                                '//*[@id="tblParamsTable"]/tbody/tr[' + str(i + 1) + ']/td[2]/input').send_keys(
                str(b) + 'T22:00:00.000000+05:30')
            time.sleep(3)
            self.driver.switch_to.default_content()
            time.sleep(3)
            self.driver.switch_to.frame("frmButtons")
            time.sleep(3)
            self.driver.find_element(By.ID, 'UcDeviceSettingsControls1_btnSendUpdate_btn').click()
            alert = self.driver.switch_to.alert
            alert.accept()
            time.sleep(3)
            self.driver.switch_to.default_content()
            time.sleep(3)
            self.driver.find_element(By.XPATH, '//*[@id="btnAlertOk_btn"]').click()
            print('Pushed Downgrade Enable parameter as 1 and Downgrade Validity parameter as ' + str(
                b) + 'T22:00:00.000000+05:30')
            print('Waiting 60 seconds')
            time.sleep(60)
            self.driver.switch_to.frame("frmDesktop")
            check = self.driver.find_element(By.XPATH,
                                        '/html/body/form/div[4]/table/tbody/tr/td[2]/span/table/tbody/tr[2]/td/div/table/tbody/tr[' + str(
                                            i + 1) + ']/td[2]').text
            print(check)
            try:
                assert check == (str(b) + 'T22:00:00.000000+05:30')
            except:
                print('Downgrade validity parameter did not get enabled')
        else:
            print('Downgrade parameter already in enable state')

        self.driver.switch_to.window(self.driver.window_handles[0])




        #firmware downgrade
        self.change_firmware(Inputs.downgrade_image,Inputs.downgrade_sign)
        self.login.webgui_login()

        if self.utils.get_firmware_version() == Inputs.downgrade:

            print('Firmware Downgraded Successfully to ' + Inputs.downgrade)
        else:
            print('Firmware is not Downgraded ')

        self.change_firmware(Inputs.upgrade_image, Inputs.upgrade_sign)
        self.login.webgui_login()

        if self.utils.get_firmware_version() == Inputs.upgrade:

            print('Firmware Downgraded Successfully to ' + Inputs.upgrade)
        else:
            print('Firmware is not Downgraded ')

        if not self.device_health.health_check():
            logger.error('Device health check failed. Exiting the test.')
            return False



    def change_firmware(self,upgrade_file,signature_file):
        self.utils.find_element(*locators.AdministrationMenu).click()
        self.utils.find_element(*locators.AdministrationMenu_MaintenanceSubMenu).click()
        self.utils.find_element(*locators.Maintenance_Firmware_Upgrade).click()

        upload_image_path = self.utils.find_element( "//input[@id='txtUploadFile']","#txtUploadFile",'txtUploadFile')
        upload_image_path.send_keys(upgrade_file)
        self.utils.find_element('//*[@id="tf1_frmUploadImg"]/div[1]/input[2]',"form[id='tf1_frmUploadImg'] input[title='Upload']").click()
        self.utils.accept_alert()
        time.sleep(60)


        upload_image_path = self.utils.find_element("//input[@id='txtSignatureFile']", "#txtSignatureFile", 'txtSignatureFile')
        upload_image_path.send_keys(signature_file)
        self.utils.find_element('//*[@id="tf1_frmUploadSigImg"]/div[1]/input[2]',"form[id='tf1_frmUploadSigImg'] input[title='Upload']").click()
        self.utils.accept_alert()
        time.sleep(60)

        self.utils.find_element('//*[@id="main"]/div[7]/div/div[3]/div[5]/input[2]').click()
        self.utils.accept_alert()

        time.sleep(300)




















