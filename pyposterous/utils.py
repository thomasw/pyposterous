import sys

def docstring_trim(docstring):
    """A docstring normalization function taken straight from PEP 257 at
    http://www.python.org/dev/peps/pep-0257/ 
    
    docstring -- the string to be normalized
    
    """
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)

def parse_date(time_string, time_format="%a, %d %b %Y %H:%M:%S"):
    """Converts a string representation of a time stamp to a UTC datetime object.
    A utcoffset of -HHMM is expected in the time_string, but should not be
    represented in the time_format string by %z. Just leave it out. This
    function will find it, and do the necessary calculation to convert the
    output to UTC.
    
    time_string -- a string to be converted to a UTC datetime object. Must contain a utcoffset string +HHMM or -HHMM
    time_format -- a string representing the format of time_string. See strptime documentation for an example. Leave out %z.    
    """
    from re import findall
    from datetime import datetime
    
    utc_offset_str = findall(r'\+[0-9]{4}|-[0-9]{4}', time_string)[0]
    time_string = time_string.replace(utc_offset_str, "", 1)
    
    # the substitution above may have resulted in unnecessary whitespace
    time_string = time_string.strip().replace('  ', ' ')
        
    return convert_to_utc(datetime.strptime(time_string, time_format), utc_offset_str)
    
def convert_to_utc(date, offset):
    from datetime import timedelta
    
    sign = offset[0]
    hour = int(offset[1:3])
    minute = int(offset[3:5])
    
    if sign == '-': sign = 1
    if sign == '+': sign = -1
    
    return date + sign * timedelta(hours=hour, minutes=minute)
    
def try_parse_int(number):
    try:
        return int(number)
    except:
        return "%s" % number
