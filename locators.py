# Menues
DashboardMenu='//*[@id="mainMenu1"]',"#mainMenu1","mainMenu1"
StatusMenu='//*[@id="mainMenu2"]','#mainMenu2',"mainMenu2"
NetworkMenu='//*[@id="mainMenu3"]',"#mainMenu3","mainMenu3"
SecurityMenu='//*[@id="mainMenu4"]',"#mainMenu4","mainMenu4"
AdministrationMenu='//*[@id="mainMenu5"]','#mainMenu5',"mainMenu5"
AdvancedMenu='//*[@id="mainMenu6"]','#mainMenu6',"mainMenu6"

SecurityMenu_FirewallSubMenu='//*[@id="tf1_security_defaultPolicy"]','#tf1_security_defaultPolicy','tf1_security_defaultPolicy'

SecurityMenu_FirewallSubMenu_IPv4FirewallRules= "//a[normalize-space()='IPv4 Firewall Rules']","div[id='main'] li:nth-child(2) a:nth-child(1)"
IPv4FirewallRules_AddNewBtn='//*[@id="main"]/div[6]/div/div[3]/input[2]',"input[title='+ Add new']"
IPv4FirewallRulesConfiguration_Service='//*[@id="tf1_selSvrName"]','#tf1_selSvrName','tf1_selSvrName'
IPv4FirewallRulesConfiguration_Action='//*[@id="tf1_selFwAction"]','#tf1_selFwAction','tf1_selFwAction'
IPv4FirewallRulesConfiguration_SaveBtn='//*[@id="tf1_dialog"]/div[3]/input[2]',"input[value='Save']"
IPv4FirewallRules_Entries='//*[@id="recordsData_info"]','#recordsData_info','recordsData_info'
IPv4FirewallRules_EditMenu='//*[@id="editMenu"]','#editMenu','editMenu'
IPv4FirewallRules_DeleteMenu="//li[@id='deleteMenu']",'#deleteMenu','deleteMenu'

SecurityMenu_FirewallSubMenu_IPv6FirewallRules='//*[@id="main"]/div[7]/ul/li[3]/a',"div[id='main'] li:nth-child(3) a:nth-child(1)"
IPv6FirewallRules_AddNewBtn='//*[@id="main"]/div[6]/div/div[3]/input[2]',"input[title='+ Add new']"
IPv6FirewallRulesConfiguration_RuleType='//*[@id="tf1_direction"]','#tf1_direction','tf1_direction'
IPv6FirewallRulesConfiguration_Service='//*[@id="tf1_selSvrName"]','#tf1_selSvrName','tf1_selSvrName'
IPv6FirewallRulesConfiguration_Action='//*[@id="tf1_selFwAction"]','#tf1_selFwAction','tf1_selFwAction'
IPv6FirewallRulesConfiguration_SaveBtn='//*[@id="tf1_dialog"]/div[3]/input[2]',"input[value='Save']"
IPv6FirewallRules_DeleteMenu="//li[@id='deleteMenu']",'#deleteMenu','deleteMenu'

IPv6FirewallRules_Entries='//*[@id="recordsData_info"]','#recordsData_info','recordsData_info'
IPv6FirewallRules_EditMenu='//*[@id="editMenu"]','#editMenu','editMenu'
# DashboardMenu

DashboardMenu_Logout_Dropdown="//p[@class='dropbtn']",'.dropbtn'
DashboardMenu_Logout_Dropdown_Logout="//div[@class='dropdown-content']",'.dropdown-content','tf1_logoutAnchor'
DashboardMenu_Logout_Dropdown_Logout_OK="//a[normalize-space()='OK']",'body > div:nth-child(1) > div:nth-child(2) > form:nth-child(6) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > a:nth-child(2)'

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
NetworkMenu_LanSubMenu="//a[@id='tf1_network_lanIPv4Config']",'#tf1_network_lanIPv4Config','tf1_network_lanIPv4Config'
LANIPv4Config_StartIP="//input[@id='tf1_dhcpStartIp']",'#tf1_dhcpStartIp','tf1_dhcpStartIp'
LANIPv4Config_EndIP="//input[@id='tf1_dhcpEndIp']",'#tf1_dhcpEndIp','tf1_dhcpEndIp'
LANIPv4Config_DomainName="//input[@id='tf1_dhcpDomainName']",'#tf1_dhcpDomainName','tf1_dhcpDomainName'
LANIPv4Config_SaveBtn="//input[@title='Save']","input[title='Save']"
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
