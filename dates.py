"""
Receives a date in dictionary.
Returns the next day in a dictionary
"""
def nextDay(date):
    day = date["day"]
    month = date["month"]
    year = date["year"]

    ret = {}

    # treating day
    if day >= 31:
        new_day = 1
    else:
        new_day = day + 1

    # treating month
    if new_day == day + 1:
        new_month = month
    else:
        if month >= 12:
            new_month = 1
        else:
            new_month = month + 1
    
    # treating year
    if new_month == month + 1 or new_month == month:
        new_year = year
    else:
        new_year = year + 1

    ret["day"] = new_day
    ret["month"] = new_month
    ret["year"] = new_year

    # check days 31
    if new_day == 31 and (new_month == 2 or new_month == 4 or new_month == 6 or new_month == 9 or new_month == 11):
        ret = nextDay(ret)
    # check day 30/02
    elif new_day == 30 and new_month == 2:
        ret = nextDay(ret)
    elif new_day == 29 and new_month == 2 and (new_year % 4) != 0:
        ret = nextDay(ret)

    return ret

"""
Receives 2 dates in dictionaries.
Compares if the dates are equal or not.
Returns 1 if is the date1 is less than date2. Returns 0 in contrary.
"""
def compareDates(date1, date2):
    try:
        day1 = date1["day"]
        month1 = date1["month"]
        year1 = date1["year"]
        day2 = date2["day"]
        month2 = date2["month"]
        year2 = date2["year"]
    except:
        print("Error extraction dates from dictionary")
        return 0
    
    # compare years
    if year1 > year2:
        return 0
    if year1 < year2:
        return 1
    
    # same year. compare months
    if month1 > month2:
        return 0
    if month1 < month2:
        return 1

    # same month. compare days
    if day1 > day2:
        return 0
    if day1 < day2:
        return 1

    return 1