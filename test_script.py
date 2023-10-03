import os
import subprocess
import time
import webbrowser

from selenium import  webdriver

#function to check if wifi is connected or not
def is_wifi_connected():
    try:
        result=subprocess.run(['netsh','interface','show','interface'],capture_output=True,text=True)
        output=result.stdout
        return 'Wireless' in output
    except Exception as e:
        print("Error while checking Wifi status : {e}")
        return  False

#Function for Disaabling  Wi-Fi
def enable_wifi():
    os.system("netsh interface set interface 'Wi-fi' admin=enable")

def disable_wifi():
    os.system("netsh interface set interface 'Wi-fi' admin=disable")


def run_traffic_script(traffic_script_path):
    subprocess.Popen(["python",traffic_script_path])

