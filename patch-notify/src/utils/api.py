import sys
from requests import get
from requests.auth import HTTPBasicAuth
from json import load

ROUTES = {
    "all_hosts": 'api/hosts?per_page=all',
    "host_collections": '/katello/api/host_collections'
}

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
    response = get(url, verify=False)

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
    response = get(url, auth=authobject, verify=False)

    if response.status_code == 200:
        data = response.json()
    else:
        data = {}
    
    return data

def simulate_api_call(path: str = ""):
    with open(path, "r") as file:
        data = load(file)
    return data


def retrieve_hosts(context: dict={}):
    """
        Name: 
        
        retrieve_hosts
        
        Desc: 

        Function to make a GET request to the application instance to retrieve
        data about all the hosts stored. 

        Returns:

        Dictionary with Data
    """ 

    hosts_api_url = context['BASE_API_URL'] + ROUTES['all_hosts']

    host_data = get_data_basic_auth(hosts_api_url,context['USER'],context['TOKEN'])

    if host_data == {}:
        print("Unable to retrieve hosts information from API. Please try again next time")
        sys.exit()

    return host_data

def retrieve_host_collections(context: dict={}):
    """
        Name: 
        
        retrieve_host_collections
        
        Desc: 

        Function to make a GET request to the application instance to retrieve
        data about all the host_collections stored.

        Returns:

        Dictionary with Data
    """ 

    host_coll_api_url = context['BASE_API_URL'] + ROUTES['host_collections']

    host_coll_data = get_data_basic_auth(host_coll_api_url,context['USER'],context['TOKEN'])

    if host_coll_data == {}:
        print("Unable to retrieve host collections information from API. Please try again next time")
        sys.exit()

    host_collections = []

    for i in range(1, host_coll_data["total"]+1):

        new_url = host_coll_api_url + f'/{i}'

        host_coll = get_data_basic_auth(new_url,context['USER'],context['TOKEN'])

        if host_coll == {}:
            print("Unable to retrieve host collection information from API. Please try again next time")
            sys.exit()

        host_collections.append(host_coll)

    if host_collections == []:
        print("Unable to retrieve host collections information from API. Please try again next time")
        sys.exit()

    return { "host_collections": host_collections  }