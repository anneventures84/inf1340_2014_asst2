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

        if traveller_status == 'Accept':
            first_name = traveller['first_name']
            last_name = traveller['last_name']
            try:
                traveller_visa_code = traveller['visa']['code']
                traveller_visa_date = traveller['visa']['date']
                valid_date = valid_date_format(traveller_visa_date)
                if not valid_date:
                    traveller_status = 'Reject'
            except:
                traveller_visa_code = ''
                traveller_visa_date = ''

def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
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

def valid_country_list(home_country_code, from_country_code, via_country_code, traveller_entry_reason, date_today,
                       country_list,traveller_visa_code, traveller_visa_date):
    """
    Checks whether the traveller needs an entry or transit visa is required, and whether there is currently a medical advisory
    :param home_country_code: string home country of the traveller
    :param from_country_code: string from country of the traveller
    :param via_country_code: string via country of the traveller
    :param traveller_entry_reason: string reason for travelling
    :param date_today: date of processing
    :param country_list: list of country with entry/visa requirements or has medical advisory
    :param traveller_visa_code: string visa code/number
    :param traveller_visa_date: date visa expiration date
    :return: Quarantine country is in medical advisory; Reject if traveller has no entry permit or visa which is required by the destination country; Accept passed validations
    """
    if from_country_code != '':
       validate_country = from_country_code
    else:
       if via_country_code != '':
           validate_country = via_country_code
       else:
           return 'Reject'
    try:
        if country_list[validate_country]['medical_advisory'] != '':
            country_traveller_status = 'Quarantine'
        else:
            country_traveller_status = 'Accept'
    except:
        country_traveller_status = 'Accept'
    if country_traveller_status == 'Accept':
        if home_country_code == 'KAN' and traveller_entry_reason == 'Returning':
            country_traveller_status = 'Accept'
        else:
            try:
                if (country_list[home_country_code]['visitor_visa_required'] == '1' or
                    country_list[home_country_code]['transit_visa_required'] == '1'):
                    if traveller_visa_code == "":
                        country_traveller_status = 'Reject'
                    else:
                        if (date_today.year - traveller_visa_date.year)>= 2:
                            country_traveller_status = 'Reject'
                        else:
                            country_traveller_status = 'Accept'
            except:
                country_traveller_status = 'Reject'
    return country_traveller_status
