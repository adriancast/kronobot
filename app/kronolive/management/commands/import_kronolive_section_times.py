import logging
import re
import time
import timedelta
from typing import Optional

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from requests.exceptions import RequestException
from telegram.error import RetryAfter

from core.models import (
    EventModel,
    SectionModel,
    InscriptionModel,
    SectionTimeModel,
    EventProvider,
)
from notification.telegram_notification_client import TelegramNotificationClient


class Command(BaseCommand):
    help = "Execute Kronolive section times synchronization"
    __TELEGRAM_SLEEP_AFTER_NOTIFICATION = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__telegram = TelegramNotificationClient(
            bot_token=settings.TELEGRAM_BOT_TOKEN,
            chat_id=settings.TELEGRAM_CHAT_ID,
        )

    def add_arguments(self, parser):
        parser.add_argument(
            "--sync", default="month", help="Use --sync all to sync all the partner data", type=str
        )
        parser.add_argument(
            "--notify",
            default="telegram",
            help="Use --notify telegram to send new times to telegram",
            type=str,
        )

    def handle(self, sync: str, notify: bool, *args, **options):
        min_start_date_filter = datetime.now() - datetime.timedelta(days=30)
        max_start_date_filter = datetime.now() + datetime.timedelta(days=30)
        events_to_sync = EventModel.objects.filter(
            start_date__gte=min_start_date_filter, start_date__lte=max_start_date_filter,
            provider_name=EventProvider.KRONOLIVE
        ).order_by("start_date")
        if sync == "all":
            events_to_sync = EventModel.objects.all().order_by("start_date")
        notify_telegram = notify == "telegram"
        for event in events_to_sync:
            self.__sync_event_times(event=event, notify_telegram=notify_telegram)

    def __sync_event_times(self, event: EventModel, notify_telegram: bool):
        try:
            response = requests.get(event.provider_data["times_url"], timeout=5)
        except RequestException as e:
            logging.exception(f"Exception updating section times. Reason: {e}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        filters_soup = soup.find("div", {"class": "filtro"})
        if not filters_soup:
            return
        category_soup = filters_soup.find_all("option")
        event_categories = [option["value"] for option in category_soup]
        for event_category in event_categories:
            kronolive_event_code = event.provider_data["times_url"].split("/")[-2]
            event_category_times_url = (
                f"http://www.kronolive.es/tiempos.aspx?p={kronolive_event_code}&c={event_category}"
            )
            try:
                response = requests.get(event_category_times_url, timeout=5)
            except RequestException as e:
                logging.exception(f"Exception updating section times. Reason: {e}")
                return None
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table")
            if not table:
                continue

            headers = [header.text for header in table.find_all("th")]
            verbose_section_names = {
                header.text: header.find("a").get("title") if header.find("a") else None
                for header in table.find_all("th")
            }
            results = [
                {headers[i]: cell for i, cell in enumerate(row.find_all("td"))}
                for row in table.find_all("tr")
            ]
            keys_that_are_not_section_names = (
                headers[0],
                headers[1],
                headers[-1],
            )

            keys_that_are_section_codes = [
                header for header in headers if header not in keys_that_are_not_section_names
            ]
            sections_mapper = {}
            for section_code in keys_that_are_section_codes:
                section, _ = SectionModel.objects.get_or_create(
                    name=verbose_section_names.get(section_code) or section_code,
                    code=section_code,
                    event=event,
                )
                sections_mapper[section_code] = section

            for result in results:
                if not result:
                    continue
                dorsal = result.get("#").text

                inscription = InscriptionModel.objects.filter(event=event, dorsal=dorsal).first()
                if not inscription:
                    continue

                section_code_time_mapper = {
                    section_name: self.__parse_time_cell(section_time)
                    for section_name, section_time in result.items()
                    if section_name not in keys_that_are_not_section_names
                }

                for section_code, section_time in section_code_time_mapper.items():
                    if section_time is not None:
                        with transaction.atomic():
                            _, created = SectionTimeModel.objects.get_or_create(
                                inscription=inscription,
                                section_time=section_time,
                                section=sections_mapper[section_code],
                            )
                        if created and notify_telegram:
                            try:
                                self.__telegram.notify_time(
                                    pilot_name=inscription.pilot.name,
                                    copilot_name=inscription.copilot.name if inscription.copilot else None,
                                    car=inscription.car,
                                    section_name=verbose_section_names.get(section_code)
                                    or section_code,
                                    section_time=section_time,
                                    image_url=inscription.car_image(),
                                )
                                time.sleep(self.__TELEGRAM_SLEEP_AFTER_NOTIFICATION)
                            except RetryAfter as e:
                                time.sleep(e.retry_after)

    def __parse_time_cell(self, time_cell_soup) -> Optional[str]:
        text = time_cell_soup.get_text(separator="!", strip=True)
        if text is None:
            return None
        if ":" not in text:
            return None

        time_text = text.split("!")[0]
        cleaned_duration = time_text.split(".")[0]

        text_contains_a_section_time = any(char.isdigit() for char in cleaned_duration)
        if not text_contains_a_section_time:
            return None

        if re.match("[ˆ0-9][0-9]:[0-5][0-9]$", cleaned_duration):
            return f"00:{cleaned_duration}"

        if re.match("[ˆ0-9][0-9]:[0-5][0-9]:[0-5][0-9]$", cleaned_duration):
            return f"{cleaned_duration}"

        logging.exception(f"Could not parse time cell. Soup: {time_cell_soup}")
