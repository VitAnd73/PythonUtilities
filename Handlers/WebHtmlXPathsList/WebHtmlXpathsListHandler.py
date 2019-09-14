import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from shlex import split
import argparse
from CoreLib.AbsHandler import AbsHandler
from time import sleep
from datetime import datetime
from time import sleep
from random import randint
import requests
from lxml import html
import pandas as pd
import numpy as np

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class WebHtmlXpathsListHandler(AbsHandler):
    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(description="Download static html from a designated address and extract required info")
        self.arg_parser.add_argument("infilepath", type=str, help="the path to output file")
        self.arg_parser.add_argument("--outfilepath", type=str, help="the path to output file")
        super().__init__()
    def get_name(self):
        return "WebHtmlXpathsListHandler"
    def get_description(self):
        return "Requests HTML from a list of web-address and gets elements specified by the XPATHs for the adresses!" + "\n" + self.get_description_from_argparser(self.arg_parser)
    def handle(self, handling_params_string):
        args_input = self.get_args_from_params_string(handling_params_string, self.arg_parser)
        #reading data from file
        df = pd.read_csv(args_input.infilepath, index_col=0)
        self.publish_info(f"Read the data from file {args_input.infilepath}!")

        #helper function to map provided values
        def get_elem_from_web_at_xpath(web_address):
            #getting the page from the designated web-address
            page = requests.get(web_address, headers=headers)
            page.raise_for_status()
            tree = html.fromstring(page.content)

            def get_elem_at_xpath(elem_xpath):
                res_elems = tree.xpath(elem_xpath)
                res_elem = res_elems[0] if len(res_elems)>0 else None
                return res_elem
            return get_elem_at_xpath

        #creating final result
        res_df = pd.DataFrame(columns=df.columns)
        for row in df.iterrows():
            index, data = row
            if self.is_running:
                try:
                    cur_mapper = get_elem_from_web_at_xpath(index)
                    cur_data = data.map(cur_mapper, na_action='ignore')
                    self.publish_info(f"Parsed @{index}: {', '.join(str(v) for v in list(cur_data))}")
                    res_df = res_df.append(cur_data)
                    sleep(randint(5, 15))

                except:
                    e = sys.exc_info()[0]
                    self.publish_info(f"Error while handling address {index}  - {e}")
            else:
                return "Stopped!"

        if args_input.outfilepath and self.is_running and res_df.shape[0]>0:
            res_df.to_csv(args_input.outfilepath, sep=',', index=True, encoding='utf-8')

        return(f'Finished!')


if __name__ == "__main__":
    WebHtmlXpathsListHandler().handle_sysragv(sys.argv)
