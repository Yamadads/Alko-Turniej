from django.forms import ModelForm
from .models import Tournament


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'branch', 'organizer', 'date', 'location_latitude',
                  'location_longitude', 'min_participants', 'max_participants', 'deadline']

