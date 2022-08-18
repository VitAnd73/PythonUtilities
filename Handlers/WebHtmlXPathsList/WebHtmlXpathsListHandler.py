import sys
import argparse

from CoreLib.AbsHandler import AbsHandler
from time import sleep
from time import sleep
from random import randint
import requests
from lxml import html
import pandas as pd
from itertools import zip_longest

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# splitter of the xpath and required command for getting the extracted stuff (text, attribute values, etc.)
splitter = "&&"
sleep_range_min = 1
sleep_range_max = 3

def deCFEmail(fp):
    try:
        r = int(fp[:2],16)
        email = ''.join([chr(int(fp[i:i+2], 16) ^ r) for i in range(2, len(fp), 2)])
        return email
    except (ValueError):
        pass

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
        df = pd.read_csv(args_input.infilepath, index_col=0, header=None)
        self.publish_info(f"Read the data from file {args_input.infilepath}!")

        #helper function to map provided values
        def get_elem_from_web_at_xpath(web_address):
            #getting the page from the designated web-address
            page = requests.get(web_address, headers=headers)
            page.raise_for_status()
            tree = html.fromstring(page.content)

            def get_elem_at_xpath(xpath_str):
                xpaths = xpath_str.split(splitter)
                res_elems = tree.xpath(xpaths[0])
                if len(xpaths)>1:
                    # res = [eval("e." + xpaths[1]) for e in res_elems]
                    res = [eval(xpaths[1]) for e in res_elems]
                    return res
                else:
                    return res_elems
            return get_elem_at_xpath

        #creating final result
        res_df = pd.DataFrame(columns=df.columns)
        errs = ['Err']*(res_df.shape[1]-1)

        # pylint: disable=no-member
        df.fillna('', inplace=True)
        # pylint: disable=no-member
        for row in df.iterrows():
            index, data = row
            if self.is_running:
                try:
                    cur_mapper = get_elem_from_web_at_xpath(data.iloc[0])
                    xpath_list = data.tolist()[1:]
                    # cur_data = map(cur_mapper, xpath_list)
                    cur_data = [cur_mapper(xp) for xp in xpath_list]
                    # cur_data = list(map(list, zip(*cur_data)))
                    if len(cur_data)>0:
                        cur_data = list(map(list, zip_longest(*cur_data, fillvalue=None)))
                        for r in cur_data:
                            res_df.loc[len(res_df)] = [data.iloc[0], *r]
                        self.publish_info(f"Parsed @{index} for : {data.iloc[0]}, gotten {len(cur_data)} rows!")
                    else:
                        self.publish_info(f"Error while handling address {data.iloc[0]}  - empty data")
                        res_df.loc[len(res_df)] = [data.iloc[0], *errs]
                    sleep(randint(sleep_range_min, sleep_range_max))
                except:
                    e = sys.exc_info()[0]
                    self.publish_info(f"Error while handling address {data.iloc[0]}  - {e}")
                    res_df.loc[len(res_df)] = [data.iloc[0], *errs]
                    
            else:
                if args_input.outfilepath and res_df.shape[0]>0:
                    res_df.to_csv(args_input.outfilepath, sep=',', index=True, encoding='utf-8')
                return "Stopped!"

        if args_input.outfilepath and self.is_running and res_df.shape[0]>0:
            res_df.to_csv(args_input.outfilepath, sep=',', index=True, encoding='utf-8')

        return(f'Finished!')


if __name__ == "__main__":
    WebHtmlXpathsListHandler().handle_sysragv(sys.argv)
