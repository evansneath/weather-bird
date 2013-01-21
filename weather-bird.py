#!/usr/bin/env python3

from bs4 import BeautifulSoup
import urllib.request


def main():
    query = 'http://weather.com/search/enhancedlocalsearch?where={}'

    location = input('> Enter your city, state: ')
    location = location.replace(',', '').replace(' ', '+')

    url = urllib.request.urlopen(query.format(location))

    # Read the html source and put it in the soup
    html = url.read()
    soup = BeautifulSoup(html)

    # Get the temperature and condition html elements
    temp_soup = soup.find('li', class_='wx-temp')
    cond_soup = soup.find('li', class_='wx-phrase')

    # Check to see if we get anything here, if not the query is bad
    if temp_soup is None or cond_soup is None:
        print('Sorry, I couldn\'t get the weather in your location.')
        return

    # Get the real temperature and condition text
    temp = temp_soup.text.strip()
    cond = cond_soup.text.strip().lower().replace('/', 'and')

    print('It\'s currently {} and {}.'.format(temp, cond))
    return


if __name__ == '__main__':
    main()
