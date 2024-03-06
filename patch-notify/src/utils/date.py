import calendar, json
from datetime import date

def find_patch_dates(year:int = None, month:int = None):
    """"""
    # Check if a year and month were supplied to the function, if not, use the current month and year
    if year is None:
        year = date.today().year
    if month is None:
        month = date.today().month

    calendar_instance = calendar.Calendar()
    calendar_month = calendar_instance.monthdatescalendar(year, month)
    patch_schedule = {}

    first_week = calendar_month[0]
    first_day = first_week[0]
    exceptions = [calendar.MONDAY, calendar.SUNDAY]
    
    # Remove the first calendar week if it does not begin on Sunday or Monday
    if first_day.month == month:
        if first_day.weekday() not in exceptions:
            calendar_month.pop(0)
    else:
        calendar_month.pop(0)
    
    # variables to record the position of the weekdays in a specific week for the month 
    mon_ordinal = 0
    tue_ordinal = 0
    thu_ordinal = 0
    
    for week in calendar_month:
        for day in week:
            if day.weekday() == calendar.MONDAY:
                mon_ordinal += 1
                if mon_ordinal == 1:
                    patch_schedule['1st Mon'] = day
            if day.weekday() == calendar.TUESDAY:
                tue_ordinal += 1
                if tue_ordinal == 2:
                    patch_schedule['2nd Tue'] = day
                elif tue_ordinal == 3:
                    patch_schedule["3rd Tue"] = day
                elif tue_ordinal == 4:
                    patch_schedule["4th Tue"] = day
            if day.weekday() == calendar.THURSDAY:
                thu_ordinal += 1
                if thu_ordinal == 2:
                    patch_schedule["2nd Thu"] = day
                elif thu_ordinal == 3:
                    patch_schedule["3rd Thu"] = day
                elif thu_ordinal == 4:
                    patch_schedule["4th Thu"] = day
    patch_schedule['TBD'] = 'TBD'
    patch_schedule['Excluded'] = 'Excluded'
    patch_schedule['Decommissioned'] = 'Decomissioned' 
    return patch_schedule

def parse_patch_dates(path: str):
    try:
        with open(path, 'r') as file:
            file_data = file.read()
            dates = json.loads(file_data)
            for pdate in dates.keys():
                dates[pdate] = date(dates[pdate][0], dates[pdate][1], dates[pdate][2])
    except:
        dates = {}
    dates['TBD'] = 'TBD'
    dates['Excluded'] = 'Excluded'
    dates['Decommissioned'] = 'Decomissioned' 
    return dates
