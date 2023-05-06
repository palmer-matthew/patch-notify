from dotenv import dotenv_values, load_dotenv

"""
    Name: 
    
    load_env_from_path 
    
    Desc: 

    Function to load the environment varibles from a specified path. 
    It defaults to the current working directory if no path is specified.
    If the .env cannot be found or cannot be loaded, the function will return
    an empty dictionary.

    Returns:

    Dictionary with Values || Empty Dictionary
"""
def load_env_from_path(path: str=None):
    if path is None:
        path = ".env"
    try:
        config = dotenv_values(path)
    except:
        config = {}
    return config

"""
    Name: 
    
    load_env
    
    Desc: 

    Function to load the environment varibles from .env into the environment. 

"""
def load_env(path: str=None):
    if path is None:
        path = ".env"
    try:
        load_dotenv(dotenv_path=path)
    except:
        pass