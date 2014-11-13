#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import pytest
from papers import decide

def test_basic():
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]

#Testing traveler with invalid passport format
def test_invalid_passport():
    assert decide("test_passport.json", "watchlist.json", "countries.json") == ["Reject", "Reject"]

#Testing visa with invalid visa format
def test_invalid_visa():
    assert decide("test_visa.json", "watchlist.json", "countries.json") == ["Reject", "Reject"]

#Testing priority of conflict. This traveler has invalid passport (Reject)
#and is in the watchlist (Secondary) and coming from a country with medical advisory (Quarantine).
#Result prioritizes Quarantine then Reject then Secondary.
def test_priority():
    assert decide("test_priority.json", "watchlist.json", "countries.json") == ["Quarantine"]

#Testing if traveler will be accepted regardless of the lowercase passport and country code
def test_casing():
    assert decide("test_casing.json", "watchlist.json", "countries.json") == ["Accept"]

def test_files():
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")

