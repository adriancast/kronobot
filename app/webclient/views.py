from django.shortcuts import render
from core.models import EventModel, EventCategory, InscriptionModel
from core.models import CompetitorModel
from datetime import datetime


def showcase(request, year: int = None):
    filter_by_year = year if year is not None else datetime.today().year
    today = datetime.today()
    context = {
        "is_live": EventModel.objects.filter(start_date__lte=today, end_date__gte=today).exists(),
        "next_events": EventModel.objects.filter(end_date__gte=datetime.today()).order_by(
            "start_date"
        )[:5],
        "rallyes": EventModel.objects.filter(
            category=EventCategory.RALLY, start_date__year=filter_by_year
        ).order_by("start_date"),
        "pujades": EventModel.objects.filter(
            category=EventCategory.HILL_CLIMB, start_date__year=filter_by_year
        ).order_by("start_date"),
        "karting": EventModel.objects.filter(
            category=EventCategory.KARTING, start_date__year=filter_by_year
        ).order_by("start_date"),
        "autocross": EventModel.objects.filter(
            category=EventCategory.AUTO_CROSS, start_date__year=filter_by_year
        ).order_by("start_date"),
        "competitors": CompetitorModel.objects.exclude(photo="")[:10],
        "historic": sorted(
            EventModel.objects.values_list("start_date__year", flat=True).distinct(), reverse=True
        ),
    }
    return render(request, "home.html", context)
    


def events(request, event_id: int = None):
    event = EventModel.objects.get(id=event_id)
    context = {
        "event": event,
        "event_description": (
            """🕘 12:33
            📍Puig major"""
        ),
        "inscriptions": InscriptionModel.objects.filter(event=event),
    }
    return render(request, 'events.html', context)

def competitors(request, competitor_id):
    competitor = CompetitorModel.objects.get(id=competitor_id)
    inscriptions_driving = InscriptionModel.objects.filter(pilot=competitor)
    total_events_driving = len(inscriptions_driving)
    inscriptions_codriving = InscriptionModel.objects.filter(copilot=competitor)
    total_events_codriving = len(inscriptions_codriving)
    total_events = total_events_driving + total_events_codriving

    comptetitor_events = [inscription.event for inscription in  inscriptions_driving]
    comptetitor_events += [inscription.event for inscription in  inscriptions_codriving]
    comptetitor_events = list(set(comptetitor_events))

    last_competition_inscription = InscriptionModel.objects.filter(pilot=competitor).last()
    car = None
    if last_competition_inscription:
        car = last_competition_inscription.car
    context={
        "competitor": competitor,
        "total_events": total_events,
        "total_events_driving": total_events_driving,
        "total_events_codriving": total_events_codriving,
        "car": car,
        "events": comptetitor_events,

    }
    return render(request, 'competitors.html', context)

def historic(request, year: int = None):
    filter_by_year = year if year is not None else datetime.today().year
    today = datetime.today()
    context = {
        "rallyes": EventModel.objects.filter(
            category=EventCategory.RALLY, start_date__year=filter_by_year
        ).order_by("start_date"),
        "pujades": EventModel.objects.filter(
            category=EventCategory.HILL_CLIMB, start_date__year=filter_by_year
        ).order_by("start_date"),
        "karting": EventModel.objects.filter(
            category=EventCategory.KARTING, start_date__year=filter_by_year
        ).order_by("start_date"),
        "autocross": EventModel.objects.filter(
            category=EventCategory.AUTO_CROSS, start_date__year=filter_by_year
        ).order_by("start_date"),
        "historic": sorted(
            EventModel.objects.values_list("start_date__year", flat=True).distinct(), reverse=True
        ),
        "year": year,
    }
    return render(request, "historic.html", context)