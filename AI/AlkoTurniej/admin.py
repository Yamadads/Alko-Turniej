from django.contrib import admin
from . import models

admin.site.register(models.TournamentLadder)
admin.site.register(models.TournamentParticipant)
admin.site.register(models.Tournament)
admin.site.register(models.SponsorLogos)
