#!/usr/bin/env python3

"""Weather-Bird

A module for collecting queries and returning current weather data over
Twitter.

classes:
    WeatherData: A small class representation of the weather data returned in
        the Twitter query.
    WeatherError: A Weather-Bird specific error class.
"""

import requests

_OPEN_WEATHER_MAP_API_URL = 'http://api.openweathermap.org/data/2.5/weather?q='


class WeatherError(Exception):
    """WeatherError class

    Inherits the base Exception class in order to provide specific exception
    support for the Weather Bird application.
    """
    pass


class WeatherData(object):
    """WeatherData class

    Attributes:
        city: City name location information.
        country: Country name location information.
        conditions: Current weather conditions of the location.
        temperature: Current temperature of the location.
    """
    def __init__(self):
        super(WeatherData, self).__init__()

        # Location information
        self.city = ''
        self.country = ''

        # Temperature information
        self.conditions = ''
        self.temperature = 0.0

        return


def _kelvin_to_celcius(kelvin_temp):
    """Convert Kelvin to Celcius (Internal)

    Arguments:
        kelvin_temp: A float representation of temperature in kelvin.

    Returns:
        A float representation of temperature in celcius.
    """
    return kelvin_temp - 273.15

def _kelvin_to_fahrenheit(kelvin_temp):
    """Convert Kelvin to Fahrenheit (Internal)

    Arguments:
        kelvin_temp: A float representation of temperature in kelvin.

    Returns:
        A float representation of temperature in fahrenheit.
    """
    celcius_temp = _kelvin_to_celcius(kelvin_temp)

    return (celcius_temp * 1.8) + 32.0

def _get_weather(city):
    """Get Weather (Internal)

    Arguments:
        city: A string representation of the city to query for weather info.

    Returns:
        A WeatherObject class instance containing basic weather data for the
        desired region.

    Raises:
        WeatherError if the API query or connection to the server failed.
    """
    # Open the API URL with the city request. Expect data in JSON format
    query = _OPEN_WEATHER_MAP_API_URL + city.strip()

    try:
        data = requests.get(query).json()
    except requests.exceptions.ConnectionError as e:
        raise WeatherError('Could not connect to weather server')

    # Convert the raw data to a usable weather object representation
    # Make sure no error message was returned
    if data['cod'] != 200:
        raise WeatherError(data['message'].replace('Error: ', ''))
    
    # We have a valid weather set. Now let's get useful data
    weather_obj = WeatherData()

    # Ex. { ... "name":"Seattle" ... }
    weather_obj.city = data['name']

    # Ex. { ... "sys":{ ... "country":"USA" ... } ... }
    weather_obj.country = data['sys']['country']

    # Ex. { ... "weather":{ [ ... "main":"Clear" ... ] ... } ... }
    weather_obj.conditions = data['weather'][0]['description']

    # Ex. { ... "main":{ ... "temp":281.15 ... } ... }
    # NOTE: Temperature is given in Kelvin and must be converted
    weather_obj.temperature = _kelvin_to_fahrenheit(data['main']['temp'])

    return weather_obj

def _format_tweet(reply_to, weather_obj):
    """Format Tweet (Internal)

    Given a populated weather object, the object data will be formatted
    appropriately to be submitted over twitter as a reply.

    Arguments:
        reply_to: The Twitter user handle which to reply.
        weather_obj: A WeatherObject class instance pre-populated with
            weather and location data.

    Returns:
        The unicode formatted message ready for sending.
    """
    msg = u'@%s Current weather for %s, %s is %s and %.1f\u00B0F'
    msg = msg % (reply_to, weather_obj.city, weather_obj.country,
            weather_obj.conditions, weather_obj.temperature)

    return msg

def _debug():
    """Debug (Internal)

    Used to test the retrieval and formatting of the message data

    Returns:
        True on success, False otherwise.
    """
    username = input('> Enter your Twitter username: ')
    city = input('> Enter your city: ')

    # Attempt to get the inputted data
    try:
        weather_obj = _get_weather(city)
    except WeatherError as e:
        print(e)
        return False

    # Print the weather data for now
    msg = _format_tweet(username, weather_obj)
    print(msg)

    return True

if __name__ == '__main__':
    _debug()
