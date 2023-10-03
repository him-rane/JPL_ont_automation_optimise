import logger_util
from Utils import Utils
import time
from logger_util import logger

class InternetConnectivity:
    def __init__(self,driver_):
        self.driver=driver_


    @staticmethod
    def ping_ipv4_from_lan_client():
        logger.info('Checking IPv4 Connectivity')
        try:
            output = Utils.cmd_line("ping google.com -4 -n 10")
            if 'time' and 'TTL' in output:
                return True
            elif ('time' not in output) and ('could not find host' in output) or ('Request timed out' in output):
                return False
        except:
            logger.error("Faild to Ping with IPv4")
            return False


    @staticmethod
    def ping_ipv6_from_lan_client():
        logger.info('Checking IPv6 Connectivity')
        try:
            output = Utils.cmd_line("ping google.com -6 -n 10")
            if 'time' in output:
                return True
            elif ('time' not in output) and ('unreachable' in output) or ('Request timed out' in output) or ('could not find' in output):
                return False
        except:
            logger.error("Faild to Ping with IPv4")
            return False

    def run_youtube(self):
        logger.info('Checking Youtube Site access from LAN Client')
        tabs = ['https://www.youtube.com/watch?v=d3zRP2mQ5s0',
                'https://www.youtube.com/watch?v=nZmO8B9rRik',
                'https://www.youtube.com/watch?v=UQbCl5Hzjp0',
                'https://www.youtube.com/watch?v=WsCCYv2adkM',
                'https://www.youtube.com/watch?v=GIF1yNwS58Q']

        url_titles = []

        for url in tabs:
            try:
                self.driver.execute_script("window.open('');")
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.get(url)
                url_titles.append(self.driver.title)
            except Exception as E:
                logger.error("Error occurred while playing YouTube")
                return False

        return True