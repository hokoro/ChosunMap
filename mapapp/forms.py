from django.forms import ModelForm

from mapapp.models import Building, Search ,Mode


class SearchCreationForm(ModelForm):
    class Meta:
        model = Search
        fields=['departure','arrival']