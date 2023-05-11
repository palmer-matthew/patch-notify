import sys
from src.utils.api import get_data_basic_auth, simulate_api_call
from src.utils.config import load_env_as_dict
from src.utils.parse import output_json,reformat_structure,populate_external,csv_to_json,json_to_dataframe,extrapolate,remove_uneligible,add_patching_dates
from src.utils.date import find_patch_dates

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
            # Intialize the program instance with environment variables needed for functionality
            context = initialize_context(path)

            # API Calls to the Local Application to retieve information on hosts and host collections
            hosts = retrieve_hosts(context)
            host_collections = retrieve_host_collections(context)

            # Make modification to the structure of JSON Data retrieved from the application instance 
            reformat_hosts = reformat_structure(hosts,host_collections)

            # Add information from an external data source to the JSON Data
            external_data = csv_to_json(context['DATA_FILE'])
            data = populate_external(external_data, reformat_hosts)

            # Add patch schedule information to the JSON Data
            date_map = find_patch_dates()
            data = add_patching_dates(data, date_map)

            # Remove hosts that are not eligible for patching this cycle.
            data = remove_uneligible(data)
            
            extrapolate(data, "collection")

            # Testing Puposes
            # hosts = simulate_api_call("src/data/hosts.json")
            # host_collections = simulate_api_call("src/data/host_collections.json")
            # reformat_hosts = reformat_structure(hosts,host_collections)
            # reformat_hosts = simulate_api_call("src/data/reformat_hosts.json")
            # external_data = csv_to_json(context['DATA_FILE'])
            # data = populate_external(external_data, reformat_hosts)
            # date_map = find_patch_dates()
            # data = add_patching_dates(data, date_map)
            # output_json(data, "src/data/complete_data.json")
            # data = remove_uneligible(data)
            # output_json(data, "src/data/removed.json")
            # complete_data = simulate_api_call("src/data/complete_data.json")
            # complete_data = remove_uneligible(complete_data)
            # output_json(complete_data, "src/data/removed.json")
            # extrapolate(complete_data, "collection")
            


if __name__ == "__main__":
    main()
    #pass
            
        

