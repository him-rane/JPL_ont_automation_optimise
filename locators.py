# Menues
DashboardMenu='//*[@id="mainMenu1"]',"#mainMenu1","mainMenu1"
StatusMenu='//*[@id="mainMenu2"]','#mainMenu2',"mainMenu2"
NetworkMenu='//*[@id="mainMenu3"]',"#mainMenu3","mainMenu3"
SecurityMenu='//*[@id="mainMenu4"]',"#mainMenu4","mainMenu4"
AdministrationMenu='//*[@id="mainMenu5"]','#mainMenu5',"mainMenu5"
AdvancedMenu='//*[@id="mainMenu6"]','#mainMenu6',"mainMenu6"

# DashboardMenu
DashboardMenu_Logout_Dropdown='//*[@id="main"]/div[1]/div[1]/p','.dropbtn'
DashboardMenu_Logout_Dropdown_Logout='//*[@id="tf1_logoutAnchor"]','#tf1_logoutAnchor','tf1_logoutAnchor'
DashboardMenu_Logout_Dropdown_Logout_OK='//*[@id="tf1_logOutContent"]/div/a[2]','body > div:nth-child(1) > div:nth-child(2) > form:nth-child(6) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > a:nth-child(2)'

#Administration >> Maintenance>>
AdministrationMenu_MaintenanceSubMenu='//*[@id="tf1_administration_backupRestore"]','#tf1_administration_backupRestore','tf1_administration_backupRestore'

#Administration >> User>>
AdministrationMenu_UserSubMenu= '//*[@id="tf1_administration_users"]', "#tf1_administration_users", "tf1_administration_users"

AdministrationMenu_UserSubMenu_Row1Col2='//*[@id="users2"]/td[2]',"tr[id='users2'] td:nth-child(2)"
AdministrationMenu_UserSubMenu_Row1Col1='//*[@id="users2"]/td[1]',"tr[id='users2'] td[class='gradeA sorting_1']"

AdministrationMenu_UserSubMenu_Row2Col2='//*[@id="users1"]/td[2]',"tr[id='users1'] td:nth-child(2)"
AdministrationMenu_UserSubMenu_Row2Col1='//*[@id="users1"]/td[1]',"tr[id='users1'] td[class='gradeA sorting_1']"

AdministrationMenu_AddNewUser='//*[@id="main"]/div[6]/div/div[4]/input[2]',"input[title='+ Add new']"

AdministrationMenu_UsersConfiguration_Pass='//*[@id="tf1_txtPwd"]','#tf1_txtPwd','tf1_txtPwd'
AdministrationMenu_UsersConfiguration_CfmPass='//*[@id="tf1_txtCfmPwd"]','#tf1_txtCfmPwd','tf1_txtCfmPwd'
AdministrationMenu_UsersConfiguration_ToggleBtn='//*[@id="tf1_disableGuestAccount"]','#tf1_disableGuestAccount','tf1_disableGuestAccount'
AdministrationMenu_UsersConfiguration_SaveBtn='//*[@id="tf1_dialog"]/div[3]/input[2]',"input[value='Save']"
AdministrationMenu_UsersConfiguration_Name='//*[@id="tf1_txtUserName"]','#tf1_txtUserName','tf1_txtUserName'
AdministrationMenu_UsersConfiguration_Desc='//*[@id="tf1_userDescription"]','#tf1_userDescription','tf1_userDescription'
AdministrationMenu_UsersConfiguration_TimeOut='//*[@id="tf1_loginTimeout"]','#tf1_loginTimeout','tf1_loginTimeout'




#Network Menu>>Wireless
NetworkMenu_WirelessSubMenu = "//a[@id='tf1_network_accessPoints']","#tf1_network_accessPoints","tf1_network_accessPoints"

#Login Page
LoginPage_UserName= '//*[@id="tf1_userName"]', '#tf1_userName', 'tf1_userName'
LoginPage_Password= '//*[@id="tf1_password"]', '#tf1_password', 'tf1_password'
LoginPage_LoginButton= "//button[normalize-space()='Login']", "button[title='Login']"


firmware_version_sidebar = "/html/body/div[1]/div[1]/div[2]/p[1]/span", "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > p:nth-child(1) > span:nth-child(2)"
mac_address_daseboard = '//*[@id="main"]/div[6]/div[2]/div[4]/div[3]/div[4]/p', "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(19) > div:nth-child(3) > div:nth-child(4) > div:nth-child(3) > div:nth-child(4) > p:nth-child(2)"
gpon_status_WAN_Information = '//*[@id="main"]/div[6]/div[1]/div/div[17]/p', "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(19) > div:nth-child(2) > div:nth-child(1) > div:nth-child(18) > p:nth-child(2)"
ipv4_address_daseboard = '//*[@id="main"]/div[6]/div[2]/div[4]/div[3]/div[5]/p', "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(19) > div:nth-child(3) > div:nth-child(4) > div:nth-child(3) > div:nth-child(5) > p:nth-child(2)"

ipv6_address_daseboard_1 = '//*[@id="main"]/div[6]/div[2]/div[4]/div[3]/div[7]/p[1]', 'body > div:nth-child(1) > div:nth-child(2) > div:nth-child(19) > div:nth-child(3) > div:nth-child(4) > div:nth-child(3) > div:nth-child(7) > p:nth-child(2)'
ipv6_address_daseboard_2 = '//*[@id="main"]/div[6]/div[2]/div[4]/div[3]/div[7]/p[2]', 'body > div:nth-child(1) > div:nth-child(2) > div:nth-child(19) > div:nth-child(3) > div:nth-child(4) > div:nth-child(3) > div:nth-child(7) > p:nth-child(3)'

#Administration >> Maintenance >>
# Maintenance '//*[@id="tf1_administration_backupRestore"]','#tf1_administration_backupRestore',
Maintenance_BackupReboot_RebootButton = '//*[@id="tf1_frmBackupReboot"]/div[1]/div/input', "input[title='Reboot']"
Maintenance_BackupReboot_DefaultButton = '//*[@id="tf1_frmBackupFactoryDefaultSettings"]/div[1]/div/input', "input[title='Default']"

DateTimeConfiguration_CurrentRouterTime = '//*[@id="tf1__div"]/p', "div[id='tf1__div'] p"
DateTimeConfiguration_TimeZone = '//*[@id="tf1_selTimezone"]', "#tf1_selTimezone"
DateTimeConfiguration_SaveButton = '//*[@id="tf1_frmDateAndTime"]/div[10]/input[1]', "input[title='Save']"
