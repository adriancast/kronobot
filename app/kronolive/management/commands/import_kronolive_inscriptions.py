import logging
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.db.models import Q
from requests import RequestException
from core.models import EventModel, InscriptionModel, CompetitorModel, EventProvider


class Command(BaseCommand):
    help = "Execute Kronolive inscriptions synchronization"

    def add_arguments(self, parser):
        parser.add_argument(
            "--sync", default="month", help="Use --sync all to sync all the partner data"
        )

    def handle(self, sync: str, *args, **options):
        min_start_date_filter = datetime.now() - timedelta(days=30)
        max_start_date_filter = datetime.now() + timedelta(days=30)
        events_to_sync = EventModel.objects.filter(
            Q(start_date__gte=min_start_date_filter, end_date__lte=max_start_date_filter) |
            Q(start_date__lte=max_start_date_filter, end_date__gte=min_start_date_filter),
            provider_name=EventProvider.KRONOLIVE
        ).order_by("start_date")
        if sync == "all":
            events_to_sync = EventModel.objects.all().order_by("start_date")

        for event in events_to_sync:
            self.__sync_event_inscriptions(event)

    def __sync_event_inscriptions(self, event: EventModel):
        try:
            response = requests.get(event.provider_data["inscribed_url"], timeout=5)
        except RequestException as e:
            logging.exception(f"Exception updating inscriptions. Reason: {e}")
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        if not table:
            return

        headers = [header.text for header in table.find_all("th")]
        results = [
            {headers[i]: cell for i, cell in enumerate(row.find_all("td"))}
            for row in table.find_all("tr")
        ]

        for result in results:
            dorsal_soup = result.get("D.")
            pilot_soup = result.get("Piloto")
            car_soup = result.get("Vehiculo")
            category_soup = result.get("Gr.")

            if not all(
                [
                    dorsal_soup,
                    pilot_soup,
                    car_soup,
                    category_soup,
                ]
            ):
                continue

            pilots_separator = "!"
            pilots_text = pilot_soup.get_text(separator=pilots_separator, strip=True)
            if pilots_separator in pilots_text:
                pilots_names = pilots_text.split(pilots_separator)
                pilot_name = pilots_names[0]
                copilot_name = pilots_names[1]
            else:
                pilot_name = pilots_text
                copilot_name = None

            category = category_soup.text.strip()
            dorsal = dorsal_soup.text.strip()
            car = car_soup.text.strip()

            pilot, _ = CompetitorModel.objects.get_or_create(name=pilot_name)
            copilot = None
            if copilot_name:
                copilot, _ = CompetitorModel.objects.get_or_create(name=copilot_name)

            InscriptionModel.objects.get_or_create(
                car=car,
                category=category,
                dorsal=dorsal,
                event=event,
                pilot=pilot,
                copilot=copilot,
            )
