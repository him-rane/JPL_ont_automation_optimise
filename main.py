import time

from selenium.webdriver.common.by import By

import Inputs
import setup
from acs_functions import acs
from device_health import device_health

from selenium import webdriver

from ExcelLogger import ExcelLogger
#
from functional_smoke import functional_smoke
from Utils import Utils
from login import login
setup=setup.Setup()
# setup.update_driver()

driver=setup.get_driver()
# device_health = device_health(driver)
# device_health.health_check()
# device_health.health_check_acs()

# exlogger = ExcelLogger("test_results.xlsx")
# login=login(driver)
# login.webgui_login()
# acs=acs(driver)
# acs.health_check_acs()
# driver.switch_to.window(driver.window_handles[0])


# login.webgui_login()

# obj=functional_smoke(driver)
# urls = [
#         'https://www.onlinesbi.sbi',
#         'https://www.facebook.com']
# print(obj.TC_Functional_Sanity_002_1())
# print(obj.TC_Functional_Sanity_002_2())
# print(obj.TC_Functional_Sanity_002_3())
# login.webgui_login()
# obj.change_firmware(Inputs.upgrade_image,Inputs.upgrade_sign)
# utils = Utils(driver)
# utils.ping_ipv4_from_lan_client()
# utils.ping_ipv6_from_lan_client()
#
# utils.search_gui('Port Forwarding')
# time.sleep(2)
# entries=utils.find_element("//div[@id='recordsData_info']",'#recordsData_info','recordsData_info').text
# print(entries)
#
# if "1" in entries:
#     print("port forward rule NOT removed after factory reset")
#
# else:
#     print("port forward rule removed after factory reset")


# obj.TC_Functional_Smoke_29_30()
# obj.TC_Functional_Smoke_32()
# obj.TC_Functional_Smoke_33()
# obj.TC_Functional_Smoke_37()
# obj.TC_Functional_Smoke_39()
# obj.TC_Functional_Smoke_40()
# obj.TC_Functional_Smoke_40()
# obj.TC_Functional_Smoke_41()
# obj.TC_Functional_Smoke_42()
# obj.TC_Functional_Sanity_46()
# obj.TC_Functional_Smoke_10()
# obj.TC_Functional_Smoke_12_47()
# obj.TC_Functional_Sanity_56()
# obj.TC_Functional_Smoke_57()









# exlogger.log_result("TC_Functional_Smoke_4", obj.TC_Functional_Smoke_4())
# exlogger.log_result("TC_Functional_Sanity_5", obj.TC_Functional_Sanity_5())
# exlogger.log_result("TC_Finctional_Smoke_9",obj.TC_Finctional_Smoke_9())
# exlogger.log_result("TC_Functional_Smoke_10", obj.TC_Functional_Smoke_10())
# exlogger.log_result("TC_Functional_Smoke_26", obj.TC_Functional_Smoke_26())
# exlogger.log_result("obj.TC_Functional_Smoke_27",obj.TC_Functional_Smoke_27())
# exlogger.log_result("obj.TC_Functional_Smoke_28_1()",obj.TC_Functional_Smoke_28_1())
# exlogger.log_result("TC_Functional_Smoke_28_2",obj.TC_Functional_Smoke_28_2())
# exlogger.log_result("TC_Functional_Smoke_32",obj.TC_Functional_Smoke_32())
# exlogger.log_result("TC_Functional_Smoke_39",obj.TC_Functional_Smoke_39())
# exlogger.log_result("TC_Functional_Sanity_005", obj.TC_Functional_Sanity_002_1())
# exlogger.log_result("TC_Functional_Smoke_021", obj.TC_Functional_Sanity_002_2())
# exlogger.log_result("TC_Functional_Smoke_029", obj.TC_Functional_Sanity_002_3())
# exlogger.log_result("TC_Functional_Sanity_002_3",obj.TC_Functional_Smoke_021())
# exlogger.log_result("TC_Functional_Sanity_005", obj.TC_Functional_Smoke_029())
# exlogger.log_result("TC_Functional_Smoke_021", obj.TC_Functional_Sanity_007())
# # exlogger.log_result("TC_Functional_Smoke_029", obj.TC_Functional_Sanity_55())









