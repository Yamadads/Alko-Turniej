from django.contrib import admin
from . import models
from .accounts.models import UserActivations

admin.site.register(models.TournamentLadder)
admin.site.register(models.TournamentParticipant)
admin.site.register(models.Tournament)
admin.site.register(models.SponsorLogos)
admin.site.register(UserActivations)
