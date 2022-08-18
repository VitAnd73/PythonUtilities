from Handlers.WebHtmlXPathsList.WebHtmlXpathsListHandler import WebHtmlXpathsListHandler
from Handlers.WebHtmlXPaths.WebHtmlXpathsHandler import WebHtmlXpathsHandler
from CoreLib.DefaultHandler import DefaultHandler
from Handlers.RosridParsing.RosridParsingHandler import RosridParsingHandler

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

def try_code(args_input_str):
    if not args_input_str: return

    # wh = WebHtmlXpathsListHandler()
    # wh = WebHtmlXpathsHandler()

    # wh.start_handling(args_input_str)

    # driver.get("https://rbc.ru")
    driver.get(args_input_str)

if __name__ == "__main__":
    while True:
        try:
            handling_params_string = input("Enter the command: ")
            if handling_params_string=="quit" or handling_params_string=="q": break
            try_code(handling_params_string)
            # print(f'handling_params_string={handling_params_string}')
        except  Exception as ex:
            print("Exception happened: " + ex.__str__())
        except:
            print("Fatal exception")
        
        driver.close()
        
else:
    pass