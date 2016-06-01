from django.contrib.auth.models import User
from django.db import models
from geoposition.fields import GeopositionField


class Tournament(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    branch = models.CharField(max_length=50, null=False)
    organizer = models.ForeignKey(User, null=False)
    date = models.DateField(null=False)
    position = GeopositionField(blank=True, null=True)
    min_participants = models.IntegerField(null=False)
    max_participants = models.IntegerField(null=False)
    deadline = models.DateField(null=False)
    current_participants = models.IntegerField(null=False, default=0)
    logo1 = models.ImageField(upload_to = 'upload/', default = 'default.jpg')
    logo2 = models.ImageField(upload_to = 'upload/', default = 'default.jpg')
    logo3 = models.ImageField(upload_to = 'upload/', default = 'default.jpg')

    def getFullInfo(self):
        return self.name + ", " + self.branch + ", " + self.organizer + ", " + self.date


class TournamentParticipant(models.Model):
    participant = models.ForeignKey(User, null=False)
    tournament = models.ForeignKey(Tournament, null=False)
    license_number = models.IntegerField(unique=True, null=False)
    ranking_position = models.IntegerField(unique=True, null=False)

    class Meta:
        unique_together = (('participant', 'tournament'),)

class TournamentLadder(models.Model):
    tournament = models.ForeignKey(Tournament, related_name="ladder", null=False)
