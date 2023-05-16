#!/usr/bin/env python3

import sys, os
from argparse import ArgumentParser
from src.utils.api import retrieve_hosts, retrieve_host_collections
from src.utils.config import initialize_context
from src.utils.parse import reformat_structure,populate_external,csv_to_json,extrapolate,remove_uneligible,add_patching_dates
from src.utils.date import find_patch_dates
from src.utils.email import email_owners

def main():
    # Initialize Object to conduct argument handling
    parser = ArgumentParser()

    parser.add_argument('-c', '--context', help="Path to Environment Variable File")
    parser.add_argument('-f', '--filter', choices=["default", "collection"], default="default", help="Filter used for data extrapolation and email delivery")
    parser.add_argument('-d', '--dates', choices=["2nd Thu", "3rd Tue", "3rd Thu", "4th Tue", "4th Thu"], metavar="\'2nd Thu\'", nargs="+")

    args = parser.parse_args()

    if args.context:
        # # Intialize the program instance with environment variables needed for functionality
        context = initialize_context(str(args.context))
    else:
        parser.exit(1, message="Please provide the path to the environment variable files \n")

    # API Calls to the Local Application to retieve information on hosts and host collections
    hosts = retrieve_hosts(context)
    host_collections = retrieve_host_collections(context)

    # Make modification to the structure of JSON Data retrieved from the application instance 
    reformat_hosts = reformat_structure(hosts, host_collections)

    # Add information from an external data source to the JSON Data
    external_data = csv_to_json(context['TEST_FILE'])
    data = populate_external(external_data, reformat_hosts)

    # Add patch schedule information to the JSON Data
    date_map = find_patch_dates()
    data = add_patching_dates(data, date_map)

    # Remove hosts that are not eligible for patching this cycle.
    data = remove_uneligible(data)

    if args.filter:
        sep_data  = extrapolate(data, filter=args.filter)
        email_owners(context=context,data=sep_data,email_type=args.filter,patch_schedule=args.dates)
            
if __name__ == "__main__":
    main()
            
        

