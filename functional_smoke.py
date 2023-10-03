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
        self.utils = Utils(self.driver)
        self.login=login(self.driver)
        self.device_health=device_health(self.driver)

    def TC_Functional_Smoke_002(self):
        logger.debug('Starting TC_Functional_Smoke_002: Validating MAC Address after Reboot and Reset')
        try:
            if self.device_health.healh_check()== False:
                logger.error('Device health check failed. Exiting the test.')
                return False

            wan_mac_address = self.utils.find_element(*locators.mac_address_daseboard).text
            logger.debug(f'WAN MAC Address before Reboot: {wan_mac_address}')



            # go to Administration >> Maintenance >> Reboot
            self.utils.find_element('//*[@id="mainMenu5"]').click()
            self.utils.find_element('//*[@id="tf1_administration_backupRestore"]').click()
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
            self.utils.find_element('//*[@id="tf1_administration_backupRestore"]').click()
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

            # success = 0
            # if current_time != changed_time:
            #     success += 1

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

    # def TC_Functional_Smoke_008(self):
    #     print('Validating Admin User & Password management functionality')
    #     # print('#########################################################')
    #     # self.utils = webgui_login()
    #     # self.utils.implicitly_wait(30)
    #     # health = device_health_check(self.utils)
    #     # if health[-1] != 0:
    #     #     get_dbglog()
    #     #     exit()
    #
    #     if self.device_health.healh_check() == False:
    #         logger.error('Device health check failed. Exiting the test.')
    #         self.utils.get_dbglog()
    #         return False
    #
    #     # go to Administration
    #     #administration_menu(self.utils)
    #     self.utils.find_element('//*[@id="mainMenu5"]').click()
    #     try:
    #         self.utils.find_element('//*[@id="tf1_administration_users"]').click()
    #     except:
    #         self.utils.find_element('tf1_administration_users').click()
    #
    #     user_type = self.utils.find_element('//*[@id="users2"]/td[2]').text
    #     if user_type.lower().strip() == 'admin':
    #         user = self.utils.find_element('//*[@id="users2"]/td[1]')
    #     else:
    #         user_type = self.utils.find_element('//*[@id="users1"]/td[2]').text
    #         if user_type.lower().strip() == 'admin':
    #             user = self.utils.find_element('//*[@id="users1"]/td[1]')
    #
    #     action = ActionChains(self.driver)
    #     action.context_click(user).perform()
    #     self.utils.find_element('//*[@id="editMenu"]').click()
    #
    #     # element = self.utils.find_element_by_css_selector('#example-element')
    #     #
    #     # # Create an ActionChains object and right-click on the element
    #     # actions = ActionChains(self.driver)
    #     # actions.context_click(element).perform()
    #
    #
    #
    #     username = 'admin'
    #     set_password = 'PR@shant2301'
    #
    #
    #     self.utils.find_element( '//*[@id="tf1_txtPwd"]').send_keys(set_password)
    #     self.utils.find_element( '//*[@id="tf1_txtCfmPwd"]').send_keys(set_password)
    #     self.utils.find_element( '//*[@id="tf1_dialog"]/div[3]/input[2]').click()
    #
    #     print("check point 1")
    #     try:
    #         self.utils.find_element("","", 'tf1_userName').send_keys(username)
    #         self.utils.find_element("","", 'tf1_password').send_keys(set_password)
    #         self.utils.find_element("//button[normalize-space()='Login']","button[title='Login']", 'button.login.users.dashboard').click()
    #
    #     except Exception as E:
    #         print("check point 2")
    #         self.utils.find_element('//*[@id="tf1_userName"]',"", 'tf1_userName').send_keys('admin')
    #         self.utils.find_element('//*[@id="tf1_password"]',"", 'tf1_password').send_keys('P@ssw0rd')
    #         self.utils.find_element( "/html/body/div[1]/div/div/div[2]/form/div/div[5]/button").click()
    #
    #     finally:
    #         try:
    #             time.sleep(5)
    #             self.utils.find_element( '//*[@id="tf1_forcedLoginContent"]/div/a').click()
    #             time.sleep(5)
    #         except Exception as E:
    #             pass
    #
    #     print("go to Network menu")
    #     #network_menu(self.utils)
    #     self.utils.find_element('//*[@id="mainMenu3"]').click()
    #     self.utils.find_element('//*[@id="tf1_network_accessPoints"]').click()
    #     xp_ = '//*[@id="1"]/td[1]'
    #     get_ap_status = self.utils.find_element(xp_).text
    #
    #     edit_xpath = '//*[@id="1"]/td[2]'
    #     edit_ap = self.utils.find_element(edit_xpath)
    #     action = ActionChains(self.driver)
    #     action.context_click(edit_ap).perform()
    #     time.sleep(5)
    #
    #     if get_ap_status.lower() == 'disabled':
    #         # print('Enabling AP{}'.format(i))
    #         self.utils.find_element('//*[@id="enableMenu"]').click()
    #         try:
    #             # Accept the alert for connection change
    #             self.utils.switch_to.alert.accept()
    #             time.sleep(5)
    #         except Exception as E:
    #             pass
    #     else:
    #         # print('Disabling AP{}'.format(i))
    #         self.utils.find_element('//*[@id="disableMenu"]').click()
    #         try:
    #             # Accept the alert for connection change
    #             self.utils.switch_to.alert.accept()
    #             time.sleep(5)
    #         except Exception as E:
    #             pass
    #
    #     message = ''
    #     try:
    #         message = self.utils.find_element('//*[@id="main"]/div[6]/p').text
    #         print(message)
    #     except Exception as E:
    #         print(E)
    #
    #
    #
    #     print("go to Administration")
    #     self.utils.find_element('//*[@id="mainMenu5"]').click()
    #     try:
    #         self.utils.find_element( '//*[@id="tf1_administration_users"]').click()
    #     except:
    #         self.utils.find_element( 'tf1_administration_users').click()
    #
    #     user_type = self.utils.find_element( '//*[@id="users2"]/td[2]').text
    #     if user_type.lower().strip() == 'admin':
    #         user = self.utils.find_element('//*[@id="users2"]/td[1]')
    #     else:
    #         user_type = self.utils.find_element('//*[@id="users1"]/td[2]').text
    #         if user_type.lower().strip() == 'admin':
    #             user = self.utils.find_element( '//*[@id="users1"]/td[1]')
    #
    #     action = ActionChains(self.driver)
    #     action.context_click(user).perform()
    #     self.utils.find_element( '//*[@id="editMenu"]').click()
    #
    #     # Reverting password
    #     old_password = 'P@ssw0rd'
    #
    #     self.utils.find_element( '//*[@id="tf1_txtPwd"]').send_keys(old_password)
    #     self.utils.find_element( '//*[@id="tf1_txtCfmPwd"]').send_keys(old_password)
    #     self.utils.find_element( '//*[@id="tf1_dialog"]/div[3]/input[2]').click()
    #
    #     if 'succeeded' in message:
    #         print('Admin Rights are checked and Its working fine')
    #         return True
    #     else:
    #         print('Test Case Failed')
    #         self.utils.get_dbglog()
    #         return False


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

            username = 'admin'
            set_password = 'PR@shant2301'

            logger.debug('Setting a new password')
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_Pass).send_keys(set_password)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_CfmPass).send_keys(set_password)
            self.utils.find_element(*locators.AdministrationMenu_UsersConfiguration_SaveBtn).click()

            logger.debug('Logging in with the new password')
            try:
                self.utils.find_element(*locators.LoginPage_UserName).send_keys(username)
                self.utils.find_element(*locators.LoginPage_Password).send_keys(set_password)
                self.utils.find_element(*locators.LoginPage_LoginButton).click()
            except Exception as E:
                logger.error('Login attempt failed. Using default credentials.')
                self.utils.find_element(*locators.LoginPage_UserName).send_keys('admin')
                self.utils.find_element(*locators.LoginPage_Password).send_keys('P@ssw0rd')
                self.utils.find_element(*locators.LoginPage_LoginButton).click()

            time.sleep(5)

            logger.debug('Going to the Network menu')
            self.utils.find_element(*locators.NetworkMenu).click()
            self.utils.find_element('//*[@id="tf1_network_accessPoints"]').click()

            xp_ = '//*[@id="1"]/td[1]'
            get_ap_status = self.utils.find_element(xp_).text

            edit_xpath = '//*[@id="1"]/td[2]'
            edit_ap = self.utils.find_element(edit_xpath)
            action = ActionChains(self.driver)
            action.context_click(edit_ap).perform()
            time.sleep(5)

            if get_ap_status.lower() == 'disabled':
                logger.debug('Enabling Access Point')
                self.utils.find_element('//*[@id="enableMenu"]').click()
                try:
                    # Accept the alert for connection change
                    self.driver.switch_to.alert.accept()
                    time.sleep(5)
                except Exception as E:
                    pass
            else:
                logger.debug('Disabling Access Point')
                self.utils.find_element('//*[@id="disableMenu"]').click()
                try:
                    # Accept the alert for connection change
                    self.driver.switch_to.alert.accept()
                    time.sleep(5)
                except Exception as E:
                    pass


            message = ''
            try:
                message = self.utils.find_element('//*[@id="main"]/div[6]/p').text
                logger.info(f'Message: {message}')
            except Exception as E:
                logger.error(str(E))


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
