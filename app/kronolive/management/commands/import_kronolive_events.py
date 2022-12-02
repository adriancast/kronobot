import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from requests import RequestException

from core.models import EventModel


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

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
        url = f"http://kronolive.es/default.aspx?a={year}"
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
            EventModel.objects.get_or_create(
                name=event_name,
                date=datetime.strptime(date, "%d/%m/%Y"),
                kronolive_times_url=f"http://kronolive.es{kronolive_times_url}",
                kronolive_inscribed_url=f"http://kronolive.es{kronolive_inscribed_url}",
            )
