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
    
    return { 'results': hosts_list }

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
        elif record['Asset Name'] not in HOST_MAP:
            continue

        index = HOST_MAP[record["Asset Name"]]
        hosts['results'][index]["additional_contacts"] = record["Additional Contacts"]
        hosts['results'][index]["owner"] = record["Business Owner"]
        hosts['results'][index]["owner_email"] = record["Manager Email Address"]
        hosts['results'][index]["presentation_name"] = record["Host Name"]
        hosts['results'][index]["ip_address"] = record["IP Address"]
    
    return hosts 

def add_patching_dates(data: dict={}, date_map: dict={}):
    """
    """
    MAP = {
        1: '2nd Thu',
        2: '3rd Tue',
        3: '2nd Thu',
        4: '2nd Thu',
        5: 'TBD',
        6: '3rd Thu',
        7: '4th Tue',
        8: '4th Thu',
        9: 'Excluded',
        10: 'Excluded'
    }

    for host in data['results']:
        id = host['host_collection_id']
        if id is None:
            continue
        date = MAP[id]
        host['patch_schedule'] = date
        if not date == 'TBD' and not date == 'Excluded':
            host["patch_date"] = date_map[date].strftime("%A, %b %d %Y")
        else:
            host["patch_date"] = date_map[date]

    return data

def remove_uneligible(data: dict={}, exclusion: list=[]):
    """
    """
    new_lst = []
    patch_exceptions = ['TBD', 'Excluded']
    for host in data['results']:

        if not type(host['host_collection_id']) == int:
            continue

        if host['patch_date'] in patch_exceptions:
            continue
        
        if host['security_count'] > 0:
            new_lst.append(host)
            continue
        
        if host['bugfix_count'] > 0:
            new_lst.append(host)
            continue

        if host['enhancement_count'] > 0:
            new_lst.append(host)
            continue

        if host['package_count'] > 0:
            new_lst.append(host)
            continue

    # Exclusion of Patch Dates
    if exclusion == []:
        return {'results': new_lst }
    
    final = []
    for host in new_lst:
        found = False
        for patch_schedule in exclusion:
            if host["patch_schedule"] == patch_schedule:
                found = True
        if not found:
            final.append(host)

    return {'results': final }

def extrapolate(data: dict={}, filter: str="default"):
    """
    """
    main_df =  json_to_dataframe(data['results'])
    main_df.set_index("host_id")

    if filter == "default":
        sort_by = main_df["additional_contacts"].unique()
        
        result = {}

        for contacts in sort_by:
            record = []
            for host in data["results"]:
                if host["additional_contacts"] == contacts:
                    record.append(host)
            result[contacts] = record
        
        return result
    elif filter == "collection":
        sort_by = main_df["patch_schedule"].unique()

        result = {}

        for collection in sort_by:
            sample = main_df[main_df["patch_schedule"] == collection]

            sort_ls = sample["additional_contacts"].unique()

            inner_result = {}
            for contacts in sort_ls:
                record = []
                for host in data["results"]:
                    if "patch_schedule" not in host:
                        continue
                    elif host["patch_schedule"] == collection and host["additional_contacts"] == contacts:
                        record.append(host)
                inner_result[contacts] = record
            result[collection] = inner_result 
        return result    
