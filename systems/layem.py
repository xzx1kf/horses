class Layem():
    def __init__(self, meetings):
        self.meetings = meetings

    def is_flat_or_aw(self, race):
        terms = ['chase']
        for term in terms:
            if term in race.name.lower():
                return False
        return True

    def is_handicap(self, race):
        term = 'handicap'
        race_title = race.name.lower()
        race_title = race_title.split()
        return term in race_title

    def has_11_to_16_runners(self, race):
        return int(race.runners) >= 11 and int(race.runners) <= 16

    def check_going(self, race):
        terms = ['good', 'good to firm', 'good to soft', 'standard']
        for term in terms:
            if term in race.going.lower():
                return True

    def is_distance_less_than_10f(self, race):
        return race.get_distance_in_yards() < 2220

    def is_horse_in_top_5_weights(self, horse):
        return int(horse.number) in range(6)

    def horse_last_ran_8_days_ago_or_more(self, horse):
        return int(horse.last_run) >= 8

    def forecast_odds_in_range(self, horse):
        odds = horse.forecast_odds_decimal()
        return odds >= 4 and odds <= 7.5

    def run(self):
        for meeting in self.meetings:
            print(meeting.name)
            for race in meeting.races:
                if self.is_flat_or_aw(race):
                    if self.is_handicap(race):
                        if self.has_11_to_16_runners(race):
                            if self.check_going(race):
                                if self.is_distance_less_than_10f(race):
                                    print('\t' + race.time, race.name, self.is_handicap(race), race.runners, race.distance)
                                    for horse in race.horses:
                                        if not self.is_horse_in_top_5_weights(horse):
                                            if self.horse_last_ran_8_days_ago_or_more(horse):
                                                if self.forecast_odds_in_range(horse):
                                                    print('\t\t' + horse.number, horse.name, horse.last_run, horse.forecast)


if __name__ == '__main__':
    """
    from horses import get_todays_racecards
    from horses import parse

    racecards = get_todays_racecards()
    meetings = []
    for racecard in racecards:
        meeting = parse(racecard)
        meetings.append(meeting)
    """
    import pickle

    #pickle.dump(meetings, open('../data/150115', 'wb'))
    meetings = pickle.load(open('../data/150115', 'rb'))
    layem = Layem(meetings)

    for meeting in meetings:
        print(meeting.name)
        for race in meeting.races:
            print('\t' + race.time, race.name, layem.is_handicap(race), race.runners, race.distance)
            for horse in race.horses:
                print('\t\t' + horse.number, horse.name, horse.last_run, horse.forecast)


