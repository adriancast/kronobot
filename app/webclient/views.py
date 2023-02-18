from django.shortcuts import render
from core.models import EventModel, EventCategory
from core.models import CompetitorModel
from datetime import datetime


def home(request):         
    context = {
        "is_live": EventModel.objects.filter(date=datetime.today()).exists(),
        "next_events": EventModel.objects.order_by('-date')[:5],
        "rallyes": EventModel.objects.filter(category=EventCategory.RALLY).order_by('-date'),
        "pujades": EventModel.objects.filter(category=EventCategory.HILL_CLIMB).order_by('-date'),
        "karting": EventModel.objects.filter(category=EventCategory.KARTING).order_by('-date'),
        "autocross": EventModel.objects.filter(category=EventCategory.AUTO_CROSS).order_by('-date'),
        "competitors": CompetitorModel.objects.exclude(photo="")[:10],
        "historic": sorted(EventModel.objects.values_list("date__year", flat=True).distinct(), reverse=True)
    }
    return render(request, 'home.html', context)
