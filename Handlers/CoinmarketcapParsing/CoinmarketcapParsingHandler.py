from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
from CoreLib.AbsHandler import AbsHandler
import random

link = list()
name = list()
GitHub = list()
Number_of_elements = 100
nolink = "No link"



class CoinmarketcapParsingHandler(AbsHandler):
    def get_name(self):
        return "Coinmarketcap parser for getting links of their github and etc."
    def get_description(self):
        return "Coinmarketcap parser"
    def handle(self, handling_params_string):
        driver = webdriver.Firefox()
        driver.get('https://coinmarketcap.com')
        i = ""
        for i in driver.find_elements_by_xpath('//a[@class="currency-name-container link-secondary"]'):
            link.append(i.get_attribute('href'))
        return "All href's in your pocket!"

        driver.get('https://coinmarketcap.com')
        i = 0
        while i < Number_of_elements:
            Coin  = driver.find_elements_by_xpath('//a[@class="currency-name-container link-secondary"]')[i].text
            name.append(Coin)
            i = i + 1
        return "Coin captured!"

        GitHublink_get = ""
        i = 0
        nolink = "No link"
        print("Starting getting GitHub links!")
        while i < Number_of_elements:
            GitHublink_get = ""
            driver.get(link[i])
            
            sleep(random.randint(6, 10))
            
            try:
                for GitHublink_get in driver.find_elements_by_xpath('//a[contains(text(),"Source Code")]'):
                    GitHublink = (GitHublink_get.get_attribute('href'))
                GitHub.append(GitHublink)
            except:
                pass
            t = i - 1
            if i > 0:
                if GitHub[t] == GitHub[i]:
                    GitHub.pop()
                    GitHub.append("No link")
                elif GitHub[t] == nolink:
                    f = 0
                    while f < t:
                        if GitHublink == GitHub[f]:
                            GitHub.pop()
                            GitHub.append("No link")
                        else:
                            pass
                        f = f + 1
                else:
                    pass
            return GitHub[i]
            i = i + 1
        return "Github link getted!"
        data = pd.DataFrame({'name': name ,'link': link, 'GitHub': GitHub})
        
        return handling_params_string + data
    
if __name__ == "__main__":
    CoinmarketcapParsingHandler().handle_sysragv(sys.argv)