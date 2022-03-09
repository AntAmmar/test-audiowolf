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
