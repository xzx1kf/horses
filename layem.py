class Layem():
    def __init__(self, meetings):
        self.meetings = meetings

    def is_handicap(self):
        return True

if __name__ == '__main__':
    from horses import get_todays_racecards

    #meetings = get_todays_racecards()
    import pickle

    #pickle.dump(meetings, open('140115', 'wb'))
    meetings = pickle.load(open('140115', 'rb'))
    layem = Layem(meetings)
    print(layem.is_handicap())

