import csv,smtplib

message = """ Subject: Monthly OS Patch Udates -Scheduled

Good Day {name},

Please be advised that we have scheduled a mandatory Operating System patch session for the following servers:

{serverList}

Currently there are {bugCount} known bugs,{securityCount} Security Vulnerabilities."""

from_address = "some_email@digicelgroup.local"
smtpObj = smtplib.SMTP('localhost')

with open("name_of_file.csv") as file:
    reader = csv.reader(file)
    next(reader) # Skip header row
    for name,email,serverList,bugCount,securityCount in reader:
        smtpObj.sendmail(
            from_address,
            email,
            message.format(name=name,serverList=serverList,bugCount=bugCount,securityCount=securityCount),
        )