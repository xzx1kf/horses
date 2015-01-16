#!/bin/python

import argparse
from datetime import date
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--display", help="Display the working dataset.", action="store_true")
parser.add_argument("-s", "--system", help="Run the named SYSTEM against the current dataset.")
parser.add_argument("-u", "--update", help="Update the working dataset.",
                    action="store_true")
args = parser.parse_args()

if args.update:
    from parsers.horses import get_todays_racecards
    from parsers.horses import parse

    racecards = get_todays_racecards()
    meetings = []
    for racecard in racecards:
        meeting = parse(racecard)
        meetings.append(meeting)

    db_name = date.today().isoformat()

    pickle.dump(meetings, open('./data/' + db_name + '.db', 'wb'))
elif args.system:
    if args.system == 'layem':
        from systems.layem import Layem
        db_name = date.today().isoformat()
        meetings = pickle.load(open('./data/' + db_name + '.db', 'rb'))
        layem = Layem(meetings)
        layem.run()
    else:
        print("The specified system is not recognised.")
elif args.display:
    import pickle

    db_name = date.today().isoformat()
    meetings = pickle.load(open('./data/' + db_name + '.db', 'rb'))

    for meeting in meetings:
        print(meeting.name)
        for race in meeting.races:
            print('\t' + race.time, race.name, race.runners, race.distance)
            for horse in race.horses:
                print('\t\t' + horse.number, horse.name, horse.last_run, horse.forecast)
else:
    parser.print_help()
