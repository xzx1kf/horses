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
    betting_forecast_list = pattern.findall(betting_forecast[0])
    return betting_forecast_list

def temp(list):
    newlist = []

    for entry in list:
        newlist.append((entry[1], entry[2]))
    return newlist

if __name__ == '__main__':
    betting_forecast_list = get_betting_forecast()
    list = temp(betting_forecast_list)
    odds, name = list[0]
    print("The odds are '%s', the name is '%s'" % (odds, name))
    print(betting_forecast_list[0][2])
