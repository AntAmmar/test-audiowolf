from manager.tasks import UploadVideoTask

from adverts.models import AdvertVideo, AdvertVideoStatus
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=AdvertVideo)
def upload_file_task(sender, instance: AdvertVideo, **kwargs):
    AdvertVideoStatus.objects.create(advert=instance)
    task_kwargs = {'id': instance.id, 'name': instance.video.name}
    UploadVideoTask.delay(**task_kwargs)
