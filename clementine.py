import inspect
from datetime import datetime
from colorama import Fore, init
from functools import lru_cache
import logging
import os

init(autoreset=True)

'''logger function'''
def logger(function):

    log_directory = os.path.dirname(inspect.getfile(function))
    log_file_path = os.path.join(log_directory, "main.log")
    logging.basicConfig(level=logging.INFO, filename=log_file_path,
            format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    '''
    wrapper function, takes parameters of the function with args and kwargs
    cache annotation "@lru_cache" specifies maximum number of the entries the cache can hold (performance reasons)
    '''
    @lru_cache(maxsize=128)
    def wrapper(*args, **kwargs):

        '''get name of the file'''
        file = __file__.split('\\')[-1]

        '''get name of the function'''
        called_function = function.__name__

        '''extract name and value of the arguments'''
        argument_names = list(inspect.signature(function).parameters.keys())
        argument_values = list(args) + list(kwargs.values())

        '''creating a list in this style: 'name=value: type' '''
        argument_info = [f"{name}={value}:{type(value).__name__}" for name, value in zip(argument_names, argument_values)]

        '''connecting the argument information to a string'''
        argument_str = ', '.join(argument_info)

        '''calls the origin function for return value'''
        result = function(*args, **kwargs)

        '''creates the full template of the function string for output to print'''
        function_call_print=f'''{
            Fore.BLUE}{called_function}({', '
            .join([f'{Fore.LIGHTRED_EX}{name}{Fore.WHITE}={Fore.GREEN}{value}{Fore.WHITE}:{Fore.YELLOW}{type(value).__name__}' 
            for name, value in zip(argument_names, argument_values)])
            }{Fore.BLUE})'''
        
        '''creates the full template of the function string for log file'''
        function_call_log=f'''{
            called_function}({', '
            .join([f'{name}={value}:{type(value).__name__}' 
            for name, value in zip(argument_names, argument_values)])
            })'''
        
        '''output of the log'''
        print(f"[{datetime.now().strftime('%d.%m.%y %H:%M:%S')}][{file}] {function_call_print}")

        '''output of the return value'''
        print(f"[{datetime.now().strftime('%d.%m.%y %H:%M:%S')}][{file}] {Fore.BLUE}{called_function} -> {Fore.GREEN}{result}" if result is not None else
              f"[{datetime.now().strftime('%d.%m.%y %H:%M:%S')}][{file}] {Fore.BLUE}{called_function} -> {Fore.BLUE}{result}")

        logging.info(f"[{file}] {function_call_log}")
        logging.info(f"[{file}] {called_function} -> {result}")

        return result

    return wrapper