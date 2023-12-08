import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

import Inputs
from logger_util import logger
from _datetime import datetime

from Utils import Utils
from login import login
from device_health import device_health
class acs:
    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils(driver)
        self.login = login(driver)
        self.device_health = device_health(driver)

    def downgrade_parameter_disable(self):
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
        if downgrade_parameter == '1':
            print('Downgrade parameter is 1')
            self.driver.switch_to.default_content()
            time.sleep(2)
            self.driver.switch_to.frame("frmButtons")
            time.sleep(2)
            self.driver.find_element(By.ID, "UcDeviceSettingsControls1_btnChange_btn").click()
            time.sleep(2)
            self.driver.switch_to.default_content()
            time.sleep(2)
            self.driver.switch_to.frame("frmDesktop")
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="tblParamsTable"]/tbody/tr[' + str(i) + ']/td[2]/input').clear()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="tblParamsTable"]/tbody/tr[' + str(i) + ']/td[2]/input').send_keys(
                '0')
            time.sleep(2)
            # self.driver.find_element(By.XPATH, '//*[@id="tblParamsTable"]/tbody/tr[14]/td[2]/input').clear()
            # time.sleep(2)
            # a = datetime.now()
            # b = datetime.date(a)
            # self.driver.find_element(By.XPATH, '//*[@id="tblParamsTable"]/tbody/tr[14]/td[2]/input').send_keys(str(b) + 'T23:59:00.000000+05:30')
            # time.sleep(2)
            self.driver.switch_to.default_content()
            time.sleep(2)
            self.driver.switch_to.frame("frmButtons")
            time.sleep(2)
            self.driver.find_element(By.ID, 'UcDeviceSettingsControls1_btnSendUpdate_btn').click()
            alert = self.driver.switch_to.alert
            alert.accept()
            time.sleep(2)
            self.driver.switch_to.default_content()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="btnAlertOk_btn"]').click()
            print('Pushed Downgrade Enable parameter as 0, waiting 60 seconds')
            time.sleep(60)
            self.driver.switch_to.frame("frmDesktop")
            check = self.driver.find_element(By.XPATH,
                                        '/html/body/form/div[4]/table/tbody/tr/td[2]/span/table/tbody/tr[2]/td/div/table/tbody/tr[' + str(
                                            i) + ']/td[2]').text
            print(check)
            try:
                assert check == '0'
                print('Downgrade parameter disabled')
            except:
                print('Downgrade parameter did not get disabled')
        else:
            print('Downgrade parameter already in disable state')
