from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        db_table = 'brand'


class AdvertVideo(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=False, null=False)
    video = models.FileField(upload_to='video/', blank=True, null=True)

    class Meta:
        db_table = 'advert_video'

    @property
    def get_last_step(self):
        if self.advertvideostatus.convert_video_to_wav == Status.IN_PROGRESS:
            return self.advertvideostatus.convert_video_to_wav
        elif self.advertvideostatus.split_audio_files == Status.IN_PROGRESS:
            return self.advertvideostatus.split_audio_files
        elif self.advertvideostatus.send_acr_cloud == Status.IN_PROGRESS:
            return self.advertvideostatus.send_acr_cloud
        elif self.advertvideostatus.spotify_get_tracks == Status.IN_PROGRESS:
            return self.advertvideostatus.spotify_get_tracks
        elif self.advertvideostatus.musiio == Status.IN_PROGRESS:
            return self.advertvideostatus.musiio
        elif self.advertvideostatus.chartmetric == Status.IN_PROGRESS:
            return self.advertvideostatus.chartmetric
        else:
            return self.advertvideostatus.upload_video


class Status(models.TextChoices):
    NOT_STARTED = ('NOT_STARTED', 'Not started')
    IN_PROGRESS = ('IN_PROGRESS', 'In progress')
    SUCCESS = ('SUCCESS', 'Successfully finished')
    ERROR = ('ERROR', 'Error')


class AdvertVideoStatus(models.Model):
    advert = models.OneToOneField(AdvertVideo, on_delete=models.DO_NOTHING)
    upload_video = models.CharField(choices=Status.choices, default=Status.NOT_STARTED, max_length=100, blank=False, null=False)
    convert_video_to_wav = models.CharField(choices=Status.choices, default=Status.NOT_STARTED, max_length=100, blank=False, null=False)
    neural_network = models.CharField(choices=Status.choices, default=Status.NOT_STARTED, max_length=100, blank=False, null=False)
    split_audio_files = models.CharField(choices=Status.choices, default=Status.NOT_STARTED, max_length=100, blank=False, null=False)
    send_acr_cloud = models.CharField(choices=Status.choices, default=Status.NOT_STARTED, max_length=100, blank=False, null=False)
    spotify_get_tracks = models.CharField(choices=Status.choices, default=Status.NOT_STARTED, max_length=100, blank=False, null=False)
    musiio = models.CharField(choices=Status.choices, default=Status.NOT_STARTED, max_length=100, blank=False, null=False)
    chartmetric = models.CharField(choices=Status.choices, default=Status.NOT_STARTED, max_length=100, blank=False, null=False)

    class Meta:
        db_table = 'advert_video_status'

    def update_upload_video(self, status: Status):
        self.upload_video = status
        self.save()

    def update_convert_video_to_wav_status(self, status: Status):
        self.convert_video_to_wav = status
        self.save()

    def update_neural_network_status(self, status: Status):
        self.neural_network = status
        self.save()

    def update_split_audio_files_status(self, status: Status):
        self.split_audio_files = status
        self.save()

    def update_send_acr_cloud(self, status: Status):
        self.send_acr_cloud = status
        self.save()

    def update_spotify_get_tracks(self, status: Status):
        self.spotify_get_tracks = status
        self.save()

    def update_musiio(self, status: Status):
        self.musiio = status
        self.save()

    def update_chartmetric(self, status: Status):
        self.chartmetric = status
        self.save()


class AdvertTask(models.Model):
    task_id = models.CharField(max_length=100, blank=False, null=False)
    advert = models.ForeignKey(AdvertVideo, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        db_table = 'advert_task'
