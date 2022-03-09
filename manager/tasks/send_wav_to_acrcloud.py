import base64
import hashlib
import hmac
import os
import time

import requests
from audiowolf.settings import MEDIA_ROOT

from adverts.models import AdvertVideoStatus, Status
from audiowolf.celery import app

from manager.tasks import BaseTask
from manager.tasks.spotify_get_tracks import SpotifyGetTracksTask


class SendWavToAcrCloudTask(BaseTask):
    name = 'send_wav_to_acr_cloud'
    callback = None

    def execute(self, *args, **kwargs):
        advert_id = kwargs.get('id')
        audio_path = kwargs.get('audio_path')
        audio_absolute_path = os.path.join(MEDIA_ROOT, 'video', audio_path)
        AdvertVideoStatus.objects.get(advert_id=advert_id).update_send_acr_cloud(Status.IN_PROGRESS)

        access_key = '51c1b46567d00a81aa1bc5fe9298c55e'
        access_secret = 'wnZxwgZ9ASgy6nAJE0MBf0lelv5a624mvhq4aWxe'
        requrl = "http://identify-eu-west-1.acrcloud.com/v1/identify"

        http_method = "POST"
        http_uri = "/v1/identify"
        data_type = "audio"
        signature_version = "1"
        timestamp = time.time()

        string_to_sign = http_method + "\n" + http_uri + "\n" + access_key + "\n" + data_type + "\n" + signature_version + "\n" + str(
            timestamp)

        sign = base64.b64encode(hmac.new(access_secret.encode('ascii'), string_to_sign.encode('ascii'),
                                         digestmod=hashlib.sha1).digest()).decode('ascii')

        files = [
            ('sample', ('test.mp3', open(audio_absolute_path, 'rb'), 'audio/mpeg'))
        ]
        data = {'access_key': access_key,
                'sample_bytes': os.path.getsize(audio_absolute_path),
                'timestamp': str(timestamp),
                'signature': sign,
                'data_type': data_type,
                "signature_version": signature_version}

        response = requests.post(requrl, files=files, data=data)
        songs = response.json().get('metadata').get('music')
        for song in songs:
            spotify_id = song.get('external_metadata').get('spotify').get('track').get('id')
            kwargs['track_id'] = spotify_id
            kwargs['youtube_id'] = song.get('external_metadata').get('youtube').get('vid')
            SpotifyGetTracksTask.delay(**kwargs)
        AdvertVideoStatus.objects.get(advert_id=advert_id).update_send_acr_cloud(Status.SUCCESS)
        return response.json()


SendWavToAcrCloudTask = app.register_task(SendWavToAcrCloudTask())
