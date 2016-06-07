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
    logo1 = models.ImageField(upload_to='upload/', default='default.jpg')
    logo2 = models.ImageField(upload_to='upload/', default='default.jpg')
    logo3 = models.ImageField(upload_to='upload/', default='default.jpg')
    active = models.BooleanField(null=False, default=True)
    in_progress = models.BooleanField(null=False, default=False)
    canceled = models.BooleanField(null=False, default=False)

    def getFullInfo(self):
        return self.name + ", " + self.branch + ", " + self.organizer + ", " + self.date


class TournamentParticipant(models.Model):
    participant = models.ForeignKey(User, null=False)
    tournament = models.ForeignKey(Tournament, null=False)
    license_number = models.IntegerField(null=False)
    ranking_position = models.IntegerField(null=False)

    class Meta:
        unique_together = (('participant', 'tournament', 'license_number', 'ranking_position'),)


class Encounter(models.Model):
    tournament = models.ForeignKey(Tournament, related_name="encounter", null=False)
    round = models.IntegerField(null=False)
    encounter_id = models.IntegerField(null=False)
    user1 = models.ForeignKey(User, related_name="user1", null=False)
    user1_decision_winner = models.NullBooleanField(null=True)
    user2 = models.ForeignKey(User, related_name="user2", null=False)
    user2_decision_winner = models.NullBooleanField(null=True)
    winner = models.ForeignKey(User, null=True, default=None)

    class Meta:
        unique_together = (('tournament', 'round', 'encounter_id'))
