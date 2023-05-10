#!/usr/bin/env python
import pandas as pd
import numpy as np
import re

df = pd.read_csv("new_data.csv", engine="python", encoding="latin-1")

init = {
    "Asset Name": [],
    "Asset State": [],
    "Asset Type": [],
    "Asset Category": [],
    "Criticality": [],
    "Product": [],
    "Product Type": [],
    "OS Name": [],
    "IP Address": [],
    "Managed By Department": [],
    "Managed By": [],
    "Service Used For": [],
    "Market": [],
    "Location": [], 
}

for i in df.index:
    test = df.loc[i, "Location"]
    test1 = df.loc[i, "OS GROUP"]
    #if str(test1).lower() == "linux" and str(test).lower() == "jamaica":
    #if str(test1).lower() != "linux" and str(test).lower() == "jamaica":
    #if str(test1).lower() == "linux" and str(test).lower() != "jamaica":
    if str(test1).lower() != "linux" and str(test).lower() != "jamaica":
        pass
    else:
        continue
    
    #Checking Hostname
    name = str(df.loc[i, "Hostname"])
    init["Asset Name"].insert(i, name)

    init["Asset Type"].insert(i, "Asset")
    init["Asset Category"].insert(i, "IT")
    init["Product Type"].insert(i, "Server")
    
    #Checking State Column
    state = str(df.loc[i, "BACK-UP NOTE"])
    if state.lower() == "decommissioned":
        init["Asset State"].insert(i, "Decommissioned")
    else:
        init["Asset State"].insert(i, "In Store")

    #Checking IP Column
    ip = df.loc[i, "IP"]
    init["IP Address"].insert(i, ip)

    #Checking Service Name Column:
    service = df.loc[i, "Service Name"]
    init["Service Used For"].insert(i, service)


    #Checking Criticality Column
    critical = df.loc[i, "Criticality"]
    high = ["Messaging team to be contacted", "Firewall troubleshooting required", "Unreachable", "To be assessed by cloud transformation cloud for compatibility"]
    low = ["Completed", "Exists","no","n/a"]
    if type(critical) == str:
        if critical in high:
            init["Criticality"].insert(i, "High")
        elif critical in low:
            init["Criticality"].insert(i, "Low")
        else:
            init["Criticality"].insert(i, str(critical.lower().capitalize()))
    else:
        init["Criticality"].insert(i, "Low")
        
    #Checking OS Name Column
    os = str(df.loc[i, "OS"])
    init["OS Name"].insert(i, os)
    
    #Checking Sever Owner and Department Column
    dept = df.loc[i, "Server Owner Department"]
    owner = df.loc[i, "Point of Contact (User)"]
    init["Managed By"].insert(i, owner) 
    init["Managed By Department"].insert(i, dept)
    
    #Sanitizing the Location Column
    location = str(df.loc[i, "Location"])
    init["Location"].insert(i, location)
    init["Market"].insert(i, location)

    #Sanitizing the OS Group Column
    model = str(df.loc[i, "OS GROUP"])
    init["Product"].insert(i, model)

odf = pd.DataFrame(init)
#odf.to_csv("jam_linux_output.csv", index=False, encoding="utf-8")
#odf.to_csv("jam_other_output.csv", index=False, encoding="utf-8")
#odf.to_csv("mia_linux_output.csv", index=False, encoding="utf-8")
odf.to_csv("mia_other_output.csv", index=False, encoding="utf-8")

#Information 
#print(np.isnan(df.loc[0, "Point of Contact (User)"]))
#print(odf)
#print(odf.loc[9, :])
#print(df.head())
#print(odf.head())
#print(f"Length of Original Dataframe: {len(df.index)}, Length of Transposed Dataframe: {len(odf.index)}")