#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Anne Simon and Rana ElSafadi'
__email__ = "anne.simon@mail.utoronto.ca and rana.elsafadi@mail.utoronto.ca"

# imports one per line
import re
import datetime
import json


def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted
<<<<<<< HEAD
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

    with open(countries_file, "r") as file_reader:
        countries_contents = file_reader.read()
        countries_json = json.loads(countries_contents)

    result = []

    # first condition
    for person in travelers_json:
        result_for_each_person = []
        traveler_passport = person['passport']
        last_name = person['last_name']
        found_in_watchlist = False
        for passports in watchlist_json:
            watchlist_passport = passports['passport']
            watchlist_name = passports['last_name']
            if watchlist_passport == traveler_passport or watchlist_name == last_name:
                found_in_watchlist = True
        if found_in_watchlist:
            result_for_each_person.append("secondary")

        # second condition
        # condition added to the if statement in condition 3

        # third condition
        if person['first_name'] == '' \
                or person['last_name'] == '' \
                or (not valid_date_format(person['birth_date'])) \
                or (not valid_passport_format(person['passport'])) \
                or person['home']['city'] == '' \
                or person['home']['country'] == '' or person['home']['region'] == '' \
                or person['entry_reason'] == '' \
                or person['from']['city'] == '' \
                or person['from']['region'] == '' \
                or person['from']['country'] == '' \
                or person["entry_reason"] != "returning":
            print(valid_passport_format(person['passport']))
            result_for_each_person.append("reject")

        # fourth condition
        from_country = person['from']['country']
        if from_country in countries_json:
            medical_advisory = countries_json[from_country]['medical_advisory']
            if medical_advisory != '':
                result_for_each_person.append('quarantine')
                # Fifth Condition: check valid visa if the entry reason is visit or transit
            if person['entry_reason'] == 'visit' or 'transit':
                transit_visa = countries_json[from_country]['transit_visa_required']
                visitor_visa = countries_json[from_country]['visitor_visa_required']
                traveller_visa = person['visa']['date']
                if transit_visa == '1' or visitor_visa == '1' \
                        and datetime.year - traveller_visa.year < 2:
                    result_for_each_person.append('accept')
                else:
                    result_for_each_person.append("reject")

        if 'quarantine' in result_for_each_person:
            result.append('quarantine')
        elif 'reject' in result_for_each_person:
            result.append('reject')
        elif 'secondary' in result_for_each_person:
            result.append('secondary')
        else:
            result.append('accept')

    return result


def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """

    passport_format = re.compile('^\w{5}-\w{5}-\w{5}-\w{5}-\w{5}$')

    passport_format = re.compile('^.{5}-.{5}-.{5}-.{5}-.{5}$')

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
print(x)
