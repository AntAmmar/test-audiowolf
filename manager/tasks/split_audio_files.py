import os
import subprocess

from audiowolf.settings import MEDIA_ROOT, AUDIO_SPLIT_DURATION

from adverts.models import AdvertVideoStatus, Status
from audiowolf.celery import app

from manager.tasks import BaseTask
from manager.tasks.send_wav_to_acrcloud import SendWavToAcrCloudTask


class SplitAudioFilesTask(BaseTask):
    name = 'split_audio_files'
    callback = None

    def execute(self, *args, **kwargs):
        advert_id = kwargs.get('id')
        path = kwargs.get('path')
        split_ranges = kwargs.get('split_ranges')
        AdvertVideoStatus.objects.get(advert_id=advert_id).update_split_audio_files_status(Status.IN_PROGRESS)
        if not split_ranges:
            filename, extension = path.split(".")
            format_filename = filename + "%03d"
            output_path = ".".join([format_filename, extension])
            subprocess.call(["ffmpeg", "-i", path, "-f", "segment", "-segment_time", AUDIO_SPLIT_DURATION, output_path])
            split_audio_files = []
            base_filename = filename.split('/')[-1]
            for audio_file in os.listdir(os.path.join(MEDIA_ROOT, 'video')):
                split_filename, split_extension = audio_file.split('.')
                if split_filename.startswith(f'{base_filename}0') and split_extension == 'wav':
                    split_audio_files.append(audio_file)
            for audio_path in split_audio_files:
                kwargs['audio_path'] = audio_path
                SendWavToAcrCloudTask.delay(**kwargs)
            AdvertVideoStatus.objects.get(advert_id=advert_id).update_split_audio_files_status(Status.SUCCESS)
            return split_audio_files

        ffmpeg_command = ["ffmpeg", "-i", path]

        for index, split_range in enumerate(split_ranges):
            filename, extension = path.split(".")
            format_filename = filename + str(index).zfill(3)
            output_path = ".".join([format_filename, extension])
            ffmpeg_command.extend(["-ss", str(split_range[0]), "-to", str(split_range[1]), "-c", "copy", output_path])

        subprocess.call(ffmpeg_command)
        return True


SplitAudioFilesTask = app.register_task(SplitAudioFilesTask())
