import subprocess
from telnetlib import EC
from selenium import webdriver

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import Inputs
import locators
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
        self.login=login(driver)
        self.device_health=device_health(driver)

    def TC_Functional_Smoke_002(self):
        logger.debug('Starting TC_Functional_Smoke_002: Validating MAC Address after Reboot and Reset')
        try:
            if self.device_health.healh_check()== False:
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

    def TC_Functional_Smoke_003(self):
        logger.info('Starting TC_Functional_Smoke_003: Validating Date & Time functionality of Device')
        try:
            if self.device_health.healh_check() == False:
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

        except Exception as e:
            logger.error("Error occurred while executing TC_Functional_Smoke_003: %s", str(e))
            return False

    def TC_Functional_Smoke_008(self):
        logger.info('Starting Test Case TC_Functional_Smoke_008')
        try:
            if not self.device_health.healh_check():
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
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Pass).send_keys(Inputs.temp_password)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_CfmPass).send_keys(Inputs.temp_password)
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
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return False

    def TC_Functional_Smoke_009(self):
        logger.info('Validating Guest User & Password management functionality')
        if self.device_health.healh_check() == False:
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

        user_type = self.utils.find_element( '//*[@id="users2"]/td[2]').text
        if user_type.lower().strip() == 'guest':
            user = self.utils.find_element('//*[@id="users2"]/td[1]')
        else:
            user_type = self.utils.find_element( '//*[@id="users1"]/td[2]').text
            if user_type.lower().strip() == 'guest':
                user = self.utils.find_element('//*[@id="users1"]/td[1]')

        action = ActionChains(self.driver)
        action.context_click(user).perform()
        self.utils.find_element( '//*[@id="editMenu"]').click()

        logger.debug("Reverting password")
        self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Pass).send_keys(Inputs.password)
        self.utils.find_element( *locators.AdministrationMenu_UsersConfiguration_CfmPass).send_keys(Inputs.password)

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

    def TC_Functional_Smoke_010_1(self):
        logger.info('Validating Custom Admin User & Password management functionality')
        try:
            if self.device_health.healh_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            self.utils.find_element(*locators.AdministrationMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_UserSubMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_AddNewUser).click()


            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Name).send_keys(Inputs.new_admin)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Pass).send_keys(Inputs.temp_password)
            self.utils.find_element( *locators.AdministrationMenu_UsersConfiguration_CfmPass).send_keys(Inputs.temp_password)
            user_type = Select(self.utils.find_element( '//*[@id="tf1_selGroup"]'))
            user_type.select_by_value('admin')
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Desc).send_keys('Test Admin')
            self.utils.find_element( *locators.AdministrationMenu_UsersConfiguration_TimeOut).send_keys('10')
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_SaveBtn).click()
            logger.info('New user with Admin rights is created')

            self.utils.logout_gui()
            self.login_as_new_user(Inputs.new_admin, Inputs.temp_password)
            message=self.enable_disable_AP1()
            self.utils.logout_gui()

            logger.debug('Removing New User after Test case is executed')
            self.login.webgui_login()

            # go to Administration
            self.utils.find_element(*locators.AdministrationMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_UserSubMenu).click()

            new_user=self.utils.find_element('//*[@id="users4"]/td[1]')
            action = ActionChains(self.driver)
            action.context_click(new_user).perform()
            self.utils.find_element( '//*[@id="deleteMenu"]').click()


            if 'succeeded' in message:
                logger.info('Admin Rights are checked and Its working fine')
                return True
            else:
                logger.error('Admin Rights are NOT working fine')
                self.utils.get_dbglog()
                return False
        except Exception as e:
            logger.error("Error occurred while executing TC_Functional_Smoke_010_1: %s", str(e))
            return False

    def TC_Functional_Smoke_010_2(self):
        logger.info('Validating Custom Guest User & Password management functionality')
        try:
            if self.device_health.healh_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            # go to Administration
            self.utils.find_element(*locators.AdministrationMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_UserSubMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_AddNewUser).click()

            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Name).send_keys(Inputs.new_guest)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Pass).send_keys(Inputs.temp_password)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_CfmPass).send_keys(Inputs.temp_password)

            button = self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_ToggleBtn)
            button_src = button.get_attribute('src')

            if 'button_off.png' in button_src:
                button.click()

            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Desc).send_keys('Test Guest')
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_TimeOut).send_keys('10')
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_SaveBtn).click()
            logger.info('New user with Guest rights is created')

            self.utils.logout_gui()
            self.login_as_new_user(Inputs.new_guest,Inputs.temp_password)

            # go to Network Menu
            message=self.enable_disable_AP1()

            self.utils.logout_gui()

            logger.debug('Removing New User after Test case is executed')
            self.login.webgui_login()
            self.utils.find_element(*locators.AdministrationMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_UserSubMenu).click()


            new_user=self.utils.find_element('//*[@id="users4"]/td[1]')

            action = ActionChains(self.driver)
            action.context_click(new_user).perform()
            self.utils.find_element( '//*[@id="deleteMenu"]').click()
            time.sleep(5)

            if 'succeeded' not in message:
                logger.info('Guest Rights are checked and Its working fine')
                return True
            else:
                logger.error('Test Case Failed')
                self.utils.get_dbglog()
                return False
        except Exception as e:
            logger.error("Error occurred while executing TC_Functional_Smoke_010_2: %s", str(e))
            return False

    def TC_Functional_Smoke_32(self):
        logger.info("Reboot from WebGUI 5 Iterations")
        for i in range(5):
            # Your code here
            print("Reboot Iteration ", i)

            if self.device_health.healh_check() == False:
                logger.error('Device health check failed. Exiting the test.')
                return False

                # go to Administration >> Maintenance >> Reboot
            self.utils.find_element(*locators.AdministrationMenu).click()
            self.utils.find_element(*locators.AdministrationMenu_MaintenanceSubMenu).click()
            self.utils.find_element(*locators.Maintenance_BackupReboot_RebootButton).click()

            self.utils.accept_alert()

            logger.debug('Reseting Device (Estimated Time: 200 Seconds)')
            time.sleep(200)

            self.login.webgui_login()

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
        if self.device_health.healh_check() == False:
            logger.error('Device health check failed. Exiting the test.')
            return False

        self.utils.search_gui('WAN IPv4 Configuration')
        wan = Select(self.utils.find_element('//*[@id="tf1_ispType"]','#tf1_ispType'))
        wan.select_by_value('1')

        static_wan_address = '20.15.10.17'
        subnet = '255.255.255.0'
        gateway = '20.15.10.1'
        primary_dns = '1.2.3.4'
        secondary_dns = '1.2.3.5'

        self.utils.find_element( '//*[@id="tf1_stIpAddr"]').send_keys(static_wan_address)
        self.utils.find_element( '//*[@id="tf1_stIpSnetMask"]').send_keys(subnet)
        self.utils.find_element( '//*[@id="tf1_stGwIpAddr"]').send_keys(gateway)
        self.utils.find_element( '//*[@id="tf1_primaryDns"]').clear()
        self.utils.find_element( '//*[@id="tf1_primaryDns"]').send_keys(primary_dns)
        self.utils.find_element( '//*[@id="tf1_secDns"]').clear()
        self.utils.find_element( '//*[@id="tf1_secDns"]').send_keys(secondary_dns)
        self.utils.find_element( '//*[@id="tf1_frmwanIPv4Config"]/div[35]/input[1]').click()
        self.utils.accept_alert()
        
        self.utils.search_gui('WAN Port Configuration')
        time.sleep(2)
        self.utils.find_element( '//*[@id="tf1_vlanId"]').clear()
        self.utils.find_element( '//*[@id="tf1_vlanId"]').send_keys('999')
        time.sleep(5)
        self.utils.find_element("//input[@title='Save']").click()
        self.utils.accept_alert()
        time.sleep(300)

        print('Checking IPv4 Connectivity with Ping')
        command = 'cmd /c ping 20.15.10.2 -4 -n 10'
        success = 0
        cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out = cmd.communicate()
        output = str(out[0])
        # print(output)

        if 'time' and 'TTL' in output:
            print('IPv4 Ping is successful')
            success += 1

        else:
            ping_fail_check_1 = 'could not find host'
            ping_fail_check_2 = 'Request timed out'
            if ('time' not in output) and (ping_fail_check_1 in output) or (ping_fail_check_2 in output):
                print('Ping IPv4 Failed')
                self.utils.get_dbglog()

        print('Reverting back to 1015')
        self.login.webgui_login()

        self.utils.search_gui('WAN IPv4 Configuration')
        wan = Select(self.utils.find_element('//*[@id="tf1_ispType"]', '#tf1_ispType'))
        wan.select_by_value('0')
        dns = Select(self.utils.find_element("//select[@id='tf1_dnsServerSource']",'tf1_dnsServerSource'))
        dns.select_by_value('1')
        self.utils.find_element( '//*[@id="tf1_frmwanIPv4Config"]/div[35]/input[1]').click()

        self.utils.search_gui('WAN Port Configuration')
        time.sleep(2)
        self.utils.find_element('//*[@id="tf1_vlanId"]').clear()
        self.utils.find_element('//*[@id="tf1_vlanId"]').send_keys('1015')
        time.sleep(5)
        self.utils.find_element("//input[@title='Save']").click()
        self.utils.accept_alert()
        time.sleep(300)

    def https_website_check(self):
        from selenium import webdriver
        driver = webdriver.Chrome()
        driver.implicitly_wait(30)

        success_count = 0
        urls = ['https://accounts.google.com',
                'https://www.onlinesbi.sbi',
                'https://www.facebook.com']

        for url in urls:
            try:
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])
                driver.get(url)
                title = driver.title

                if title != '':
                    success_count += 1

            except Exception as e:
                pass

        if success_count > 0:
            print('HTTPS site access is successful for at least one website')
        else:
            print('We are not able to access any HTTPS websites')

        return success_count

    def add_firewall_rule(self,service_='HTTP', action_value_='DROP', modify_existing=0):
        print("Adding Firewall Rule")
        self.login.webgui_login()
        self.utils.find_element(*locators.SecurityMenu).click()
        self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu).click()
        self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu_IPv4FirewallRules).click()

        if modify_existing == 0:
            self.utils.find_element(*locators.IPv4FirewallRules_AddNewBtn).click()
            select_service = Select(self.utils.find_element(*locators.IPv4FirewallRulesConfiguration_Service))
            select_service.select_by_value(service_)
            action = Select(self.utils.find_element(*locators.IPv4FirewallRulesConfiguration_Action))
            action.select_by_value(action_value_)
            self.utils.find_element(*locators.IPv4FirewallRulesConfiguration_SaveBtn).click()

            self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu_IPv6FirewallRules).click()
            self.utils.find_element(*locators.IPv6FirewallRules_AddNewBtn).click()
            rule_type = Select(self.utils.find_element(*locators.IPv6FirewallRulesConfiguration_RuleType))
            rule_type.select_by_value('Outbound')

            select_service = Select(self.utils.find_element(*locators.IPv6FirewallRulesConfiguration_Service))
            select_service.select_by_value(service_)
            action = Select(self.utils.find_element(*locators.IPv6FirewallRulesConfiguration_Action))
            action.select_by_value(action_value_)
            self.utils.find_element(*locators.IPv6FirewallRulesConfiguration_SaveBtn).click()
        if modify_existing == 1:
            action = ActionChains(self.driver)

            total_rules_=self.utils.find_element(*locators.IPv6FirewallRules_Entries).text
            total_rules = int(total_rules_.split(' ')[-2])

            rule_path = ''
            for rule in range(total_rules):
                firewall_rule = self.utils.find_element(By.XPATH, '//table/tbody/tr[{}]'.format(rule + 1)).text
                if service_ in firewall_rule:
                    rule_path = self.utils.find_element(By.XPATH, '//table/tbody/tr[{}]'.format(rule + 1))
                    break

            action.context_click(rule_path).perform()
            self.utils.find_element(*locators.IPv6FirewallRules_EditMenu)

            action = Select(self.utils.find_element(*locators.IPv4FirewallRulesConfiguration_Action))
            action.select_by_value(action_value_)
            self.utils.find_element(*locators.IPv6FirewallRulesConfiguration_SaveBtn)

            # Modifying IPv6 Rule to Allow
            self.utils.find_element('//*[@id="main"]/div[7]/ul/li[3]/a').click()
            action = ActionChains(self.driver)
            total_rules_=self.utils.find_element(*locators.IPv4FirewallRules_Entries).text

            total_rules = int(total_rules_.split(' ')[-2])
            # print(total_rules)
            rule_path = ''
            for rule in range(total_rules):
                firewall_rule = self.utils.find_element(By.XPATH, '//table/tbody/tr[{}]'.format(rule + 1)).text
                if service_ in firewall_rule:
                    rule_path = self.utils.find_element(By.XPATH, '//table/tbody/tr[{}]'.format(rule + 1))
                    break

            action.context_click(rule_path).perform()
            self.utils.find_element(*locators.IPv4FirewallRules_EditMenu)
            action = Select(self.utils.find_element(*locators.IPv6FirewallRulesConfiguration_Action))
            action.select_by_value(action_value_)
            self.utils.find_element(*locators.IPv6FirewallRulesConfiguration_SaveBtn).click()

    def delete_firewall_rule(self,service_='HTTP'):
        self.login.webgui_login()
        self.utils.find_element(*locators.DashboardMenu).click()
        self.utils.find_element(*locators.SecurityMenu).click()
        self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu).click()

        try:
            logger.info("Deleting the IPv4 rules")
            self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu_IPv4FirewallRules).click()
            total_rules_ = self.utils.find_element(*locators.IPv4FirewallRules_Entries).text
            total_rules = int(total_rules_.split(' ')[-2])
            for rule in range(total_rules):
                firewall_rule = self.utils.find_element('//*[@id="firewallRules{}"]/td[2]'.format(rule + 1))
                if service_ in firewall_rule.text:
                    action = ActionChains(self.driver)
                    action.context_click(firewall_rule).perform()
                    self.utils.find_element(*locators.IPv4FirewallRules_DeleteMenu).click()
                    break
        except:
            print('We are not able to delete IPv4 Firewall Rule')

        try:
            logger.info("Deleting the IPv6 rules")
            self.utils.find_element(*locators.SecurityMenu_FirewallSubMenu_IPv6FirewallRules).click()

            total_rules_=self.utils.find_element(*locators.IPv6FirewallRules_Entries).text
            total_rules = int(total_rules_.split(' ')[-2])
            for rule in range(total_rules):
                firewall_rule = self.utils.find_element('//*[@id="{}"]/td[3]'.format(rule + 1))
                if service_ in firewall_rule.text:
                    action = ActionChains(self.driver)
                    action.context_click(firewall_rule).perform()
                    self.utils.find_element(*locators.IPv6FirewallRules_DeleteMenu).click()
                    break
        except:
            print('We are not able to delete IPv6 Firewall Rule')

    def https_firewall_rule_check(self):
        # if self.device_health.healh_check() == False:
        #     logger.error('Device health check failed. Exiting the test.')
        #     self.utils.get_dbglog()
        #     return False
        #
        test_expected_check = [1, 0, 1]
        test_actual_check = []




        def https_website_check(self):
            print('Check Point https_website_check ')
            # setup = Setup()
            # driver = setup.get_driver()
            options = webdriver.ChromeOptions()
            options.add_argument('ignore-certificate-errors')
            options.add_argument("--start-maximized")

            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(30)
            tabs = ['https://accounts.google.com',
                    'https://www.onlinesbi.sbi',
                    'https://www.facebook.com']

            time.sleep(10)
            check = []
            for url in tabs:
                try:
                    self.driver.execute_script("window.open('');")
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    self.driver.get(url)
                    title_ = self.driver.title
                    # print(title_)
                    if title_ != '':
                        check.append(1)
                    else:
                        check.append(0)

                    time.sleep(20)
                except Exception as E:
                    pass

            if any(check) == 1:
                print('Http site access is successful for website')
            else:
                print('We are not able to access HTTP website')






        # default_https_check = https_website_check()
        # test_actual_check.append(default_https_check)
        # # print(default_https_check)
        # if default_https_check == 1:
        #     print('Default HTTPS Service is running fine')
        # else:
        #     print('Default HTTPS Service is not running as expected')
        #
        print('Adding HTTPS Block Firewall Rules')
        add_firewall_rule(service_='HTTPS', action_value_='DROP')
        time.sleep(30)
        print("Check Point 1")
        blocked_https_check = https_website_check(self)
        test_actual_check.append(blocked_https_check)
        if blocked_https_check == 0:
            print('Block Firewall Rule for HTTPS is working as expected')
        else:
            print('Block Firewall Rule for HTTPS is not working as expected')
            self.utils.get_dbglog()
        #
        # print('Rechecking HTTPS Service after Enabling firewall Rules')
        # add_firewall_rule(service_='HTTPS', action_value_='ACCEPT', modify_existing=1)
        # allowed_https_check = https_website_check()
        # test_actual_check.append(allowed_https_check)
        # if allowed_https_check == 1:
        #     print('Allow Firewall Rule for HTTPS is working as expected')
        # else:
        #     print('Allow Firewall Rule for HTTPS is not working as expected')
        #     get_dbglog()
        #
        print('Removing the existing Rule')
        delete_firewall_rule('HTTPS')
        #
        # success = 0
        # if test_expected_check == test_actual_check:
        #     success = 1
        #     print('Test Case is Pass')
        # else:
        #     print('Test Case is Fail')
        # return success

