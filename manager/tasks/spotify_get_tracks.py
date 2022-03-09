import requests

from adverts.models import AdvertVideoStatus, Status
from audiowolf.celery import app

from manager.tasks import BaseTask
from manager.tasks.musiio import MusiioTask

CLIENT_ID = 'd7b5d544859446389b016ea2194cf30e'
CLIENT_SECRET = '56d74311e9374cdea2a5dce7bf362c2f'

AUTH_URL = 'https://accounts.spotify.com/api/token'


class SpotifyGetTracksTask(BaseTask):
    name = 'spotify_get_tracks'
    callback = None

    def execute(self, *args, **kwargs):
        advert_id = kwargs.get('id')
        track_id = kwargs.get('track_id')
        AdvertVideoStatus.objects.get(advert_id=advert_id).update_upload_video(Status.IN_PROGRESS)
        auth_response = requests.post(AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })

        auth_response_data = auth_response.json()
        access_token = auth_response_data['access_token']
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        BASE_URL = 'https://api.spotify.com/v1/'

        search_response = requests.get(BASE_URL + 'tracks/' + track_id, headers=headers)
        # audio_analysis_response = requests.get(BASE_URL + 'audio-analysis/' + track_id, headers=headers)
        audio_features_response = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
        AdvertVideoStatus.objects.get(advert_id=advert_id).update_spotify_get_tracks(Status.SUCCESS)
        kwargs['spotify_artist_urls'] = [artist.get('external_urls').get('spotify') for artist in search_response.json().get('artists')]
        MusiioTask.delay(**kwargs)
        return {
            'search_response': search_response.json(),
            # 'audio_analysis_response': audio_analysis_response.json(),
            'audio_features_response': audio_features_response.json()
        }


SpotifyGetTracksTask = app.register_task(SpotifyGetTracksTask())
