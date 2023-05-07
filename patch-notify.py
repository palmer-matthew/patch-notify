import sys
from src.utils.api import get_data_basic_auth
from src.utils.config import load_env_as_dict

ROUTES = {
    "all_hosts": 'api/hosts?per_page=all',
    "host_collections": '/katello/api/host_collections'
}

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

    host_data = get_data_basic_auth(hosts_api_url,context['USER'],context['PASSWD'])

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

    host_coll_data = get_data_basic_auth(host_coll_api_url,context['USER'],context['PASSWD'])

    if host_coll_data == {}:
        print("Unable to retrieve host collections information from API. Please try again next time")
        sys.exit()

    host_collections = []

    for i in range(host_coll_data["total"]):

        new_url = host_coll_api_url + f'/{i}'

        host_coll = get_data_basic_auth(new_url,context['USER'],context['PASSWD'])

        if host_coll == {}:
            print("Unable to retrieve host collection information from API. Please try again next time")
            sys.exit()

        host_collections.append(host_coll)

    if host_collections == []:
        print("Unable to retrieve host collections information from API. Please try again next time")
        sys.exit()

    return { "host_collections": host_collections  }

def display_help():
    pass

def main():
    if len(sys.argv) == 1:
        display_help()
        sys.exit()
    else:
        for index, arg in enumerate(sys.argv[1:]):
            if arg == "-e":
                path = sys.argv[index + 2]
        if path is None:
            print("Please provide the path to the environment variables file")
            sys.exit()
        else:
            context = initialize_context(path)
            hosts = retrieve_hosts(context)
            host_collections = retrieve_host_collections(context)


if __name__ == "__main__":
    #main()
    pass
            
        

