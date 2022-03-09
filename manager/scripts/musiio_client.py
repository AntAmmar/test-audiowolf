import requests
from requests.auth import HTTPBasicAuth

from audiowolf.settings import MUSIIO_API_KEY


class MusiioExtractionService:
    def __init__(self, youtube_url: str):
        self.audio_link = youtube_url
        self.api_key = MUSIIO_API_KEY

    def extract_tags(self, uploaded_track_id):
        extract_tags_response = requests.post(
            'https://api-us.musiio.com/api/v1/extract/tags/',
            json={
                'id': uploaded_track_id,
                'tags': [
                    "CONTENT TYPE", "GENRE", "GENRE V2", "GENRE V3", "MOOD", "BPM", "KEY", "KEY SHARP", "KEY FLAT",
                    "ENERGY", "INSTRUMENTATION"
                ]
            },
            auth=HTTPBasicAuth(self.api_key, '')
        )
        return extract_tags_response.json()

    def get_tags(self):
        upload_response = requests.post('https://api-us.musiio.com/api/v1/upload/audio-link',
                                        json={'link': self.audio_link},
                                        auth=HTTPBasicAuth(self.api_key, '')
                                        )
        tags_response = self.extract_tags(upload_response.json().get('id'))
        return tags_response.get('tags')
