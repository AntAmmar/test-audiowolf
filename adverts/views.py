import json
from typing import Iterable

import boto3
from django.conf import settings
from django_celery_results.models import TaskResult

from adverts.forms import AdvertVideoForm
from django.urls import reverse
from django.views.generic import ListView, DetailView, FormView

from adverts.models import Brand, AdvertVideoStatus, AdvertVideo


class BrandList(ListView):
    model = Brand
    template_name = 'brands/list.html'


class BrandAdverts(DetailView, FormView):
    model = Brand
    template_name = 'adverts/list.html'
    form_class = AdvertVideoForm
    queryset = Brand.objects.all().prefetch_related('advertvideo_set')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.brand = self.get_object()
        instance.video = form.cleaned_data.get('video')
        instance.save()
        return super().form_valid(instance)

    def get_success_url(self):
        return reverse('brand-adverts', kwargs={'pk': self.get_object().id})


class AdvertPipeline(DetailView):
    model = AdvertVideoStatus
    template_name = 'adverts/pipeline.html'


def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x


class AdvertDetails(DetailView):
    model = AdvertVideo
    template_name = 'adverts/video_details.html'

    def get_video_url(self, obj):
        endpoint_url = settings.AWS_S3_ENDPOINT_URL
        bucket = settings.AWS_STORAGE_BUCKET_NAME

        boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY
        )

        return f'{settings.AWS_S3_ENDPOINT_URL}/{bucket}/{obj.video.name}'

    def get_context_data(self, **kwargs):
        context = super(AdvertDetails, self).get_context_data(**kwargs)
        context['name'] = self.get_object().video.name.split('/')[-1]
        context['advert_url'] = self.get_video_url(self.get_object())
        advert_tasks = self.get_object().adverttask_set.all()
        context_tasks = []
        preview_tasks_name = ['send_wav_to_acr_cloud', 'spotify_get_tracks', 'musiio', 'chartmetric_task']
        advert_task_ids = [advert_task.task_id for advert_task in advert_tasks]
        tasks = TaskResult.objects.filter(task_id__in=advert_task_ids).order_by('id')
        for task in tasks:
            if task.task_name in preview_tasks_name and task.status == 'SUCCESS':
                context_tasks.append(task)
        context['tasks'] = context_tasks
        return context
