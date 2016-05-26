from django.contrib.auth.models import User

class EmailBackend:
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        user = None
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            pass

        if user:
            if user.check_password(password):
                return user
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None