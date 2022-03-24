from django.urls import path, include

from api.advert.views import AdvertListView
from api.router import RestRouter

router = RestRouter()
router.register('', AdvertListView, basename='advert-list')

urlpatterns = [
    path('', include(router.urls)),
]
