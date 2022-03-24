import boto3
from django.conf import settings
from rest_framework import serializers

from adverts.models import AdvertVideo
from rest_framework.serializers import ModelSerializer


class AdvertListSerializer(ModelSerializer):
    brand_name = serializers.CharField(source='brand.name')
    advert_url = serializers.SerializerMethodField()
    sector_name = serializers.CharField(source='sector.name', allow_blank=True)
    product_name = serializers.CharField(source='product.name', allow_null=True)

    class Meta:
        model = AdvertVideo
        fields = ('brand_name', 'advert_url', 'name', 'sector_name', 'product_name', 'release_date', 'processing_date')

    def get_advert_url(self, obj):
        endpoint_url = settings.AWS_S3_ENDPOINT_URL
        bucket = settings.AWS_STORAGE_BUCKET_NAME

        client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY
        )
        return client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': obj.video.name},
            ExpiresIn=5,
        )
