import logging

import Inputs
from login import login
from Utils import Utils
from logger_util import logger
class device_health:



    def __init__(self, driver_):
        self.driver = driver_
        self.utils = Utils(self.driver)
        self.login=login(self.driver)

    def health_check(self):

        self.login.webgui_login()

        logger.debug("Performing device health check...")
        fail=0

        GPON_state=self.utils.get_GPON_state();
        if "01" in GPON_state:
            logger.error("Device is not in operational state")
            fail+=1

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

        if self.utils.get_firmware_version()!=Inputs.latast_firmware:
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




