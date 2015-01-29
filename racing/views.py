from django.db.models import Q
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from datetime import datetime, timedelta
from racing.models import Meeting, Race, Horse
from collections import OrderedDict

def index(request):
    meetings = Meeting.objects.filter(date__gte=(datetime.today() - timedelta(days=2)))
    meeting_dates = set([m.date for m in meetings])             # Create a set of meeting dates.
    meetings_separated = dict([(d, []) for d in meeting_dates]) # Initialise an empty list for each date.
    for d in meeting_dates:                                     # Separate out the meetings into a
        for m in meetings:                                      # dictionary by index date with a list of meetings.
            if m.date == d:
                meetings_separated[d].append(m)
    meetings_separated = OrderedDict(sorted(meetings_separated.items(), reverse=True))
    return render(request, 'racing/index.html', {"meetings_separated": meetings_separated})

def meeting_detail(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    races = get_list_or_404(Race, meeting=meeting)
    return render(request, 'racing/meeting_detail.html', {'meeting': meeting, 'races': races})

def layem(request):
    races = Race.objects.filter(meeting__date=datetime.today())
    races = races.filter(distance__lt=2200, distance__gte=0)
    races = races.filter(runners__lte=16, runners__gte=11)
    races = races.filter(name__icontains='handicap')
    races = races.filter(
        Q(going__icontains='standard') | Q(going__icontains='good')
    )
    races = races.exclude(name__icontains='chase').exclude(name__icontains='hurdle')

    for race in races:
        race.horses = race.horses.exclude(number__lte=5)
        race.horses = race.horses.filter(last_run__gte=8)
        race.horses = race.horses.filter(forecast__gte=5, forecast__lte=8.5)

    return render(request, 'racing/layem.html', {'races': races})

def update(request):
    # For a waiting page use celery.
    from parsers.horses import get_todays_racecards, parse
    racecards = get_todays_racecards()
    meetings = []
    for racecard in racecards:
        meeting = parse(racecard)
        meetings.append(meeting)

        m = Meeting(name=meeting.name, date=datetime.today().date())
        m.save()

        for race in meeting.races:
            yards = race.get_distance_in_yards()
            rtime = datetime.strptime(race.time + " pm", "%I:%M %p")
            rdate = datetime.today().date()
            r = Race(
                date=datetime.combine(rdate, rtime.time()),
                distance=yards,
                going=race.going,
                meeting=m,
                name=race.name,
                runners=race.runners)
            r.save()

            for horse in race.horses:
                h = Horse(
                    forecast=horse.forecast_odds_decimal(),
                    last_run=horse.last_run,
                    name=horse.name,
                    number=horse.number,
                    weight=horse.weight)
                h.save()

                r.horses.add(h)

    return redirect('racing:index')

def delete_todays_meetings(request):
    meetings = Meeting.objects.filter(date=datetime.today().date())
    for meeting in meetings:
        meeting.delete()

    return redirect('racing:index')
