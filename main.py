

import device_health
import internet_connectivity
import setup
from logger_util import logger
from login import login
from device_health import device_health
from Utils import  Utils
from ExcelLogger import ExcelLogger

from functional_smoke import functional_smoke

logger.warning("Test Start")




#
setup=setup.Setup()
driver=setup.get_driver()

login=login(driver)
login.webgui_login()




    # Create an instance of the ExcelLogger

# exlogger = ExcelLogger("test_results.xlsx")

    # Replace these with your actual test cases



obj=functional_smoke(driver)
# exlogger.log_result("TC_Functional_Smoke_002", obj.TC_Functional_Smoke_002())
# exlogger.log_result("TC_Functional_Smoke_003", obj.TC_Functional_Smoke_003())
# exlogger.log_result("TC_Functional_Smoke_008", obj.TC_Functional_Smoke_008())
# exlogger.log_result("TC_Functional_Smoke_003", obj.TC_Functional_Smoke_009())
# exlogger.log_result("TC_Functional_Smoke_008", obj.TC_Functional_Smoke_010_1())
# exlogger.log_result("TC_Functional_Smoke_008", obj.TC_Functional_Smoke_010_2())
# exlogger.log_result("TC_Functional_Smoke_32", obj.TC_Functional_Smoke_32())
# obj.add_firewall_rule('FTP','DROP','Outbound')
# obj.delete_firewall_rule('FTP')

obj.TC_Functional_Sanity_002_1()
obj.TC_Functional_Sanity_002_2()
obj.TC_Functional_Sanity_002_3()

# obj.ftp_check()
# obj.static_wan_configuration();



# utils=Utils(driver)
#
# login.webgui_login()
# utils.get_ipv4()
# utils.get_ipv6()






