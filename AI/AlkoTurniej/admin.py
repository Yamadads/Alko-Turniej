from django.contrib import admin
from . import models
from .accounts.models import UserActivations, UserPasswordReset

admin.site.register(models.TournamentLadder)
admin.site.register(models.TournamentParticipant)
admin.site.register(models.Tournament)
admin.site.register(UserActivations)
admin.site.register(UserPasswordReset)
