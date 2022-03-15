from django.core.management import BaseCommand

from manager.tasks.download_videos import DownloadVideos


class Command(BaseCommand):
    help = 'Push downloaded video to pipeline'

    def handle(self, *args, **options):
        DownloadVideos().push_video_to_pipeline()
