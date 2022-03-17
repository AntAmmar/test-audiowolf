from django import template

register = template.Library()

tasks = {
    'send_wav_to_acr_cloud': 'ACR Cloud',
    'spotify_get_tracks': 'Spotify',
    'musiio': 'Musiio',
    'chartmetric_task': 'Chartmetric'
}


@register.filter(name='map_task_name')
def map_task_name(value):
    return tasks[value]
