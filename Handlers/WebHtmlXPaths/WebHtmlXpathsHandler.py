import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from shlex import split
import argparse
from CoreLib.AbsHandler import AbsHandler
from time import sleep
from datetime import datetime
import requests
from lxml import html
import pandas as pd

class WebHtmlXpathsHandler(AbsHandler):
    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(description="Download static html from a designated address and extract required info")
        self.arg_parser.add_argument("webaddress", type=str, help="the web address")
        self.arg_parser.add_argument("--xpathstrs", nargs='*', dest='xpathstrs', required="True", help="the xpathstr to search for the elements")
        self.arg_parser.add_argument("--keepwhitespace", action = 'store_true', help="keep whitespaces (leading and trailing)")
        self.arg_parser.add_argument("--keepempty", action = 'store_true', help="keep empty records")
        self.arg_parser.add_argument("--outfilepath", type=str, help="the path to output file")
        super().__init__()
    def get_name(self):
        return "XpathFromWebStaticHTML"
    def get_description(self):
        return "Requests HTML from a designated web-address and gets elements by the specified XPATHs!" + "\n" + self.get_description_from_argparser(self.arg_parser)
    def handle(self, handling_params_string):
        args_input = self.get_args_from_params_string(handling_params_string, self.arg_parser)
        page = requests.get(args_input.webaddress)
        if page.status_code==200 and self.is_running:
            self.publish_info(f"Html retrieved from {args_input.webaddress}!")
        else:
            return "Err retrieving html!"
        tree = html.fromstring(page.content)
        data = {}
        for xps in args_input.xpathstrs:
            itms = tree.xpath(xps)
            temp_list = itms if args_input.keepwhitespace else [ itm.strip().lstrip() for itm in itms]
            data[xps] = temp_list if args_input.keepempty else list(filter(None, temp_list))
        df = pd.DataFrame(data)
        if args_input.outfilepath and self.is_running:
            self.publish_info(f"Writing results to file {args_input.outfilepath}!")
            df.to_csv(args_input.outfilepath, sep=',', index=False, encoding='utf-8')

        for index, row in df.iterrows():
            if self.is_running:
                self.publish_info(f"#{index}: " + '; '.join(row))
            else:
                return ""

        return(f'Finished retrieving data from HTML at [{args_input.webaddress}]!')


if __name__ == "__main__":
    WebHtmlXpathsHandler().handle_sysragv(sys.argv)
