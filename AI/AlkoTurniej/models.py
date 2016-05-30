from django.contrib.auth.models import User
from django.db import models
from geoposition.fields import GeopositionField

class Tournament(models.Model):
    name = models.CharField(max_length=50, null=False, error_messages={'required': 'To pole jest wymagane'})
    branch = models.CharField(max_length=50, null=False, error_messages={'required': 'To pole jest wymagane'})
    organizer = models.ForeignKey(User, null=False)
    date = models.DateField(null=False, error_messages={'required': 'To pole jest wymagane'})
    position = GeopositionField(null=True)
    min_participants = models.IntegerField(null=False, error_messages={'required': 'To pole jest wymagane'})
    max_participants = models.IntegerField(null=False, error_messages={'required': 'To pole jest wymagane'})
    deadline = models.DateField(null=False, error_messages={'required': 'To pole jest wymagane'})
    current_participants = models.IntegerField(null=False, default=0)
    def getFullInfo(self):
        return self.name + ", " + self.branch + ", " + self.organizer + ", " + self.date


class TournamentParticipant(models.Model):
    participant = models.ForeignKey(User, null=False)
    tournament = models.ForeignKey(Tournament, null=False)

    class Meta:
        unique_together = ('participant', 'tournament',)


class SponsorLogos(models.Model):
    tournament = models.ForeignKey(Tournament, related_name='sponsor_logos', null=False)
    picture = models.ImageField()


class TournamentLadder(models.Model):
    tournament = models.ForeignKey(Tournament, related_name="ladder", null=False)
