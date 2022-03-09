from adverts.models import AdvertVideoStatus, Status
from audiowolf.utils import file_transferred
from audiowolf.celery import app
from audiowolf.utils import import_attribute
from manager.tasks import BaseTask
from manager.tasks.convert_video_to_wav import ConvertAudioToWavTask
from celery.utils.log import get_task_logger

logger = get_task_logger(name=__name__)


class UploadVideoTask(BaseTask):
    name = 'upload_video'
    callback = None

    @staticmethod
    def transfer(name, local, remote):
        try:
            remote.save(name, local.open(name))
            return True
        except Exception as e:
            logger.error("Unable to save '%s' to remote storage. "
                         "About to retry." % name)
            logger.exception(e)
            return False

    def execute(self, *args, **kwargs):
        name = kwargs.get('name')
        advert_id = kwargs.get('id')
        AdvertVideoStatus.objects.get(advert_id=advert_id).update_upload_video(Status.IN_PROGRESS)

        local = import_attribute('django.core.files.storage.FileSystemStorage')()
        remote = import_attribute('adverts.storage.VultrStorage')()
        result = self.transfer(name, local, remote)

        if result is True:
            file_transferred.send(sender=self.__class__,
                                  name=name, local=local, remote=remote)
            # local.delete(name)
        elif result is False:
            args = [name]
            self.retry(args=args, kwargs=kwargs)
        else:
            raise ValueError("Task '%s' did not return True/False but %s" %
                             (self.__class__, result))
        AdvertVideoStatus.objects.get(advert_id=advert_id).update_upload_video(Status.SUCCESS)
        ConvertAudioToWavTask.delay(**kwargs)
        return result


UploadVideoTask = app.register_task(UploadVideoTask())
