from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import Inputs
import locators
from logger_util import logger
from device_health import device_health
from Utils import Utils
import time
from login import login
from selenium.webdriver.common.action_chains import ActionChains

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
            #
            # username = 'admin'
            # set_password = 'PR@shant2301'

            logger.debug('Setting a new password')
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Pass).send_keys(Inputs.temp_password)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_CfmPass).send_keys(Inputs.temp_password)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_SaveBtn).click()

            logger.debug('Logging in with the new password')
            try:
                self.utils.find_element(*locators.LoginPage_UserName).send_keys(Inputs.username)
                self.utils.find_element(*locators.LoginPage_Password).send_keys(Inputs.temp_password)
                self.utils.find_element(*locators.LoginPage_LoginButton).click()
            except Exception as E:
                logger.error('Login attempt failed. Using default credentials.')
                self.utils.find_element(*locators.LoginPage_UserName).send_keys(Inputs.username)
                self.utils.find_element(*locators.LoginPage_Password).send_keys(Inputs.password)
                self.utils.find_element(*locators.LoginPage_LoginButton).click()

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

        try:
            self.utils.find_element(*locators.LoginPage_UserName).send_keys(Inputs.guest)
            self.utils.find_element(*locators.LoginPage_Password).send_keys(Inputs.temp_password)
            self.utils.find_element(*locators.LoginPage_LoginButton).click()

        except Exception as E:
            self.utils.find_element(*locators.LoginPage_UserName).send_keys(Inputs.new_guest)
            self.utils.find_element(*locators.LoginPage_Password).send_keys(Inputs.password)
            self.utils.find_element(*locators.LoginPage_LoginButton).click()

        finally:
            try:
                time.sleep(5)
                self.utils.find_element( '//*[@id="tf1_forcedLoginContent"]/div/a').click()
                time.sleep(5)
            except Exception as E:
                pass

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
            return True
        else:
            logger.error('Test Case Failed')
            self.utils.get_dbglog()
            return False

    def TC_Functional_Smoke_010_1(self):
        logger.info('Validating Guest User & Password management functionality')
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
            print('New user with Admin rights is created')
            self.utils.logout_gui()

            try:
                self.utils.find_element( *locators.LoginPage_UserName).send_keys(Inputs.new_admin)
                self.utils.find_element( *locators.LoginPage_Password).send_keys(Inputs.temp_password)
                self.utils.find_element( *locators.LoginPage_LoginButton).click()

            except Exception as E:
                self.utils.find_element( *locators.LoginPage_UserName).send_keys(Inputs.username)
                self.utils.find_element( *locators.LoginPage_Password).send_keys(Inputs.password)
                self.utils.find_element( *locators.LoginPage_LoginButton).click()

            finally:
                try:
                    time.sleep(5)
                    self.utils.find_element( '//*[@id="tf1_forcedLoginContent"]/div/a').click()
                    time.sleep(5)
                except Exception as E:
                    pass


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

            try:
                self.utils.find_element(*locators.LoginPage_UserName).send_keys(Inputs.new_guest)
                self.utils.find_element(*locators.LoginPage_Password).send_keys(Inputs.temp_password)
                self.utils.find_element(*locators.LoginPage_LoginButton).click()
            except Exception as E:
                self.utils.find_element(*locators.LoginPage_UserName).send_keys(Inputs.username)
                self.utils.find_element(*locators.LoginPage_Password).send_keys(Inputs.password)
                self.utils.find_element(*locators.LoginPage_LoginButton).click()

            finally:
                try:
                    self.utils.find_element( '//*[@id="tf1_forcedLoginContent"]/div/a').click()
                except:
                    pass

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

