from django.shortcuts import render
from core.models import EventModel, EventCategory
from core.models import CompetitorModel
from datetime import datetime


def showcase(request, year: int = None):
    filter_by_year = year if year is not None else datetime.today().year
    context = {
        "is_live": EventModel.objects.filter(start_date=datetime.today()).exists(),
        "next_events": EventModel.objects.filter(start_date__gte=datetime.today()).order_by("start_date")[:5],
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
