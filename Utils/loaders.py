import os, sys
from pkgutil import iter_modules, importlib
from inspect import getmembers
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from CoreLib.AbsHandler import AbsHandler
from importlib.util  import spec_from_file_location, module_from_spec

def load_handlers(path_to_folder, abs_class = AbsHandler):
    items_in = os.listdir(path_to_folder)
    hanlders_folders = [ ]
    for f in items_in:
        f_path = os.path.join(path_to_folder, f)
        if os.path.isdir(f_path) and "__" not in f: hanlders_folders.append(f_path)
    
    installed_handlers={}
    for (importer, modname, ispkg) in iter_modules(hanlders_folders):
        mod = importer.find_module(modname).load_module(modname)
        for member_name, member in getmembers(mod):
            if member_name.startswith('__'): continue
            if isinstance(member, type) and issubclass(member, abs_class) and not member==AbsHandler:
                installed_handlers[member_name] = member()

    return installed_handlers

def load_module(module_name, module_abs_path, abs_class = AbsHandler):
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, module_abs_path)
    imp_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(imp_module)
    from inspect import getmembers, isclass
    for member_name, member in getmembers(imp_module):
        if isinstance(member, type) and issubclass(member, abs_class) and not member==AbsHandler:
            return member()


if __name__ == "__main__":
    while True:
        try:
            handling_params_string = input("Enter the folder: ")
            if handling_params_string=="quit" or handling_params_string=="q": break
            print(handling_params_string)
            hs = load_handlers(handling_params_string)
            print(hs)
        except  Exception as ex:
            print("Exception happened: " + ex.__str__())
        except:
            print("Fatal exception")