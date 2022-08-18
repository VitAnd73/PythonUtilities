import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import CoreLib.AbsHandler as cl

class DefaultHandler(cl.AbsHandler):
    def get_name(self) -> str:
        return "DefaultHandler"
    def get_description(self) -> str:
        return "The Default handler is only to demonstrate functionality of various modules which may be loaded from a specially designated folder (see description for more details)! Please, select appropriate handlers for your task!"
    def handle(self, handling_params_string : str) -> str:
        return handling_params_string + "The Default handler has only demonstration functionality. Please, select appropriate handler which will hanle your task and provide output (results) here."

if __name__ == "__main__":
    DefaultHandler().handle_sysragv(sys.argv)