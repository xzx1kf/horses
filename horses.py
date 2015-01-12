from bs4 import BeautifulSoup
from datetime import date
import re
import requests

def get_todays_racecards():
    """
    Return a list of dictionaries containing the keys 'name' and 'link' for
    the racecards of each of todays races.
    """
    index_url = 'http://www.racingpost.com/horses2/cards/home.sd?r_date=$DATE$'
    index_url = index_url.replace('$DATE$', date.today().isoformat())
    response = requests.get(index_url)
    soup = BeautifulSoup(response.text)

    crBlocks = soup.select('div.crBlock')

    racecards = []
    for race in crBlocks:
        link = ''
        name = ''
        for a in race.select('p.bull.show a'):
            link = a.attrs.get('href')

        for a in race.select('td.meeting h3 a'):
            name = a.get_text()

        # If either the name or link is missing, then it isn't a valid
        # racecard. So don't add it to the list. Otherwise add it.
        if len(link) is not 0 and len(name) is not 0:
            racecard = {}
            racecard['name'] = name
            racecard['link'] = link
            racecards.append(racecard)

    return racecards

def get_betting_forecast(racecard):
    """Return the betting forecast as a list."""
    root_url = 'http://racingpost.com'
    index_url = root_url + racecard['link']
    response = requests.get(index_url)
    soup = BeautifulSoup(response.text)

    # Return a list of all <p> tags that have an id beginning with "bettingForecastContainer".
    betting_forecast = [a.get_text() for a in soup.select('div.info >  p[id^="bettingForecastContainer"]')]

    # The regex pattern matches against the following, "2/1 Horse Name,"
    pattern = re.compile('((\d+/\d+)\s(.+?)),')

    # This will need changing. At the moment it is a hard-coded selection on which card to
    # find all the matches against.
    betting_forecast_dict = {}

    # Create a dictionary of the betting forecast.
    for entry in pattern.findall(betting_forecast[0]):
        betting_forecast_dict[entry[1]] = entry[2]
    return betting_forecast_dict

if __name__ == '__main__':
    # Get a list of todays racecards.
    racecards = get_todays_racecards()

    betting_forecast_dict = get_betting_forecast(racecards[0])
    for name, odds in betting_forecast_dict.items():
        print(name, odds)

