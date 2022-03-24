from adverts.models import AdvertVideo
from rest_framework.serializers import ModelSerializer


class AdvertListSerializer(ModelSerializer):
    class Meta:
        model = AdvertVideo
        fields = '__all__'
