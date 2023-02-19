from django.shortcuts import render
from core.models import EventModel, EventCategory
from core.models import CompetitorModel
from datetime import datetime


def showcase(request, year: int = None):
    filter_by_year = year if year is not None else datetime.today().year
    context = {
        "is_live": EventModel.objects.filter(date=datetime.today()).exists(),
        "next_events": EventModel.objects.filter(date__gte=datetime.today()).order_by("date")[:5],
        "rallyes": EventModel.objects.filter(
            category=EventCategory.RALLY, date__year=filter_by_year
        ).order_by("date"),
        "pujades": EventModel.objects.filter(
            category=EventCategory.HILL_CLIMB, date__year=filter_by_year
        ).order_by("date"),
        "karting": EventModel.objects.filter(
            category=EventCategory.KARTING, date__year=filter_by_year
        ).order_by("date"),
        "autocross": EventModel.objects.filter(
            category=EventCategory.AUTO_CROSS, date__year=filter_by_year
        ).order_by("date"),
        "competitors": CompetitorModel.objects.exclude(photo="")[:10],
        "historic": sorted(
            EventModel.objects.values_list("date__year", flat=True).distinct(), reverse=True
        ),
    }
    return render(request, "home.html", context)
