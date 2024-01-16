import calendar, json
from datetime import datetime

def find_patch_dates(year:int = None, month:int = None):
    if year is None:
        year = datetime.today().year
    if month is None:
        month = datetime.today().month

    calendarInstance = calendar.Calendar()
    calendarMonth = calendarInstance.monthdatescalendar(year,month)
    patchDatesForMonth = {}

    firstDayInFirstWeek = calendarMonth[0][0]
    
    if firstDayInFirstWeek.weekday() != calendar.MONDAY or firstDayInFirstWeek.weekday() != calendar.SUNDAY:
        calendarMonth.pop(0)
    
    tuesdayPositionInMonth = 0
    thursdayPositionInMonth = 0
    
    for week in calendarMonth:
        for day in week:
            if day.month == month:
                    if day.weekday() == calendar.TUESDAY:
                        tuesdayPositionInMonth += 1
                        if tuesdayPositionInMonth == 3:
                            patchDatesForMonth["3rd Tue"] = day
                        elif tuesdayPositionInMonth == 4:
                            patchDatesForMonth["4th Tue"] = day
                    if day.weekday() == calendar.THURSDAY:
                        thursdayPositionInMonth += 1
                        if thursdayPositionInMonth == 2:
                            patchDatesForMonth["2nd Thu"] = day
                        elif thursdayPositionInMonth == 3:
                            patchDatesForMonth["3rd Thu"] = day
                        elif thursdayPositionInMonth == 4:
                            patchDatesForMonth["4th Thu"] = day
    patchDatesForMonth['TBD'] = 'TBD'
    patchDatesForMonth['Excluded'] = 'Excluded'
    patchDatesForMonth['Decommissioned'] = 'Decomissioned' 
    return patchDatesForMonth

def parse_patch_dates(path: str):
    try:
        with open(path, 'r') as file:
            file_data = file.read()
            dates = json.loads(file_data)
            for date in dates.keys():
                dates[date] = datetime(dates[date][0], dates[date][1], dates[date][2])
    except:
        dates = {}
    dates['TBD'] = 'TBD'
    dates['Excluded'] = 'Excluded'
    dates['Decommissioned'] = 'Decomissioned' 
    return dates
