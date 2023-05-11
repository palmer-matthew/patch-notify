import calendar
from datetime import datetime

def find_patch_dates():
    """
    """
    cal = calendar.Calendar()
    month = cal.monthdatescalendar(datetime.today().year, datetime.today().month)

    monthly_patch_dates = {}
    tuesday = 0
    thursday = 0
    for week in month:
        for day in week:
            if day.month == datetime.today().month:
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