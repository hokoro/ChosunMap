from django.forms import ModelForm

from mapapp.models import Building, Search, Mode, Search_Bus


class SearchCreationForm(ModelForm):
    class Meta:
        model = Search
        fields = ['departure', 'arrival']


class BusCreationForm(ModelForm):
    class Meta:
        model = Search_Bus
        fields = ['route']
