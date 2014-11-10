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

    :param input_file: The name of a JSON formatted file that contains cases to decide (i.e., example_entries.json)
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist (i.e., watchlist.json)
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether (i.e., countries.json)
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """
    try:
        with open(input_file, "r") as traveller_input:
            travellers_file = traveller_input.read()
            travellers_json = json.loads(travellers_file)
    except:
        raise FileNotFoundError

    try:
        with open(watchlist_file, "r") as watchlist_input:
                watchlist_contents = watchlist_input.read()
                watchlist_json = json.loads(watchlist_contents)
    except:
        raise FileNotFoundError
    try:
        with open(countries_file, "r") as country_input:
            country_contents = country_input.read()
            country_list_json = json.loads(country_contents)
    except:
        raise FileNotFoundError

    result = []
    date_today = datetime.date.today()

    for traveller in travellers_json:
        from_country_code = ''
        via_country_code = ''
        traveller_status = 'Accept'
        try:
            home_country_code = traveller['home']['country'].upper()
        except ValueError:
            traveller_status = 'Reject'
        if traveller_status == 'Accept':
            try:
                from_country_code = traveller['from']['country'].upper()
            except ValueError:
                try:
                    via_country_code = traveller['via']['country'].upper()
                    from_country_code = ''
                except ValueError:
                    traveller_status = 'Reject'
        if traveller_status == 'Accept':
            first_name = traveller['first_name']
            last_name = traveller['last_name']
            try:
                traveller_visa_code = traveller['visa']['code']
                traveller_visa_date = traveller['visa']['date']
                valid_date = valid_date_format(traveller_visa_date)
                if not valid_date:
                    traveller_status = 'Reject'
            except ValueError:
                traveller_visa_code = ''
                traveller_visa_date = ''
        if traveller_status == 'Accept':
            traveller_entry_reason = traveller['entry_reason']
            traveller_status = valid_country_list(home_country_code, from_country_code, via_country_code, traveller_entry_reason,
                                                 date_today, country_list_json, traveller_visa_code, traveller_visa_date)
        if traveller_status == 'Accept':
            traveller_passport = traveller['passport'].upper()
            valid_passport = valid_passport_format(traveller_passport)
            if not valid_passport:
                traveller_status = 'Reject'
        if traveller_status == 'Accept':
            traveller_birth_date = traveller['birth_date']
            valid_date = valid_date_format(traveller_birth_date)
            if not valid_date:
                traveller_status = 'Reject'
        if traveller_status == 'Accept':
            traveller_status = watchlist(traveller_passport, first_name, last_name, watchlist_json)
        result.append(traveller_status)
    return result


def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
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

def watchlist(passport_number, first_name, last_name, watchlist):
    """
    Checks whether the traveller is in watch list
    :param passport_number: string passport number of the traveller
    :param first_name: string first name of the traveller
    :param last_name: string last name of the traveller
    :param watchlist: list of persons under watch list
    :return: Secondary traveller is in watch list, Accept passed validations
    """
    watch_traveller_status = 'Accept'
    for watch in watchlist:
        if watch['passport'] == passport_number:
            watch_traveller_status = 'Secondary'
            break
            if watch['first_name'] == first_name:
                if watch['last_name'] == last_name:
                    watch_traveller_status = 'Secondary'
                    break
    return watch_traveller_status


x = decide("example_entries.json", "watchlist.json", "countries.json")
print (x )