from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = 'AIzaSyAEW6eclU1735ApKjKmgAhSAz5-JhjU9ho'

YOUTUBE_API_SERVICE_NAME = 'youtube'

YOUTUBE_API_VERSION = 'v3'


def youtube_search(artist_name, song_name):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q='"' + artist_name + ' - ' + song_name + '"',
        part='id,snippet',
        maxResults=1
    ).execute()

    print(search_response)


if __name__ == '__main__':
    try:
        youtube_search('senidah', 'behute')
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
