import threading
from datetime import datetime
import time
from typing import Dict
import pytz as pytz
import requests

from models.base_player_parameters import BasePlayerParameters
from services.base_player import BasePlayer
from services.chromecast_player import ChromeCastPlayer
from util.enums import PrayerTimeCalculationMethod
from util.util import time_until_end_of_day


class AthanSchedulingService:

    def __init__(self, timezone: str = "America/New_York", method: PrayerTimeCalculationMethod = 2, lat: float = 0,
                 long: float = 0,
                 city: str = "NEW YORK",
                 player: BasePlayer = ChromeCastPlayer(BasePlayerParameters(
                     media_url='https://drive.google.com/uc?export=download&id=1kC8afyTAJPTZm3RtmgSu2Io5mhTkNvNd'))):
        self.timezone: str = timezone
        self.method: PrayerTimeCalculationMethod = method
        self.lat: float = lat
        self.long: float = long
        self.city: str = city
        self.tz: pytz.tzinfo = pytz.timezone(timezone)
        self.last_checked_time: datetime = None
        self.player = player
        self._current_timings: Dict[str, str] = self.retrieve_daily_time()

    def daily_reschedule(self):
        """
        :return:
        """
        self.retrieve_daily_time()
        fajr_thread = threading.Thread(target=self.schedule_athan, args=("Fajr Athan", self.get_fajr_time()),
                                       daemon=True)
        dhuhr_thread = threading.Thread(target=self.schedule_athan, args=("Dhuhr Athan", self.get_dhuhr_time()),
                                        daemon=True)
        asr_thread = threading.Thread(target=self.schedule_athan, args=("Asr Athan", self.get_asr_time()),
                                      daemon=True)
        maghrib_thread = threading.Thread(target=self.schedule_athan, args=("Maghrib Athan", self.get_maghrib_time()),
                                          daemon=True)
        isha_thread = threading.Thread(target=self.schedule_athan, args=("Isha Athan", self.get_isha_time()),
                                       daemon=True)
        fajr_thread.start()
        dhuhr_thread.start()
        asr_thread.start()
        maghrib_thread.start()
        isha_thread.start()

        time_till_tomorrow_s = time_until_end_of_day()
        time.sleep(time_till_tomorrow_s)

    def schedule_athan(self, text, t):
        now = datetime.now(self.tz)
        seconds_remaining = (t - now).total_seconds()
        while seconds_remaining > 0:
            now = datetime.now(self.tz)
            seconds_remaining = (t - now).total_seconds()
            print(f"{text} - {seconds_remaining} seconds remaining\n")
            time.sleep(5)
        print(f"{text} - Triggering Athan\n")
        self.player.playAthan()

    def loop(self):
        try:
            while True:
                self.daily_reschedule()
        except KeyboardInterrupt:
            print('interrupted!')

    def _get_url(self):
        current_time = datetime.now(self.tz)

        if self.last_checked_time is None or current_time.date() != self.last_checked_time.date():
            self.last_checked_time = current_time

        return f"http://api.aladhan.com/v1/timings/{self.last_checked_time}?latitude=35.890980&longitude=-78.830880&method=1"

    def retrieve_daily_time(self):
        r = requests.get(self._get_url())
        if r.status_code == 200:
            return r.json()["data"]["timings"]

    def get_fajr_time(self):
        return self.convert_to_datetime(self._current_timings["Fajr"])

    def get_dhuhr_time(self):
        return self.convert_to_datetime(self._current_timings["Dhuhr"])

    def get_asr_time(self):
        return self.convert_to_datetime(self._current_timings["Asr"])

    def get_maghrib_time(self):
        return self.convert_to_datetime(self._current_timings["Maghrib"])

    def get_isha_time(self):
        return self.convert_to_datetime(self._current_timings["Isha"])

    def convert_to_datetime(self, t):
        tval = time.strptime(t, "%H:%M")
        return datetime.now(self.tz).replace(hour=tval.tm_hour, minute=tval.tm_min, second=0, microsecond=0)


AthanSchedulingService().loop()
