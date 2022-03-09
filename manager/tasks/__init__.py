import logging
from celery import Task, group

from adverts.models import AdvertTask

logger = logging.getLogger(__name__)

__all__ = [
    'BaseTask', 'DispatchTask', 'UploadVideoTask', 'ConvertAudioToWavTask', 'SplitAudioFilesTask',
    'SendWavToAcrCloudTask', 'SpotifyGetTracksTask', 'MusiioTask', 'ChartmetricTask',
]


class BaseTask(Task):
    abstract = True
    # ----------
    name = None
    callback = None

    def execute(self, *args, **kwargs):
        raise NotImplementedError

    def run(self, *args, **kwargs):
        local_params = locals()
        logger.info(f"'{self.name}' with params '{local_params}' is started")

        AdvertTask.objects.create(advert_id=int(kwargs.get('id')), task_id=self.request.id)
        result = self.execute(*args, **kwargs)

        if self.callback:
            self.callback()(result, *args, **kwargs)

        logger.info(f"{self.name} with params '{local_params}' is finished")
        logger.debug(f'Task: {self.name}, Context: {local_params}, Result: {result}')

        return result

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.exception(exc)
        # raise exc  # NOTE: django-celery-results is not working properly in case of 'raise'


class DispatchTask(Task):
    abstract = True
    # ----------
    name = None
    task = None

    def generate_monitoring_tasks(self):
        raise NotImplementedError

    def send_tasks_to_queue(self, tasks):
        group(self.task.s(**task) for task in tasks).apply_async()
        logger.info(f"{len(tasks)} tasks sent")

    def run(self, *args, **kwargs):
        local_params = locals()
        logger.info(f"'{self.name}' with params '{local_params}' is started")

        tasks = list(self.generate_monitoring_tasks())

        self.send_tasks_to_queue(tasks)

        logger.info(f"{self.name} with params '{local_params}' is finished")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.exception(exc)
        # raise exc  # NOTE: django-celery-results is not working properly in case of 'raise'

from .upload_video import UploadVideoTask # noqa
from. convert_video_to_wav import ConvertAudioToWavTask # noqa
from .split_audio_files import SplitAudioFilesTask # noqa
from .send_wav_to_acrcloud import SendWavToAcrCloudTask # noqa
from .spotify_get_tracks import SpotifyGetTracksTask # noqa
from .musiio import MusiioTask # noqa
from .chartmetric import ChartmetricTask # noqa
