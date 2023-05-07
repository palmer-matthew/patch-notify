import sys
from src.utils.api import get_data_basic_auth
from src.utils.config import load_env_as_dict

def initialize_context(path : str=None):
    env = load_env_as_dict(path)
    if env == {}:
        print("Environment Variables file is empty or it cannot be located")
        sys.exit()
    return env

def retrieve_hosts(context: dict={}):
    hosts_api_url = context['BASE_API_URL'] + 'api/hosts?per_page=all'
    host_data = get_data_basic_auth(hosts_api_url,context['USER'],context['PASSWD'])
    if host_data == {}:
        print("Unable to retrieve hosts information from API. Please try again next time")
        sys.exit()
    return host_data

def retrieve_host_collections(context: dict={}):
    host_coll_api_url = context['BASE_API_URL'] + '/katello/api/host_collections'
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


if __name__ == "__main__":
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
            
        

