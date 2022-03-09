import json

from adverts.models import AdvertVideoStatus, Status

from manager.scripts.import_musiio_data import ImportMusiioData

from audiowolf.celery import app

from manager.tasks import BaseTask
from manager.tasks.chartmetric import ChartmetricTask


class MusiioTask(BaseTask):
    name = 'musiio'
    callback = None

    def execute(self, *args, **kwargs):
        advert_id = kwargs.get('id')
        youtube_id = kwargs['youtube_id']
        AdvertVideoStatus.objects.get(advert_id=advert_id).update_musiio(Status.IN_PROGRESS)

        musiio_response: dict = ImportMusiioData.run(youtube_id)
        for spotify_artist_url in kwargs['spotify_artist_urls']:
            kwargs['spotify_artist_url'] = spotify_artist_url
            ChartmetricTask.delay(**kwargs)
        AdvertVideoStatus.objects.get(advert_id=advert_id).update_musiio(Status.SUCCESS)
        return musiio_response


MusiioTask = app.register_task(MusiioTask())
