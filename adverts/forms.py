from django import forms
from adverts.models import AdvertVideo


class AdvertVideoForm(forms.ModelForm):
    class Meta:
        model = AdvertVideo
        fields = ['brand', 'video']
