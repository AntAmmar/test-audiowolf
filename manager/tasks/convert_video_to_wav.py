import os
import subprocess

from audiowolf.settings import MEDIA_ROOT

from adverts.models import AdvertVideoStatus, Status
from manager.tasks.neural_network import NeuralNetworkTask
from audiowolf.celery import app

from manager.tasks import BaseTask

formats = (".mp4", ".webm", ".mkv")


class ConvertAudioToWavTask(BaseTask):
    name = 'convert_video_to_wav'
    callback = None

    def execute(self, *args, **kwargs):
        advert_id = kwargs.get('id')
        path = os.path.join(MEDIA_ROOT, kwargs.get('name'))
        AdvertVideoStatus.objects.get(advert_id=advert_id).update_convert_video_to_wav_status(Status.IN_PROGRESS)
        for fmt in formats:
            if path.endswith(fmt):
                outpath = path.replace(fmt, ".wav")
                break
        else:
            print("Video format not recognized (.mp4, .webm, .mkv)")
            return False

        if not os.path.isfile(outpath):
            subprocess.call(["ffmpeg", "-i", path, outpath])
            kwargs['path'] = outpath
            NeuralNetworkTask.delay(**kwargs)
            AdvertVideoStatus.objects.get(advert_id=advert_id).update_convert_video_to_wav_status(Status.SUCCESS)
            return outpath
        else:
            print("Skipping - file already exists")
            return False


ConvertAudioToWavTask = app.register_task(ConvertAudioToWavTask())
