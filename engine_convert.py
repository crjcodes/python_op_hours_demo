import logging, sys, csv
import dateutil.parser, re

from model_operating_hours import OperatingHours

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def ConvertFrom(filename):
    """
    Takes the name of a csv file matching the business specification, then
    maps to a list of our internal data model
    DESIGN: mapping to a data model may be overkill. Can just map to a json structure
    and treat it like a database of sorts
    """
    if not filename or not filename.strip():
        logging.error("Invalid filename for input data")
        raise ValueError()

    internal_data = {}

    with open(filename, newline='') as cvsfile:
        reader = csv.DictReader(cvsfile)
        for row in reader:
            restaurant_name = row['Restaurant Name']
            in_hours = row['Hours'].strip()
            parsed_op_hours = parse_op_hours(in_hours)
            internal_data[restaurant_name] = parsed_op_hours

    return internal_data


def parse_op_hours(human_readable_op_hours):
    """
    TODO:
      Future: if performance concerns, compile the regex
        beforehand (plus other options)
      Future: the find/replace can be replaced by one operation
    """
    if human_readable_op_hours is None or human_readable_op_hours == "":
        return None

    sections = re.split(r'\s*\/\s*', human_readable_op_hours)

    op_hours_per_day = {}

    for section in sections:
        section, close_time_text = parse_last_time_text(section)
        section, open_time_text = parse_last_time_text(section)
        open_time = parse_time(open_time_text)
        close_time = parse_time(close_time_text)

        subsections = re.split(r'\s*,\s*', section)

        for subsection in subsections:
            for dow in parse_dow_text(subsection):
                op_hours_per_day[dow] = OperatingHours(open_time, close_time)

    return op_hours_per_day


def parse_last_time_text(section):
    if section is None or section == "":
        return section, None

    # non-overlapping
    # look for the last occurrence first
    # TODO: FUTURE: possible performance improvements with a different search, if needed
    match = re.search(r"(?s:.*)\s([0-9][0-9:]*\s*[ap]m)\s*", section)

    if match is None:
        return section, None

    time_text = match.group(1)
    section = section.replace(time_text, "")
    # TODO: as regex, in case spaces aren't there
    section = section.replace(" - ", "")

    # TODO: error check on the match results
    return section, re.sub(r'\s', "", time_text)


def parse_dow_text(section):
    # TODO; right now, relying on exceptions for the error handling

    # TODO: move to common location
    dow_full = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    dow_list = []

    section = section.replace("\"", "")
    section = re.sub(r'\s+', "", section)

    # disconnected days
    first_break = section.split(",")
    for f in first_break:
        second_break = f.split("-")
        start_dow = second_break[0].strip()[0:3]
        if start_dow not in dow_full:
            continue

        df_start_index = dow_full.index(start_dow)

        if len(second_break) == 1:
            dow_list.append(f.strip())
        else:
            end_dow = second_break[1].strip()[0:3]
            if end_dow not in dow_full:
                continue

            df_end_index = dow_full.index(end_dow)
            for df in dow_full[df_start_index:df_end_index + 1]:
                dow_list.append(df)

    return dow_list


# TODO: FUTURE: can be moved to a utility for common use
# TODO: FUTURE: better way to do this in python

def parse_time(time_text):
    # a bit of a hack, but the python time library doesn't seem to have the power of C# DateTime
    dummy_datestamp = "2000-01-01 " + time_text
    parsed = dateutil.parser.parse(dummy_datestamp)
    return parsed.strftime("%H:%M")


# Area of volatility, if other data patterns will break this, will need to update
def split_line(line):
    return re.split(r',(?=")', line)
