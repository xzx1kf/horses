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
        try:
            code = race.select('table.raceHead td.meeting h3 em')[0].get_text()
            if code == 'RUK' or code == 'ATR':
                pass
            else:
                continue
        except:
            continue


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

def get_betting_forecast(race_soup):
    """Return the betting forecast as a list."""
    # Return a list of all <p> tags that have an id beginning with "bettingForecastContainer".
    betting_forecast = [a.get_text() for a in race_soup.select('div.info p[id^="bettingForecastContainer"]')]

    # The regex pattern matches against the following, "2/1 Horse Name,"
    pattern = re.compile('((\d+/\d+)\s(.+?))[,.]')

    # This will need changing. At the moment it is a hard-coded selection on which card to
    # find all the matches against.
    betting_forecast_dict = {}

    # Create a dictionary of the betting forecast.
    for entry in pattern.findall(betting_forecast[0]):
        betting_forecast_dict[entry[2]] = entry[1]
    return betting_forecast_dict

def parse_horses(racecard):
    horses = racecard.select('tr.cr')
    horses_list = []
    for horse in horses:
        name = [a.get_text() for a in horse.find(title="Full details about this HORSE")][0].strip()
        weight = horse.select('td')[4].get_text().strip()
        number = horse.select('td.t strong')[0].get_text().strip()
        short_info = horse.select('div.horseShortInfo')
        last_run = 0
        try:
            last_run = int(short_info[0].get_text().strip().split('(')[0])
        except:
            last_run = 0
        horses_list.append(Horse(number, name, weight, last_run))
    return horses_list

def parse_race(race_url):

    response = requests.get(race_url)
    race_soup = BeautifulSoup(response.text)

    raceInfo = race_soup.select('div.raceInfo ul.results li')

    # Time
    time = race_soup.select('span.navRace span')[0].get_text().strip()

    # Going
    going = raceInfo[3].select('strong')
    going = (going[0].get_text()).strip()

    # Distance
    distance = raceInfo[2].select('strong')
    distance = (distance[0].get_text()).strip()

    # Runners
    runners = raceInfo[1].select('strong')
    runners = (runners[0].get_text()).strip()

    horses = parse_horses(race_soup)

    # Betting Forecast
    betting_forecast_dict = get_betting_forecast(race_soup)
    for name, odds in betting_forecast_dict.items():
        for horse in horses:
            if horse.name.lower() == name.lower():
                horse.forecast = odds

    return time, going, distance, runners, horses

def parse(racecard):
    root_url = 'http://racingpost.com'
    index_url = root_url + racecard['link']
    response = requests.get(index_url)
    soup = BeautifulSoup(response.text)

    meeting = Meeting(racecard['name'])

    # Retrieve the links for each of the races.
    race_links = soup.select('td.raceTitle a')
    for a in race_links:

        race_title = a.get_text()

        race_url = a.attrs.get('href')
        try:
            time, going, distance, runners, horses = parse_race(root_url + race_url)
        except:
            continue

        race = Race(race_title, time, going, distance, runners, horses)

        # Create a meeting and
        meeting.add_race(race)

    return meeting



class Meeting():
    def __init__(self, name):
        self.name = name
        self.races = []

    def add_race(self, race):
        self.races.append(race)


class Race():
    def __init__(self, name, time, going, distance, runners, horses):
        self.name = name
        self.horses = horses
        self.runners = runners
        self.going = going
        self.distance = distance
        self.time = time

    def get_distance_in_yards(self):
        total = 0

        pattern = re.compile('(\d+)(\w)')
        for distance in pattern.findall(self.distance):
            if distance[1] == 'm':
                total += int(distance[0]) * 8 * 220
            elif distance[1] == 'f':
                total += int(distance[0]) * 220
            elif distance[1] == 'y':
                total += int(distance[0])

        return total


class Horse():
    def __init__(self, number, name, weight, last_run):
        self.name = name
        self.number = number
        self.weight = weight
        self.forecast = 0
        self.last_run = last_run

    def forecast_odds_decimal(self):
        try:
            a, b = str(self.forecast).split('/')
            return (float(a) / float(b)) + 1
        except:
            return 0



if __name__ == '__main__':
    # Get a list of todays race cards.
    # These aren't race cards. This in a dictionary of meeting name,
    # and a link to the full list of races.
    racecards = get_todays_racecards()

    meetings = []

    # parse race card
    for racecard in racecards:
        meeting = parse(racecard)

        meetings.append(meeting)

        """
        print(meeting.name)
        for race in meeting.races:
            print('\t' + race.name, race.runners, race.distance)
            for horse in race.horses:
                print('\t\t' + horse.number, horse.name, horse.forecast, horse.last_run)
        """
