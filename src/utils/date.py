import calendar
from datetime import datetime

def find_patch_dates(gyear = None, gmonth = None):
    """
    """
    if gyear is None:
        gyear = datetime.today().year
    if gmonth is None:
        gmonth = datetime.today().month

    cal = calendar.Calendar()
    month = cal.monthdatescalendar(gyear,gmonth)
    monthly_patch_dates = {}

    first_week = month[0]
    for i in first_week:
        if i.weekday() == calendar.TUESDAY and i.day == 1:
            tuesday = -1
            thursday = -1
            break
        elif (i.weekday() == calendar.THURSDAY or i.weekday == calendar.WEDNESDAY) and i.day == 1:
            tuesday = 0
            thursday = -1
            break
        else:
            tuesday = 0
            thursday = 0
    
    for week in month:
        for day in week:
            if day.month == gmonth:
                    if day.weekday() == calendar.TUESDAY:
                        tuesday += 1
                        if tuesday == 3:
                            monthly_patch_dates["3rd Tue"] = day
                        elif tuesday == 4:
                            monthly_patch_dates["4th Tue"] = day
                    if day.weekday() == calendar.THURSDAY:
                        thursday += 1
                        if thursday == 2:
                            monthly_patch_dates["2nd Thu"] = day
                        elif thursday == 3:
                            monthly_patch_dates["3rd Thu"] = day
                        elif thursday == 4:
                            monthly_patch_dates["4th Thu"] = day
    monthly_patch_dates['TBD'] = 'TBD'
    return monthly_patch_dates