from django.shortcuts import render
from core.models import EventModel, EventCategory
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
    


def events(request):
    context = {
        "escuderia":[
            { "name":"E.MCA.Competició", "id":1,},
            { "name":"E.COSTA NORD", "id":2,},
            { "name":"FAIB", "id":3,},
            { "name":"P.A.S.Q.", "id":4,},
            { "name":"E.SANT SALVADOR", "id":5,},
            { "name":"E.MANACOR", "id":6,},
            { "name":"M.C.S.R.P", "id":7,},
            { "name":"E.MITJA ILLA", "id":8,},
            { "name":"A.C.I.F", "id":9,},
            { "name":"E.SERRA TRAMUNTANA", "id":10,},
            { "name":"E.BUNYOLA", "id":11,},
        ]
    }
    return render(request, 'event.html', context)