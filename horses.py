import bs4
import re
import requests

# At the moment the index_url contains all the card information for the day. This may have to change.
root_url = 'http://www.racingpost.com'
index_url = root_url + '/horses2/cards/meeting_of_cards.sd?crs_id=10&r_date=2015-01-08&tab=sc_'

def get_betting_forecast():
    """Return the betting forecast as a list."""
    # For testing purposes the following two lines are commented out. This is because the
    # web page has been saved to disk.
    #response = requests.get(index_url)
    #soup = bs4.BeautifulSoup(response.text)
    soup = bs4.BeautifulSoup(open('/home/nick/downloads/test.html'))                                        # Temporary

    # Return a list of all <p> tags that have an id beginning with "bettingForecastContainer".
    betting_forecast = [a.get_text() for a in soup.select('div.info >  p[id^="bettingForecastContainer"]')]

    # The regex pattern matches against the following, "2/1 Horse Name,"
    pattern = re.compile('((\d+/\d+)\s(.+?)),')

    # This will need changing. At the moment it is a hard-coded slection on which card to
    # find all the matches against.
    betting_forecast_dict = {}

    # Create a dictionary of the betting forecast.
    for entry in pattern.findall(betting_forecast[0]):
        betting_forecast_dict[entry[1]] = entry[2]
    return betting_forecast_dict

if __name__ == '__main__':
    betting_forecast_dict = get_betting_forecast()
    for name, odds in betting_forecast_dict.items():
        print(name, odds)
