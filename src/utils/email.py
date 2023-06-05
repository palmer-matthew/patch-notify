import smtplib, traceback
from email.headerregistry import Address
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pandas import DataFrame

# HTML TEMPLATES
style = """
    .link{
        color: blue;
        /* text-decoration: underline; */
    }
    body{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, Arial, sans-serif;
        background-color: #f5f5f5;
        padding: 5px 20px;
    }
    .info{
        display: block;
        font-size: 1em;
        font-weight: bold;
    }
    
    /*Table Formatting*/
    .table{
        margin: auto 0;
        font-size: 1em;
        text-align: center;
    }
    .table thead th{
        border: 1px solid black;
        background-color: #333CEB;
        padding: 7.5px;
        color: #fff;
    }

    .table tbody td{
        border: 1px solid black;
        /* background-color: #D6D8FF; */
        padding: 7.5px;
    }

    /* .table tbody tr:nth-child(2n) td{
        background-color: #fff;
    } */
"""

day_before = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html lang="en">
<head>
    <title>title</title>
    <style type="text/css">        
        {style_rulesets}
    </style>
</head>
<body>
    <div>
        <br><br> Good Day Team / Application Owner,
        <br><br> Please be advised of the following servers eligible for patching <b> tomorrow </b>:
        <br><br><b> Scheduled Time: {date_scheduled} | 8:30 PM to 7:00 AM GMT-5 [JA Time] </b>
    </div>
    <div style="margin: 20px 0px 10px 0px;">{host_table}</div>
    <div>
        <p> The patching session will proceed in 3 phases: </p>
        <ol>
            <li>Phase 1 - Patch Installation : 8:30 PM to 12:00 AM</li>
            <li>Phase 2 - Server Reboot : 12:00 AM to 3 AM</li>
            <li>Phase 3 - Service Restoration & Rollback and Recovery if necessary : 3:00 AM to 7:00 AM</li>
        </ol>
        <p> 
            Please also note the following items : 
        </p>
        <ul>
            <li>
                Installation of OS Patches <b>may require a reboot of the servers</b>. 
                If there is a preference with regards to the order in which the servers are rebooted, 
                <b> please indicate this before the reboot phase begins.</b>
            </li>
            <li>
                If there are any application services running that will need to be stopped, 
                <b>please ensure that they are stopped before 12 AM</b> and set to start again upon reboot. 
                If this is not possible, please ensure that someone is on standy to restart application services once
                the reboot is complete. 
            </li>
            <li>
                There will be a bridge available to facilitate this pacthing session and address any issues that may arise during the process.
                An invite will be sent to you before the patching session begins.
            </li>
            <li>This activity is considered BAU and priority as such if you require a CRQ for your stakeholders, you will be responsible for its creation.</li>
            <li>
                The following patch schedule will be adhered to going forward for further patch installations:
            </li>
            <table class="table" border=0 cellspacing="3" cellpadding="0">
                <thead>
                    <tr>
                        <th>Group</th>
                        <th>Day Scheduled</th>
                        <th>Server Grouping</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>P3</td>
                        <td>2nd Thursday</td>
                        <td>Patching of Test, Dev and UAT Servers</td>
                    </tr> 
                    <tr>
                        <td>P4</td>
                        <td>3rd Tuesday</td>
                        <td>Patching of Virtual Server in JA</td>
                    </tr>
                    <tr>
                        <td>P4</td>
                        <td>3rd Thursday</td>
                        <td>Patching of Virtual Servers in Miami</td>
                    </tr>
                    <tr>
                        <td>P4</td>
                        <td>4th Tuesday</td>
                        <td>Patching of Physical Servers (Caymanas Switch, DC and Headend)</td>
                    </tr>
                    <tr>
                        <td>P4</td>
                        <td>4th Thursday</td>
                        <td>Patching of Physical Servers (Downtown, Balmoral, Dumfries)</td>
                    </tr>
                </tbody>
            </table>
        </ul>
        <p>
            We kindly request that you take note of the aforementioned points and make necessary arrangements in order to ensure minimal 
            disruptions to your operations.
        </p>
    </div>
    <div class="footer">
        <br><b>Need Support ? - Send us an email at <span class="link">JAM_IT_SysAd@digicelgroup.com</span>.</b>
        <br><br> Thank you, <br><b> Group IT Infrastructure </b>
        <br><br><b>NB. This email is an automated message. Please do not reply to this email.</b>
    </div>
</body>
</html>
"""

main_notif = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html lang="en">
<head>
    <title>title</title>
    <style type="text/css">
        {style_rulesets}
    </style>
</head>
<body>
    <div class="footer">
        <br><br> Good Day Team / Application Owner,
        <br><br> Please be advised of the below schedule for <b> mandatory OS Patches </b> for the following servers: 
    </div>
    <div style="margin: 20px 0px 10px 0px;">{host_table}</div>
    <div>
        <p> The patching session will proceed in 3 phases: </p>
        <ol>
            <li>Phase 1 - Patch Installation : 8:30 PM to 12:00 AM</li>
            <li>Phase 2 - Server Reboot : 12:00 AM to 3 AM</li>
            <li>Phase 3 - Service Restoration & Rollback and Recovery if necessary : 3:00 AM to 7:00 AM</li>
        </ol>
        <p> 
            Please also note the following items : 
        </p>
        <ul>
            <li>
                Installation of OS Patches <b>may require a reboot of the servers</b>. 
                If there is a preference with regards to the order in which the servers are rebooted, 
                <b> please indicate this before the reboot phase begins.</b>
            </li>
            <li>
                If there are any application services running that will need to be stopped, 
                <b>please ensure that they are stopped before 12 AM</b> and set to start again upon reboot. 
                If this is not possible, please ensure that someone is on standy to restart application services once
                the reboot is complete. 
            </li>
            <li>
                There will be a bridge available to facilitate this pacthing session and address any issues that may arise during the process.
                An invite will be sent to you before the patching session begins.
            </li>
            <li>This activity is considered BAU and priority as such if you require a CRQ for your stakeholders, you will be responsible for its creation.</li>
            <li>
                The following patch schedule will be adhered to going forward for further patch installations:
            </li>
            <table class="table" border=0 cellspacing="3" cellpadding="0">
                <thead>
                    <tr>
                        <th>Group</th>
                        <th>Day Scheduled</th>
                        <th>Server Grouping</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>P3</td>
                        <td>2nd Thursday</td>
                        <td>Patching of Test, Dev and UAT Servers</td>
                    </tr> 
                    <tr>
                        <td>P4</td>
                        <td>3rd Tuesday</td>
                        <td>Patching of Virtual Server in JA</td>
                    </tr>
                    <tr>
                        <td>P4</td>
                        <td>3rd Thursday</td>
                        <td>Patching of Virtual Servers in Miami</td>
                    </tr>
                    <tr>
                        <td>P4</td>
                        <td>4th Tuesday</td>
                        <td>Patching of Physical Servers (Caymanas Switch, DC and Headend)</td>
                    </tr>
                    <tr>
                        <td>P4</td>
                        <td>4th Thursday</td>
                        <td>Patching of Physical Servers (Downtown, Balmoral, Dumfries)</td>
                    </tr>
                </tbody>
            </table>
        </ul>
        <p>
            We kindly request that you take note of the aforementioned points and make necessary arrangements in order to ensure minimal 
            disruptions to your operations.
        </p>
    </div>
    <div class="footer">
        <br><b>Need Support ? - Send us an email at <span class="link">JAM_IT_SysAd@digicelgroup.com</span>.</b>
        <br><br> Thank you, <br><b> Group IT Infrastructure </b>
        <br><br><b>NB. This email is an automated message. Please do not reply to this email.</b>
    </div>
</body>
</html>
"""

# TEXT TEMPLATES 
text_placeholder = "TEXT IN CASE HTML FAILS TO DISPLAY"

# FUNCTIONS
def create_SMTP_connection():
    SMTP_PORT = 25
    SMTP_SERVER = 'localhost'
    return smtplib.SMTP(SMTP_SERVER, port=SMTP_PORT)

def close_SMTP_connection(conn: smtplib.SMTP):
    conn.close()

def send_email(conn: smtplib.SMTP, sender: Address, receivers: list, cc: list, subject: str, body: str, debug=False):

    COMMASPACE = ', '

    message = MIMEMultipart("alternative")

    # Email Message Headers
    message['Subject'] = subject
    message['From'] = str(sender)
    message['To'] = COMMASPACE.join([str(i) for i in receivers])
    if not cc == []:
        message['Cc'] = COMMASPACE.join([str(i) for i in cc])
    message.attach(MIMEText(text_placeholder, "plain")) 
    message.attach(MIMEText(body, "html"))

    conn.send_message(message)

def email_owners(context: dict, data: dict={}, email_type: str="default", patch_schedule: list=["2nd Thu"]):
    server = create_SMTP_connection()
    try:
        if email_type == "default":
            keys = data.keys()
            for key in keys:
                records = data[key]
                table =  format_table(records)
                message = main_notif.format(host_table=table, style_rulesets=style)
                result = create_to_cc_receipients(context=context, records=records)
                sender = Address(context["SMTP_SENDER_NAME"], context["SMTP_USER"], context["SMTP_DOMAIN"])
                #send_email(conn=server, sender=sender, receivers=result["recs"], cc=result["cc"], subject="Monthly OS Patch Updates - Upcoming Month Schedule [DO NOT REPLY]", body=message)
        elif email_type == 'collection':
            for patch_date in patch_schedule:
                keys = data[patch_date].keys()
                sub_dict = data[patch_date]
                for key in keys:
                    records = sub_dict[key]
                    table =  format_table(records, notifcation_type=email_type)
                    date = records[0]["patch_date"]
                    message = day_before.format(host_table=table, date_scheduled=date, style_rulesets=style)
                    result = create_to_cc_receipients(context=context, records=records)
                    sender = Address(context["SMTP_SENDER_NAME"], context["SMTP_USER"], context["SMTP_DOMAIN"])
                    #send_email(conn=server, sender=sender, receivers=result["recs"], cc=result["cc"], subject="Monthly OS Patch Updates - [REMINDER - DO NOT REPLY]", body=message)
    except Exception as e:
        close_SMTP_connection(server)
        traceback.print_exc()

def create_to_cc_receipients(context: dict, records: list):
    domain = context["SMTP_DOMAIN"]
    receipients = []
    first_row = records[0]
    owner_split = first_row["owner_email"].split('@')
    add_con = first_row["additional_contacts"]
    receipients.append(Address(first_row["owner"], owner_split[0], domain=domain))
    for email in add_con.split(sep=","):
        email_split = email.split("@")
        receipients.append(Address(username=email_split[0], domain=domain))

    cc = []
    cc_1 = context["CC_1_USER"]
    cc.append(Address(' '.join(cc_1.split(sep='.')), cc_1, domain))
    cc_2 = context["CC_2_USER"]
    cc.append(Address(' '.join(cc_2.split(sep='.')), cc_2, domain))
    cc_3 = context["CC_3_USER"]
    cc.append(Address('', cc_3.split("@")[0], domain))

    # Check for similarities in cc listing
    for i in receipients:
        for j in cc:
            if i.username == j.username:
                cc.remove(j)
    
    return { "recs": receipients, "cc": cc   }

def format_table(records: list, notifcation_type = "default"):
    if notifcation_type == "default":
        tableformat = """
        <table class="table" border=0 cellspacing="3" cellpadding="0">
            <thead>
                <tr>
                    <th>Hostname</th>
                    <th>IP Address</th>
                    <th>Installable Updates - Security</th>
                    <th>Installable Updates - Bug Fixes</th>
                    <th>Installable Updates - Enhancements</th>
                    <th>Installable Packages</th>
                    <th>OS</th>
                    <th>Lifecycle Environment</th>
                    <th>Patch Date Scheduled</th>
                </tr>
            </thead>
            <tbody>
            {rows}
            </tbody>
        </table>
        """
        rows = ""
        for i in records:
            row = f"""
                <tr>
                    <td>{i["presentation_name"]}</td>
                    <td>{i["ip_address"]}</td>
                    <td>{i["security_count"]}</td>
                    <td>{i["bugfix_count"]}</td>
                    <td>{i["enhancement_count"]}</td>
                    <td>{i["package_count"]}</td>
                    <td>{i["os"]}</td>
                    <td>{i["lifecycle_environment"]}</td>
                    <td>{i["patch_date"]}</td>
                </tr>
            """
            rows += row
    else:
        tableformat = """
        <table class="table" border=0 cellspacing="3" cellpadding="0">
            <thead>
                <tr>
                    <th>Hostname</th>
                    <th>IP Address</th>
                    <th>Installable Updates - Security</th>
                    <th>Installable Updates - Bug Fixes</th>
                    <th>Installable Updates - Enhancements</th>
                    <th>Installable Packages</th>
                    <th>OS</th>
                </tr>
            </thead>
            <tbody>
            {rows}
            </tbody>
        </table>
        """
        rows = ""
        for i in records:
            row = f"""
                <tr>
                    <td>{i["presentation_name"]}</td>
                    <td>{i["ip_address"]}</td>
                    <td>{i["security_count"]}</td>
                    <td>{i["bugfix_count"]}</td>
                    <td>{i["enhancement_count"]}</td>
                    <td>{i["package_count"]}</td>
                    <td>{i["os"]}</td>
                </tr>
            """
            rows += row
    return tableformat.format(rows=rows)