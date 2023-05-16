import sys
from dotenv import dotenv_values, load_dotenv


def load_env_as_dict(path: str=None):
    """
        Name: 
        
        load_env_as_dict 
        
        Desc: 

        Function to load the environment varibles from a specified path. 
        It defaults to the current working directory if no path is specified.
        If the .env cannot be found or cannot be loaded, the function will return
        an empty dictionary.

        Returns:

        Dictionary with Values || Empty Dictionary
    """
    if path is None:
        path = ".env"
    try:
        config = dotenv_values(path)
    except:
        config = {}
    return config


def load_env(path: str=None):
    """
        Name: 
        
        load_env
        
        Desc: 

        Function to load the environment varibles from .env into the environment. 

    """
    if path is None:
        path = ".env"
    try:
        load_dotenv(dotenv_path=path)
    except:
        pass


def initialize_context(path : str=None):
    """
        Name: 
        
        intialize_context
        
        Desc: 

        Function to establish the context. Returns the ENV  variables needed for function
        as a dictionary.

        Returns:

        Dictionary with Data
    """ 

    env = load_env_as_dict(path)
    
    if env == {}:
        print("Environment Variables file is empty or it cannot be located")
        sys.exit()
    
    return env

