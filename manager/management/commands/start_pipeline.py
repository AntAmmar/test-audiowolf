from django.core.management.base import BaseCommand

from manager.tasks.download_videos import DownloadVideos


class Command(BaseCommand):
    help = 'Start pipeline'

    def handle(self, *args, **options):
        DownloadVideos().download_video()
