
import setup


from selenium import webdriver

from ExcelLogger import ExcelLogger
#
from functional_smoke import functional_smoke
setup=setup.Setup()
# setup.update_driver()
driver=setup.get_driver()
exlogger = ExcelLogger("test_results.xlsx")

obj=functional_smoke(driver)
obj.TC_Functional_Sanity_007()
# exlogger.log_result("TC_Functional_Smoke_002", obj.TC_Functional_Smoke_002())
# exlogger.log_result("TC_Functional_Smoke_003", obj.TC_Functional_Smoke_003())
# exlogger.log_result("TC_Functional_Smoke_008",obj.TC_Functional_Smoke_008())
# exlogger.log_result("TC_Functional_Smoke_009", obj.TC_Functional_Smoke_009())
# exlogger.log_result("TC_Functional_Smoke_010_1", obj.TC_Functional_Smoke_010_1())
# exlogger.log_result("obj.TC_Functional_Smoke_010_2",obj.TC_Functional_Smoke_010_2())
# exlogger.log_result("obj.TC_Functional_Smoke_018()",obj.TC_Functional_Smoke_018())
# exlogger.log_result("TC_Functional_Sanity_002_1",obj.TC_Functional_Sanity_002_1())
# exlogger.log_result("TC_Functional_Sanity_002_2",obj.TC_Functional_Sanity_002_2())
# exlogger.log_result("TC_Functional_Sanity_002_3",obj.TC_Functional_Sanity_002_3())
# exlogger.log_result("TC_Functional_Sanity_005", obj.TC_Functional_Sanity_5())
# exlogger.log_result("TC_Functional_Smoke_021", obj.TC_Functional_Smoke_021())
# # exlogger.log_result("TC_Functional_Smoke_029", obj.TC_Functional_Smoke_029())



