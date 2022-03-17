import json
from typing import Iterable

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

    def get_context_data(self, **kwargs):
        context = super(AdvertDetails, self).get_context_data(**kwargs)
        context['name'] = self.get_object().video.name.split('/')[-1]
        context['advert_url'] = self.get_object().advert_url.replace('view?usp=sharing', 'preview')
        advert_tasks = self.get_object().adverttask_set.all()
        context_tasks = []
        advert_task_ids = [advert_task.task_id for advert_task in advert_tasks]
        tasks = TaskResult.objects.filter(task_id__in=advert_task_ids)
        for task in tasks:
            if task.task_name == 'send_wav_to_acr_cloud' and task.status == 'SUCCESS':
                tasks_map = {}
                children = json.loads(task.meta).get('children')
                flat_list = flatten(children)
                subtasks = [TaskResult.objects.filter(task_id=task_id, status='SUCCESS') for task_id in flat_list]
                tasks_map[task] = list(filter(lambda v: v.exists(), subtasks))[0]
                context_tasks.append(tasks_map)
        context['tasks'] = context_tasks
        return context
