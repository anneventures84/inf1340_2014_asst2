#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import re
import datetime
import json


def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """
    with open(input_file, "r") as file_reader:

        travelers_file = file_reader.read()
        travelers_json = json.loads(travelers_file)

    with open(watchlist_file, "r") as file_reader:
        watchlist_contents = file_reader.read()
        watchlist_json = json.loads(watchlist_contents)
        result = []
        
    for passport in travelers_json:
        traveler_passport = passport['passport']
        found_in_watchlist = False
        for passports in watchlist_json:
            watchlist_passport = passports['passport']
            if watchlist_passport == traveler_passport :
                found_in_watchlist = True;
        if found_in_watchlist:
            result.append("reject")
        else:
            result.append("accept")

    return result

    #return ["Reject"]


def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('.{5}-.{5}-.{5}-.{5}-.{5}')

    if passport_format.match(passport_number):
        return True

    else:
        return False


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

x = decide("example_entries.json", "watchlist.json", "countries.json")
print (x )