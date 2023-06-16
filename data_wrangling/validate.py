"""Validation functions"""
from datetime import date
import pandas as pd


def validate_data(data: pd.DataFrame):
    """
    Validate data

    Args
    ---
        data - dataframe with the data for validation
    """
    # Test 1: validate date format
    date_test = (pd.to_datetime(data['date']).dt.date < date.today()).all()

    # Test 2: validate that there are no nulls
    null_test = (data['value'].notnull()).all()

    # Return True if all tests pass, False otherwise
    return bool(date_test and null_test)
