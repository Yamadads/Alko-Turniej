from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string
import hashlib


class UserActivations(models.Model):
    user = models.ForeignKey(User, related_name='user_activation', null=False)
    activation_key = models.CharField(max_length=50, null=False, unique=True)

    def set_activation_key(self, email):
        hash_input = (get_random_string(10) + email).encode('utf-8')
        self.activation_key = hashlib.sha1(hash_input).hexdigest()
