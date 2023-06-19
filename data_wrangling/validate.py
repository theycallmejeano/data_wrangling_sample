"""Validation functions"""
from datetime import date
import pandas as pd


def validate_data(data: pd.DataFrame) -> bool:
    """
    Validate data

    Args
        data - dataframe with the data for validation

    Returns
        True if all tests pass, False otherwise
    """
    # Test 1: validate that all dates are before today
    date_test = (pd.to_datetime(data['date']).dt.date < date.today()).all()

    # Test 2: validate that there are no nulls
    null_test = (data['value'].notnull()).all()

    # Test 3: validate that temepratures are > 0
    min_test = (data['value'] > 0).all()

    # Return True if all tests pass, False otherwise
    return bool(date_test and null_test and min_test)
