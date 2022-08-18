import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from shlex import split
import argparse

sys.path.append(".")

from CoreLib.AbsHandler import AbsHandler
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from re import findall, search
import pandas as pd
from time import sleep
from random import randint

#region setting constants - todo move to config later
initial_url = 'https://rosrid.ru/'
searchLink_path = "/html/body/div[1]/div/header/nav/ul/li[1]/a"
search_string_input_path = "//*[@id='queryString']"
pages_summary_element_xpath = "/html/body/div[1]/div/div[5]/div[8]/div[2]/nav/ul/li[3]/em"
pages_next_element_xpath = "/html/body/div[1]/div/div[5]/div[8]/div[2]/nav/ul/li[4]/a"
links_to_results_path = "//button[contains(@onclick, 'modalRequest')]"
current_links_paths = '//button[contains(@onclick, "modalRequest")]'
#endregion setting constants


class RosridParsingHandler(AbsHandler):
    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(description="Load Rosrid data and parse it!")
        self.arg_parser.add_argument("search_string", type=str, help="the search string used for selection of the Rosrid's data")
        self.arg_parser.add_argument("--maxnumofpages", type=int, default=3, help="the maximum number of search result pages to be parsed")
        self.arg_parser.add_argument("--outfilepath", type=str, help="the path to output file, including file name with extension")
        self.list_of_links = []

        super().__init__()
    def get_name(self):
        return "ParseRosridData"
    def get_description(self):
        return "Parse data from Rosrid using a search string and other parameters:" + "\n" + self.get_description_from_argparser(self.arg_parser)

    def handle(self, handling_params_string):
        args_input = self.get_args_from_params_string(handling_params_string, self.arg_parser)
        self.init_setup()
        self.driver.get(initial_url)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, searchLink_path))
            )
            #find search panel
            searchLink = self.driver.find_element_by_xpath(searchLink_path)
            searchLink.click()
            #find search input box
            search_string_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, search_string_input_path))
            )
            pages_summary_element_old = self.driver.find_element_by_xpath(pages_summary_element_xpath)

            #enter search keywords
            search_string_input.send_keys(args_input.search_string)
            search_string_input.send_keys(Keys.ENTER)

            #locating the element with the number of pages text for the search
            WebDriverWait(self.driver, 10).until(EC.staleness_of(pages_summary_element_old))

            pages_summary_element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, pages_summary_element_xpath))
                )
            current_page = int(findall(r'\d+', pages_summary_element.text)[0])
            total_number_of_pages = int(findall(r'\d+',pages_summary_element.text)[1])
            self.publish_finish_info(f'The search returned [{total_number_of_pages}] pages in total! Starting to handle page = [{current_page}] with max number of pages = [{args_input.maxnumofpages}]')

            links_to_results= self.driver.find_elements_by_xpath(links_to_results_path)

            self.handle_found_links(links_to_results)
            current_page+=1

            while self.is_running and current_page <= total_number_of_pages and current_page <= args_input.maxnumofpages:
                try:
                    next_page_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, pages_next_element_xpath))
                    )
                    next_page_element.click()
                    current_links=WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, current_links_paths)))
                    self.handle_found_links(current_links, current_page)
                    sleep(randint(5, 15))
                except:
                    e = sys.exc_info()[0]
                    self.publish_info(f"Exception on {current_page} page - {e}")

                finally:
                    self.publish_info(f"moving to the next page = {current_page + 1}")
                    current_page+=1
            if args_input.outfilepath and self.is_running:
                self.store_info(args_input.outfilepath)
        except:
            e = sys.exc_info()[0]
            print(e)

        self.finilize_setup()
        return(f'Finished parsing data from Rosrid for search string [{args_input.search_string}]!')

    def handle_found_links(self, links_to_results, iteration_number=1):
        i=1
        self.publish_info(f"Iteration/page #{iteration_number}")
        for l in links_to_results:
            attr_value = l.get_attribute("onclick")
            link_value = search(r"modalRequest\(\'\/(.*?)\?modal=true", attr_value).group(1)
            self.publish_info("#{0:3} - {1}".format(i, link_value))
            self.list_of_links.append(link_value)
            i+=1

    def store_info(self, outfilepath):
        data = {}
        data['Found links']=self.list_of_links
        df = pd.DataFrame(data)
        df.to_csv(outfilepath, sep=',', index=False, encoding='utf-8')



    #region utils stuff for prep and finish

    def init_setup(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)

        self.driver = webdriver.Firefox(profile)
        self.driver.delete_all_cookies()

    def finilize_setup(self):
        self.driver.quit()
        self.list_of_links = []

    #endregion

if __name__ == "__main__":
    RosridParsingHandler().handle_sysragv(sys.argv)
