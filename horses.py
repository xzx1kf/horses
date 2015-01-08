import requests
#response = requests.get('http://www.racingpost.com/horses2/cards/card.sd?race_id=615958&r_date=2015-01-07#raceTabs=sc_')
#response = requests.get('http://www.racingpost.com/horses2/cards/meeting_of_cards.sd?crs_id=10&r_date=2015-01-08&tab=sc_')

import bs4
#soup = bs4.BeautifulSoup(response.text)
soup = bs4.BeautifulSoup(open('/home/nick/downloads/test.html'))
bettingForecast = [a.get_text() for a in soup.select('div.info >  p[id^="bettingForecastContainer"]')]

import re
pattern = re.compile('((\d+/\d+)\s(.+?)),')
h = pattern.findall(bettingForecast[0])
print(h)
