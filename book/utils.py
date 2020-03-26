import re, datetime

def check_valid_year(string):
    this_year = datetime.datetime.now().year
    pattern = re.compile('^\d{4}$')
    if pattern.match(string) and int(string) <= this_year:
        return True
    return False

