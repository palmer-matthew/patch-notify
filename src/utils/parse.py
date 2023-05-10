import pandas as pd
import json

def generate_host_map(lst: list=[], key: str="host_id"):
    """
    """
    if lst == []:
        raise Exception("Please provide required arguments for host map generation")
    
    HOST_MAP = {}

    # Populate HOST_MAP
    for index, host in enumerate(lst):
        HOST_MAP[host[key]] = index
    
    return HOST_MAP

def output_json(obj: object, path: str):
    """
    """
    with open(path, "w") as file:
        file.write(json.dumps(obj, indent=4))

def csv_to_json(path: str):
    """
    """
    data_csv = pd.read_csv(path)
    
    data_json = json.loads(data_csv.to_json(orient="records"))

    return { "results": data_json }

def json_to_dataframe(lst: object):
    """
    """
    dataframe = pd.read_json(json.dumps(lst), orient='records')
    
    return dataframe


def reformat_structure(hosts: dict=None, host_coll: dict=None):
    """
    """  
    if hosts == {} or host_coll == {}:
        raise Exception("Unable to parse host and host collection data. Try again")
    
    hosts_list = []

    for host in hosts["results"]:

        # Skipping records for hosts that are not attached to a content view
        if "content_facet_attributes" not in host:
            continue

        host_format = {}

        # Gather the required data from the hosts JSON data
        host_format["host_id"] = host["id"]
        host_format["hostname"] = host["name"]
        host_format["ip_address"] = host["ip"]
        host_format["location"] = host["location_name"]
        host_format["model"] = host["model_name"]
        host_format["owner"] = host["owner_name"]
        host_format["os"] = host["operatingsystem_name"]
        host_format["lifecycle_environment"] = host["content_facet_attributes"]["lifecycle_environment"]["name"]
        host_format["security_count"] = host["content_facet_attributes"]["errata_counts"]["security"]
        host_format["bugfix_count"] = host["content_facet_attributes"]["errata_counts"]["bugfix"]
        host_format["enhancement_count"] = host["content_facet_attributes"]["errata_counts"]["enhancement"]
        host_format["package_count"] = host["content_facet_attributes"]["upgradable_package_count"]
        host_format["host_collection"] = None
        host_format["host_collection_id"] = None
        host_format["additional_contacts"] = None
        host_format["owner_email"] = None
        host_format["presentation_name"] = None
        
        hosts_list.append(host_format)
    
    # Sort the list based on ID

    hosts_list = sorted(hosts_list, key=lambda item: item["host_id"])

    HOST_MAP = generate_host_map(hosts_list)

    # Populate the Hosts with Correct Host Collection Information
    for collection in host_coll["host_collections"]:
        for host_id in collection["host_ids"]:
            hosts_list[HOST_MAP[host_id]]["host_collection"] = collection["name"]
            hosts_list[HOST_MAP[host_id]]["host_collection_id"] = collection["id"]
    
    return hosts_list

def populate_external(data: dict=None, hosts: list=[]):
    """
    """
    if hosts == []:
        raise Exception("Unable to parse host and host collection data. Try again")
    
    if data == {}:
        raise Exception("Unable to data from csv. Try again")
    
    HOST_MAP = generate_host_map(hosts['results'], "hostname")

    for record in data['results']:

        if record['Asset Name'] == "Not Onboarded":
            continue

        index = HOST_MAP[record["Asset Name"]]
        hosts['results'][index]["additional_contacts"] = record["Additional Contacts"]
        hosts['results'][index]["owner"] = record["Business Owner"]
        hosts['results'][index]["owner_email"] = record["Email Address"]
        hosts['results'][index]["presentation_name"] = record["Host Name"]
        hosts['results'][index]["ip_address"] = record["IP Address"]
    
    return hosts 

def extrapolate(data: dict={}, filter: str="default"):
    """
    """
    main_df =  json_to_dataframe(data['results'])

    if filter == "default":
        sort_by = main_df["additional_contacts"].unique()
        
        result = {}

        for contacts in sort_by:
            result[contacts] = main_df[main_df["additional_contacts"] == contacts].sort_values(by="host_collection")
        
        return result
    elif filter == "collection":
        sort_by = main_df["host_collection"].unique()

        result = {}

        for collection in sort_by:
            sample = main_df[main_df["host_collection"] == collection]

            sort_ls = sample["additional_contacts"].unique()

            inner_result = {}

            for contacts in sort_ls:
                inner_result[contacts] = sample[sample["additional_contacts"] == contacts]

            result[collection] = inner_result 
            
        return result

"""
TODO:

- Write a function / functions to perform sorting and extrapolation of data needed for each email

The Objective: Once we have the data in the format we want it, it needs to be sorted based on Host Collection or By Owner
so we can send emails with customized information to that particular business owner. Also we do have to consider 
servers that have no patches applicable as well as issues with subscriptions that presents variables.
"""


# Testing Purposes
# from api import simulate_api_call
# host_collection = simulate_api_call('../json-foreman/host_collection.json')
# hosts_data = simulate_api_call('../json-foreman/hosts.json')
# reformat_structure(hosts_data,host_collection)
# items_to_display=["host_id", "hostname" , "ip_address","location", "model", "owner", "os", "lifecycle_environment", \
#            "security_count", "bugfix_count", "enhancement_count", "package_up_count", "host_collection", "host_collection_id", \
#            "additional_contacts", "owner_email", "presentation_name"]
# result[contacts] = main_df[main_df["additional_contacts"] == contacts].filter(items=['hostname', "additional_contacts", "host_collection"]).sort_values(by="host_collection")

        