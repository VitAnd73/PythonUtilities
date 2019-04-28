from abc import ABC, abstractmethod, abstractproperty
import os, sys
from shlex import split
import argparse
from re import sub as substitute

class AbsHandler(ABC):
    def __init__(self, info_handler = None, finish_handler = None, handling_params_string : str = None, handle_immediately : bool = False) -> None:
        self.is_running = False
        self.set_notifications(info_handler, finish_handler)
        if handle_immediately:
            self.start_handling(handling_params_string)

    def set_notifications(self, info_handler = None, finish_handler = None) -> None:
        self.publish_info = info_handler if info_handler else print
        self.publish_finish_info = finish_handler if finish_handler else print

    def start_handling(self, handling_params_string) -> None:
        self.is_running = True
        r = self.handle(handling_params_string)
        if self.is_running:
            self.publish_finish_info(' '.join(["Done!", r]))
            self.is_running = False

    def stop_handling(self) -> None:
        if self.is_running:
            self.is_running = False

    def handle_sysragv(self, sys_input_params):
        handling_params_string = ' '.join(sys.argv) if (sys.argv) else  None
        self.start_handling(handling_params_string)

    def get_args_from_params_string(self, handling_params_string, argparser):
        params = split(handling_params_string)
        args = argparser.parse_args(params)
        return args

    def get_description_from_argparser(self, argparser):
        command_description = substitute(r'^usage.*-h', r'[-h', argparser.format_usage())
        return command_description

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def handle(self, handling_params_string) -> str:
        pass
