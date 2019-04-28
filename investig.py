from shlex import split
import argparse
from configparser import ConfigParser
from lxml import html
import requests
import pandas as pd
from Handlers.WebHtmlXPaths.WebHtmlXpathsHandler import WebHtmlXpathsHandler
from Handlers.DefaultHandler import DefaultHandler

def try_code(args_input_str):
    if not args_input_str: return
    wh = WebHtmlXpathsHandler()
    wh.start_handling(args_input_str)
    print('Ended testing code------------------')

if __name__ == "__main__":
    while True:
        try:
            handling_params_string = input("Enter the command: ")
            if handling_params_string=="quit" or handling_params_string=="q": break
            try_code(handling_params_string)
        except  Exception as ex:
            print("Exception happened: " + ex.__str__())
        except:
            print("Fatal exception")
else:
    pass