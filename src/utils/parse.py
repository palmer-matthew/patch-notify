import pandas as pd
import json


def reformat_structure(hosts: dict=None, host_coll: dict=None):
    """
    """  
    hosts_list = []
    HOST_MAP = {}

    for host in hosts["results"]:

        # Skipping records for hosts that are not attached to a content view
        if "content_facet_attributes" not in host:
            continue

        host_format = {}

        # Gather the required data from the hosts JSON data
        host_format["host_id"] = host["id"]
        host_format["hostname"] = host["name"] or host["certname"]
        host_format["ip_address"] = host["ip"]
        host_format["location"] = host["location_name"]
        host_format["model"] = host["model_name"]
        host_format["owner"] = host["owner_name"]
        host_format["os"] = host["operatingsystem_name"]
        host_format["lifecycle_environment"] = host["content_facet_attributes"]["lifecycle_environment"]["name"]
        host_format["security_count"] = host["content_facet_attributes"]["errata_counts"]["security"]
        host_format["bugfix_count"] = host["content_facet_attributes"]["errata_counts"]["bugfix"]
        host_format["enhancement_count"] = host["content_facet_attributes"]["errata_counts"]["enhancement"]
        host_format["package_up_count"] = host["content_facet_attributes"]["applicable_package_count"] or host["content_facet_attributes"]["upgradable_package_count"]
        host_format["host_collection"] = None
        host_format["host_collection_id"] = None
        host_format["additional_contacts"] = None
        host_format["owner_email"] = None
        
        hosts_list.append(host_format)
    
    # Sort the list based on ID

    hosts_list = sorted(hosts_list, key=lambda item: item["host_id"])

    # Populate HOST_MAP
    for index, host in enumerate(hosts_list):
        HOST_MAP[host["host_id"]] = index

    # Populate the Hosts with Correct Host Collection Information
    for collection in host_coll["host_collections"]:
        for host_id in collection["host_ids"]:
            hosts_list[HOST_MAP[host_id]]["host_collection"] = collection["name"]
            hosts_list[HOST_MAP[host_id]]["host_collection_id"] = collection["id"]
    
    return hosts_list

    # output_json(hosts_list)

def output_json(lst):
    with open("src/utils/test.json", "w") as file:
        file.write(json.dumps({
            "results": lst
        }, indent=4))


# Testing Purposes
# from api import simulate_api_call
# host_collection = simulate_api_call('../json-foreman/host_collection.json')
# hosts_data = simulate_api_call('../json-foreman/hosts.json')
# reformat_structure(hosts_data,host_collection)

        