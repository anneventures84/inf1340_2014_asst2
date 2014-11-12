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
    try:
        with open(input_file, "r") as file_reader:
            travelers_file = file_reader.read()
            travelers_json = json.loads(travelers_file)
    except:
        raise FileNotFoundError

    try:
        with open(watchlist_file, "r") as file_reader:
            watchlist_contents = file_reader.read()
            watchlist_json = json.loads(watchlist_contents)
    except:
        raise FileNotFoundError

    try:
        with open(countries_file, "r") as file_reader:
            countries_contents = file_reader.read()
            countries_json = json.loads(countries_contents)
    except:
        raise FileNotFoundError

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
            medical_advisory_from = countries_json[from_country]['medical_advisory']
            if medical_advisory_from != '':
                result_for_each_person.append('quarantine')

            if 'via' in person:
                via_country = person['via']['country']
                medical_advisory_via = countries_json[via_country]['medical_advisory']
                if medical_advisory_via != '':
                    result_for_each_person.append('quarantine')

                    # Fifth Condition: check valid visa if the entry reason is visit or transit
            if person['entry_reason'] == 'visit' or person['entry_reason'] == 'transit':
                visit_visa = countries_json[from_country]['visitor_visa_required']
                transit_visa = countries_json[from_country]['transit_visa_required']
                if 'visa' in person:
                    if visit_visa == '1' or transit_visa == '1':
                        traveller_visa_date = person['visa']['date']
                        traveller_visa_number = person['visa']['code']
                        if valid_visa( traveller_visa_number,traveller_visa_date):
                            result_for_each_person.append('accept')
                        else:
                            result_for_each_person.append("reject")

        # checking traveller status according to priority
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
    if passport_format.match(passport_number):
        return True

    else:
        return False


def valid_visa(visa_number, visa_date):
    """
    Checks whether a visa number is 2 sets of five alpha-number characters separated by dashes
    :rtype : object
    :param visa_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """

    valid_format = False
    valid_date = False

    visa_format = re.compile('^\w{5}-\w{5}$')

    if visa_format.match(visa_number):
        valid_format = True

    visa_years = datetime.datetime.now() - datetime.datetime.strptime(visa_date, "%Y-%m-%d")
    visa_years_difference = visa_years.days / 365

    if visa_years_difference < 2:
        valid_date = True
        # this if condition checks if the visa validity is less than two years

    if valid_date and valid_format:
        # return True only if visa has a valid format and is not over two years old
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
