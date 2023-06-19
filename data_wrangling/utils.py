"""Functions to pull data from the API"""
import json
import os
import datetime
from typing import Tuple, Optional
import requests
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from loguru import logger

load_dotenv()

# define variables
LOCATION_NAMES = json.loads(os.environ['LOCATION_NAMES'])
START_DATE = os.environ['START_DATE']
END_DATE = os.environ['END_DATE']
URL_TEMPLATE = os.environ['URL_TEMPLATE']


# format the URL
def format_url(lat:float, long:float) -> str:
    """
    Format the URL for an API request

    Args
        lat: Latitude of the location
        long: Longitude of the location

    Returns
        str: Formatted URL

    """
    max_date = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime(format='%Y-%m-%d')

    if END_DATE >= str(max_date):
        raise TypeError('Invalid end date')

    url = URL_TEMPLATE.format(lat=lat, long=long, start=START_DATE, end=END_DATE)

    return url

# get coords
def get_coords(location: str) -> Tuple[float, float]:
    """
    Get the coordinates of a given location to 2 decimal places

    Args:
        location: Name of the location

    Returns:
        Tuple[float, float]: Latitude and longitude of the location
    """
    # calling the Nominatim tool
    loc = Nominatim(user_agent="GetLoc")

    # entering the location name
    location_details = loc.geocode(location)

    # get latitude and longitude
    latitude = round(location_details.latitude, 2)
    longitude = round(location_details.longitude, 2)

    return latitude, longitude


# get API response
def get_api_response(url: str) -> Optional[requests.Response]:
    """
    Send a GET request for a given URL

    Args
        url (str): The URL to send the request to

    Returns
        response: API Response
    """
    session = requests.Session()

    # get response
    try:
        response = session.get(url, timeout=20)
        return response

    except requests.exceptions.RequestException as ex:
        logger.info('Connection error'+ str(ex))
        return None
