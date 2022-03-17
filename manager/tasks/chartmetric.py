import requests

from adverts.models import Status, AdvertVideoStatus

from audiowolf.celery import app

from manager.tasks import BaseTask

REFRESH_TOKEN = 'IBLeIXD5SR3DxhAvKW7NB2ktc9oX0XGE8tZtFgg96SCQJKkSMImZxhHyUROuGRke'
BASE_URL = 'https://api.chartmetric.com/api'
AUTH_URL = BASE_URL + '/token'
CHARTMETRIC_SEARCH_URL = BASE_URL + '/search'


class ChartmetricTask(BaseTask):
    name = 'chartmetric_task'
    callback = None

    def read_responses(self, advert_id, spotify_artist_url, headers):
        get_artist = requests.get(CHARTMETRIC_SEARCH_URL, params={'q': spotify_artist_url}, headers=headers)
        artist_id = get_artist.json().get('obj').get('artists')[0].get('id')

        artist_cpp = requests.get(BASE_URL + '/artist/' + str(artist_id) + '/cpp',
                                  params={'stat': 'score'},
                                  headers=headers)
        cpp = artist_cpp.json()
        AUDIENCE_URL = BASE_URL + '/artist/' + str(artist_id) + '/instagram-audience-stats'
        audience_data = requests.get(AUDIENCE_URL, headers=headers)
        audience = audience_data.json()
        AdvertVideoStatus.objects.get(advert_id=advert_id).update_chartmetric(Status.SUCCESS)
        return {
            'cpp': cpp,
            'audience': audience
        }

    def execute(self, *args, **kwargs):
        advert_id = kwargs.get('id')
        spotify_artist_url = kwargs.get('spotify_artist_url')
        AdvertVideoStatus.objects.get(advert_id=advert_id).update_chartmetric(Status.IN_PROGRESS)
        auth_response = requests.post(AUTH_URL, {
            'refreshtoken': REFRESH_TOKEN,
        })

        auth_response_data = auth_response.json()
        access_token = auth_response_data['token']

        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        return self.read_responses(advert_id, spotify_artist_url, headers)


ChartmetricTask = app.register_task(ChartmetricTask())
