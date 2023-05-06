from requests import get
from requests.auth import HTTPBasicAuth

def get_data(url: str=None):
    """
        Name: 
        
        get_data
        
        Desc: 

        Function to make a GET request to the specified url 

        Returns:

        Dictionary with Data || Empty Dictionary
    """    
    # Check if the api url is empty. If it is, it will raise an exception

    if url is None:
        raise Exception("API Url has not been defined. Please provide argument")

    # Makes a GET request to the specified url 
    response = get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        data = {}
    
    return data

def get_data_basic_auth(url: str=None, username:str=None, passwd: str=None):
    """
        Name: 
        
        get_data_basic_auth
        
        Desc: 

        Function to make a GET request to the specified url with Basic Authentication
        using given username and passwd

        Returns:

        Dictionary with Data || Empty Dictionary
    """

    # Check if the username or password is empty. If it is, it will raise an exception

    if username is None or passwd is None:
        raise Exception("Username or Password has not been defined. Please provide both arguments")
    
    # Check if the api url is empty. If it is, it will raise an exception

    if url is None:
        raise Exception("API Url has not been defined. Please provide argument")

    # Creates a Basic Authentication object with specified username and password
    authobject = HTTPBasicAuth(username=username, password=passwd)

    # Makes a GET request to the specified url along with the attached Basic Auth object
    response = get(url, auth=authobject)

    if response.status_code == 200:
        data = response.json()
    else:
        data = {}
    
    return data
