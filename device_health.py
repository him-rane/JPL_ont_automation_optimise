import logging

from selenium.webdriver.common.by import By

import Inputs
from login import login
from Utils import Utils
from logger_util import logger
import time
from _datetime import datetime
class device_health:



    def __init__(self, driver_):
        self.driver = driver_
        self.utils = Utils(self.driver)
        self.login=login(self.driver)

    def health_check(self):

        self.login.webgui_login()

        logger.debug("Performing device health check")
        fail=0

        GPON_state = self.utils.get_GPON_state()
        if ("05" not in str(GPON_state)) and ("O5" not in str(GPON_state)):
            logger.error("Device is not in operational state")
            fail += 1

        ipv4 = self.utils.get_ipv4()
        if "0.0.0.0" in ipv4:
            logger.error("Device has not received WAN IPv4 Address")
            fail += 1

        if self.utils.get_ipv6()==-1:
            logger.error("Device has not received WAN IPv6 Address")
            fail+=1

        if "1015" not in self.utils.get_wan_port():
            logger.error("WAN port is NOT 1015")
            fail += 1

        if self.utils.get_firmware_version()!=Inputs.latest_firmware:
            logger.error("Device is not having latest firmware")
            fail += 1
        # if self.utils.website_check()==False:
        #     logger.error("Error occurred while accessing internet")
        #     fail += 1

        if self.utils.ping_ipv4_from_lan_client()==False:
            logger.error("Unable to ping google with IPv4")

        if self.utils.ping_ipv6_from_lan_client() == False:
            logger.error("Unable to ping google with IPv6")

        if fail != 0:
            logger.warning("Device health check completed with %d issues.", fail)
            return False
        else:
            logger.info("Device health check completed successfully.")
            return True

    def time_date_conversion(self,my_time):
        time_date_value = datetime.strptime(my_time, '%m/%d/%Y %H:%M:%S')
        return time_date_value


    def get_last_connection_time(self):
        element = self.utils.find_element('//*[@id="tblDeviceInfo"]/tbody/tr[11]/td[2]',
                                          'tbody tr:nth-child(10) td:nth-child(2) span:nth-child(1)').text

        return self.time_date_conversion(element)

    def health_check_acs(self):
        logger.debug("Performing device ACS health check")
        try:
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.login.acs_login()

            old_time=self.get_last_connection_time()
            logger.info(f"Old Connection Time - {old_time}")
            time.sleep(30)

            for number in range(5):
                self.utils.find_element('//*[@id="btnReCheck_btn"]','#btnReCheck_btn').click()
                time.sleep(30)
                new_time=self.get_last_connection_time()
                logger.info(f"New Connection Time - {new_time}")
                if new_time > old_time:
                    logger.info("ONT is Online on ACS")
                    return True
                time.sleep(60)

            logger.error("ONT is offline on ACS")
            return False
        except Exception as E:
            logger.error(f"Error occurred while performing ACS health check +{E}")
            return False



