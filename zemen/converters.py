#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module provides functions for converting between Julian Day Number (JDN),
Gregorian calendar dates, and Ethiopian calendar dates. It supports the conversion
of:

1. Gregorian dates to Julian Day Numbers (JDN) and vice versa.
2. Julian Day Numbers (JDN) to Ethiopian calendar dates.
3. Gregorian dates to Ethiopian calendar dates.
"""


from calendar import isleap
from datetime import date, datetime, timedelta, timezone



def _greg_to_jdn(*, year: int, month: int, day: int) -> int:
    """
    Convert Gregorian date to Julian Day Number(JDN).

    :param year: Year
    :param month: Month
    :param day: Day

    :return: Julian Day Number(JDN)

    :raises ValueError: If the date is invalid for Gregorian calendar
    """
    try:
        date(year, month, day)
    except ValueError:
        raise ValueError("Invalid date for Gregorian calendar")
    return date(year, month, day).toordinal() + 1721425


def jdn_to_greg(jdn: int) -> date:
    """
    Convert Julian Day Number(JDN) to Gregorian date.

    :param jdn: Julian Day Number(JDN)

    :return: Gregorian date

    :raises ValueError: If the JDN is invalid
    """
    if jdn < 1721425:
        raise ValueError("Invalid Julian Day Number")
    return date.fromordinal(jdn - 1721425)


def _eth_from_jdn(jdn: int) -> tuple:
    """
    Convert Julian Day Number(JDN) to Ethiopian date.

    :param jdn: Julian Day Number(JDN)

    :return: Ethiopian date as tuple of year, month, day

    :raises ValueError: If the JDN is invalid
    """

    JDN_ETH_OFFSET : int = 1723856

    if jdn < 1721425:
        raise ValueError("Invalid Julian Day Number")
    
    r = (jdn - JDN_ETH_OFFSET) % 1461
    n = (r % 365) + (365 * (r // 1460))
    year = 4 * ((jdn - JDN_ETH_OFFSET) // 1461) + (r // 365) - (r // 1460)
    month = n // 30 + 1
    day = n % 30 + 2
    return year, month, day


def eth_from_greg(*, year: int, month: int, day: int) -> tuple:
    """
    Convert Gregorian date to Ethiopian date.

    :param year: Year
    :param month: Month
    :param day: Day

    :return: Ethiopian date as tuple of year, month, day

    :raises ValueError: If the date is invalid for Gregorian calendar
    """

    jdn = _greg_to_jdn(year=year, month=month, day=day)
    return _eth_from_jdn(jdn)


def eth_to_greg(*, year: int, month: int, day: int) -> tuple:
    """
    Convert Ethiopian date to Gregorian date.

    :param year: Year
    :param month: Month
    :param day: Day

    :return: Gregorian date as tuple of year, month, day

    :raises ValueError: If the date is invalid for Ethiopian calendar
    """