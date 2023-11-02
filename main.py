
import setup


from selenium import webdriver

from ExcelLogger import ExcelLogger
#
from functional_smoke import functional_smoke
from login import login

setup=setup.Setup()
# setup.update_driver()
driver=setup.get_driver()
exlogger = ExcelLogger("test_results.xlsx")
login=login(driver)
login.webgui_login()

obj=functional_smoke(driver)
# obj.get_access_point_status()
obj.TC_Functional_Smoke_011_012()

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




