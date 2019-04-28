# PythonUtilities (PyTils)

This repo is for development of simple GUI tool (working name is PyTils) with a base for collection of python utilities (for web scraping, data cleaning, etc.) which can be **run in async mode thus allowing to display progress and cancellation**. The tool is just for easier development and use of separate tools in manually-driven settings (i.e. not for batch-work/schedules, etc.). Besides using the tools via GUI, it can also be for command-line use of separate utilities as well.

Overall, the development of the tool has been inspired by a great book ["Automate the Boring Stuff with Python"](https://automatetheboringstuff.com). While learning python and solving practical tasks in day-to-day boring life-stuff, the concept of the tool emerged as a simple solution to handle development and maintanance of the code. The code is supposed to live and evolve and so, ***THE TOOL IS NOT INTENDED FOR END-USERS, BUT MAY BE USEFUL TO "CODUSERS"*** :relaxed: - those who practically use code to solve tasks not related to code/coding itself. I.e. not professioninal programmers who can use various repositories, package managers, etc. but also not simple users who do not know how to change code or config files.

## Use of the tool

The tool may be used to run components in GUI or in command line mode.

### GUI

The file main_window.py may be run to start the GUI application, which allows to dynamically load available components (also called handlers) with parameters passed in as a string. The components report progress in a dedicated text-box. Async execution of handlers allows stopping execution by the handlers at any time ***BUT AS INTENTED BY THE COMPONENT*** - i.e. the executing component is notified of the cancellation request, but it is up to the component to the component to actually stop work! There's no built-in termination of the async process!

![General GUI view](Assets/GUI_general.png)

### Command line mode

The components can be run in command line mode via starting file [investig.py](investig.py) with directly calling the necessary component in the main loop:
![Investig command line view](Assets/Investig_example.png)

Alternatively, component can be run by interpreter directly (__main__):
![Run main from command line view](Assets/Main_example.png)

## Components

The components can be developed independently and placed into a separate folders (relative path to them must be set in config file), from which they are loaded dynamically (at run time). The components must be in subfolders (one component per subfolder) and inherit from [the abstract base class AbsHandler.py](CoreLib/AbsHandler.py). In the current version, the folder for the components is called ["Handlers"](Handlers) (path to it may be changed in the [config file](settings.config)) and besides [Default handler](Handlers/DefaultHandler.py), it also contains folders for various components (for now it is just one component for extracting data via XPATH from static HTML web-sites - [WebHtmlXPaths](Handlers/WebHtmlXPaths)).

## Similar tools and frameworks

This PyTils tool is in no way a substitute for already existing great frameworks and tools which may be quite useful for practical tasks related to automation and utilities. Particularly, the tool may be used/integrated with the following:

- [Luigi](https://github.com/spotify/luigi) - a Python module that helps to build complex pipelines of batch jobs. As of the current version, the PyTils' components can not be used directly with Luigi - some development/customization is required. Particularly, the components can not be run as Tasks without modification ([see Luigi docs for details](https://luigi.readthedocs.io/en/stable/tasks.html)). It is possible that in later versions of PyTils support for automatic run (or conversion) of components to Luigi's tasks may be added.
- [Gooey](https://github.com/chriskiehl/Gooey) - a tool to turn (almost) any Python command line program into a full GUI application with one line. This Gooey tool is great for easy convertion of ***existing command-line stuff*** :construction_worker: by very little modification of the code (actually - adding couple decorators and writing some regex - [see for details and examples](https://github.com/chriskiehl/Gooey#how-does-it-work)). PyTils is for ***development of components from scratch*** in a way so that they could be run both in command line mode and in GUI.