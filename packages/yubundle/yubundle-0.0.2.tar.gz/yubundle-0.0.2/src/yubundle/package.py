import importlib.util
import sys

def check_package(name: str) -> bool:
    if name in sys.modules:
        return True
    elif (spec := importlib.util.find_spec(name)) is not None:
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return True
    else:
        return False