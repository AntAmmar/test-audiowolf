from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from adverts.models import AdvertVideo

from api.advert.serializers import AdvertListSerializer


class AdvertListView(ListModelMixin, GenericViewSet):
    serializer = AdvertListSerializer
    queryset = AdvertVideo.objects.all()
