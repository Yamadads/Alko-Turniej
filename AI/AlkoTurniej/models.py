from django.contrib.auth.models import User
from django.db import models


class Tournament(models.Model):
    name = models.TextField(null=False)
    branch = models.TextField(null=False)
    organizer = models.ForeignKey(User, null=False)
    date = models.DateField(null=False)
    location_latitude = models.FloatField(null=False)
    location_longitude = models.FloatField(null=False)
    min_participants = models.IntegerField(null=False)
    max_participants = models.IntegerField(null=False)
    deadline = models.DateField(null=False)
    current_participants = models.IntegerField(null=False, default=0)


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
