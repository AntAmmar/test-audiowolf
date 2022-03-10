import os
from time import sleep
from urllib.error import HTTPError

import openpyxl
from django.core.files import File

from audiowolf.settings import BASE_DIR, SPREADSHEET_FILE

from adverts.models import AdvertVideo, Brand

from pytube import YouTube


class DownloadVideos:
    @staticmethod
    def read_spreadsheet():
        wb = openpyxl.load_workbook(SPREADSHEET_FILE)
        ws = wb.active

        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i == 0:
                continue
            official_yt_link = row[7]
            name = row[6]
            brand = row[1]
            if official_yt_link:
                yield official_yt_link, name, brand
                continue

    def download(self, link):
        youtube: YouTube = YouTube(link)
        try:
            video = youtube.streams.get_highest_resolution()
            video.download(os.path.join(BASE_DIR, "media", "downloaded"))
            video_filename = video.default_filename
            return video_filename
        except HTTPError:
            sleep(60)
            return self.download(link)
        except Exception as exc:
            print(exc)
            return

    def download_video(self):
        links = self.read_spreadsheet()
        for link, name, brand_name in links:
            video_filename = self.download(link)
            if video_filename:
                brand, created = Brand.objects.get_or_create(name=brand_name)
                with open(os.path.join(BASE_DIR, "media", "downloaded", video_filename), 'rb') as video_file:
                    advert = AdvertVideo(brand=brand)
                    advert.video.save(video_filename, File(video_file))
