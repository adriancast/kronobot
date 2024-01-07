import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from requests import RequestException

from core.models import EventModel, EventProvider, EventCategory


class Command(BaseCommand):
    help = "Try to link kronolive events with our local events database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--sync", default="month", help="Use --sync all to sync all the partner data", type=str
        )

    def handle(self, sync: str, *args, **options):
        current_year = datetime.now().year
        years_to_process = [current_year]
        if sync == "all":
            years_to_process = list(range(2012, current_year + 1))

        for year in years_to_process:
            self.__sync_events_year(year)

    def __sync_events_year(self, year: int) -> None:
        url = f"http://www.kronolive.es/default.aspx?a={year}"
        try:
            response = requests.get(url, timeout=5)
        except RequestException as e:
            logging.exception(f"Exception updating events. Reason: {e}")
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
            name_soup = result.get("Nombre")
            date_soup = result.get("Fecha")
            if not all([name_soup, date_soup]):
                continue

            kronolive_base_url = name_soup.find("a")["href"]

            kronolive_times_url = kronolive_base_url.replace("TiemposOnline", "Tiempos")
            kronolive_inscribed_url = kronolive_base_url.replace(
                "TiemposOnline", "ListaDeInscritos"
            )

            date = date_soup.text.strip()
            event_name = name_soup.text.strip()
            kronolive_times_url = f"http://www.kronolive.es{kronolive_times_url}"
            kronolive_inscribed_url = f"http://www.kronolive.es{kronolive_inscribed_url}"
            category = self.__decide_event_category(event_name)

            try:
                kronobot_event = EventModel.objects.get(
                    start_date=datetime.strptime(date, "%d/%m/%Y"),
                    category=category,
                )

                kronobot_event.provider_name = EventProvider.KRONOLIVE
                kronobot_event.provider_data = {
                    "times_url": kronolive_times_url,
                    "inscribed_url": kronolive_inscribed_url,
                }
                kronobot_event.save()
            except EventModel.DoesNotExist:
                pass

    def __decide_event_category(self, event_name: str):
        lower_event_name = event_name.lower()
        if "pujada" in lower_event_name:
            return EventCategory.HILL_CLIMB

        if "tierra" in lower_event_name:
            return EventCategory.AUTO_CROSS

        return EventCategory.RALLY
