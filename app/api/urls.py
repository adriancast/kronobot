from ninja import NinjaAPI
from core.models import EventModel
from core.models import InscriptionModel

api = NinjaAPI(title="Kronobot API", version="1.0.0")

@api.get("/events")
def all_events(request):
    results = []
    for event in EventModel.objects.filter():
        results.append({
            "name": event.name,
            "picture": event.picture.url if event.picture else None,
            "start_date": event.start_date,
            "end_date": event.end_date,
            "description": event.description,
            "category": event.category,
            "id": event.id,
            "is_live": event.is_live(),
        })
    return {"events": results}


@api.get("/events/{event_id}/inscriptions")
def event_inscriptions(request, event_id: int):
    result = []
    for inscription in InscriptionModel.objects.filter(event_id=event_id):
        result.append({
            "car": inscription.car,
            "category": inscription.category,
            "dorsal": inscription.dorsal,
            "pilot": inscription.pilot.name,
            "copilot": inscription.copilot.name,
        })
    return {"inscriptions": result }


