from datetime import datetime
from unicodedata import normalize

def ordinal(n):
    if 4 <= n <= 20 or 24 <= n <= 30:
        return str(n) + 'th'
    else:
        return str(n) + ["st", "nd", "rd"][n % 10 - 1]


def get_date():
    tstamp      = datetime.now().timetuple()
    month       = datetime.now().strftime('%B')
    day         = ordinal(tstamp.tm_mday)
    year        = tstamp.tm_year
    hour        = tstamp.tm_hour - 12 if tstamp.tm_hour > 12 \
                                        else tstamp.tm_hour
    minute      =  '0' + str(tstamp.tm_min) if tstamp.tm_min < 10 \
                                            else tstamp.tm_min
    second      = datetime.now().time().second
    
    def meridiem():
        return "am" if tstamp.tm_hour < 12 else "pm"

    return "%s %s %s, %s:%s:%s %s" %(month, 
                                    day, 
                                    year, 
                                    hour, 
                                    minute, 
                                    second, 
                                    meridiem())


def get_timestamp():
    return datetime.utcnow()


def date_to_timestamp(d):
    import time
    return int(time.mktime(d.timetuple()))


def random_date(start, end):
    """ 
    Ruturns a date between a start and end date
    ie: randomDate(datetime(2013,01,01), datetime(2013,12,05))
    """
    import random

    stime = date_to_timestamp(start)
    etime = date_to_timestamp(end)

    ptime = stime + random.random() * (etime - stime)
    return datetime.fromtimestamp(ptime)

def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time 
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"


def iso_date(date):
    return date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def console_inspect(data):
    print '\n'
    print '----'
    print data
    print '----'
    print '\n'


def random_str(length):
    import string
    import random

    lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(length)]
    return "".join(lst)
    
    
def avatar(email, size):
    from hashlib import md5
    return 'http://www.gravatar.com/avatar/' + md5(email).hexdigest() + '?d=mm&s=' + str(size)


def slug(text, encoding=None,
         permitted_chars='abcdefghijklmnopqrstuvwxyz0123456789-'):
    if isinstance(text, str):
        text = text.decode(encoding or 'ascii')
    clean_text = text.strip().replace(' ', '-').lower()
    while '--' in clean_text:
        clean_text = clean_text.replace('--', '-')
    ascii_text = normalize('NFKD', clean_text).encode('ascii', 'ignore')
    strict_text = map(lambda x: x if x in permitted_chars else '', ascii_text)
    return ''.join(strict_text)


def abbreviate(name, pretty=False):
    names = name.split()
    if len(names) == 2:
        return name
    result = [names[0]]
    tiny_name = False
    for surname in names[1:-1]:
        if len(surname) <= 3:
            result.append(surname)
            tiny_name = True
        else:
            if pretty and tiny_name:
                result.append(surname)
            else:
                result.append(surname[0] + '.')
            tiny_name = False
    result.append(names[-1])
    return ' '.join(result)