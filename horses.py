from bs4 import BeautifulSoup
from datetime import date
import re
import requests

def get_todays_racecards():
    """
    Return a list of dictionaries containing the keys 'name' and 'link' for
    the race cards of each of todays races.
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
        # race card. So don't add it to the list. Otherwise add it.
        if len(link) is not 0 and len(name) is not 0:
            racecard = {}
            racecard['name'] = name
            racecard['link'] = link
            racecards.append(racecard)

    return racecards

def get_betting_forecast(soup):
    """Return the betting forecast as a list."""

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

def get_race_title(soup):
    """Return the race title"""
    for a in soup.select('table.raceHead td.raceTitle strong.uppercase a'):
        return a.get_text()

def get_meeting_going(soup):
    going = soup.select('div.raceInfo.clearfix p')
    return going[0].contents[2].lstrip().split('(', 1)[0].rstrip()

def is_handicap(race_title):
    term = 'handicap'
    race_title = race_title.lower()
    words = race_title.split()
    return term in words

def parse_horses(racecard):
    horses = racecard.select('tr.cr')
    for horse in horses:
        name = horse.select('td.h a')
        name = [a.get_text() for a in name][0]
        weight = horse.select('td')[4].get_text()
        number = horse.select('td.t strong')[0].get_text()
        print(number, name, weight)



def parse(racecard):
    root_url = 'http://racingpost.com'
    index_url = root_url + racecard['link']
    response = requests.get(index_url)
    soup = BeautifulSoup(response.text)

    # Get the going for the meet.
    going = get_meeting_going(soup)

    # Create a meeting and
    meeting = Meeting(racecard['name'], going)

    racecards = soup.select('div.cardBlock.lightCards')

    print(meeting.name)

    count = 0
    for racecard in racecards:
        # Get race title
        race = Race(get_race_title(racecard))

        if is_handicap(race.name):

            meeting.add_race(race)
            print(race.name)

            parse_horses(racecard)

            # Get the betting forecast
            betting_forecast_dict = get_betting_forecast(racecard)
            for name, odds in betting_forecast_dict.items():
                print(name, odds)

            break
            """
            count += 1

            if count >= 2:
                import sys
                sys.exit(0)
            """


class Meeting():
    races = []
    def __init__(self, name, going):
        self.name = name
        self.going = going

    def add_race(self, race):
        self.races.append(race)

    def going(self):
        return self.going

    def name(self):
        return self.name


class Race():
    def __init__(self, name):
        self.name = name

    def name(self):
        return self.name


class Horse():
    def __init__(self, name):
        self.name = name


if __name__ == '__main__':
    # Get a list of todays race cards.
    # These aren't race cards. This in a dictionary of meeting name,
    # and a link to the full list of races.
    racecards = get_todays_racecards()

    # parse race card
    for racecard in racecards:
        parse(racecard)
