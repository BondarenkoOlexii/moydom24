from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(email__iexact=username) | Q(user_id__iexact=username))

        except User.DoesNotExist:
            User().set_password(password)
            return None


        if user.check_password(password) and not user.user_status == 'inactive':
            return user
        return None


class CustomAdminModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email__iexact=username, is_admin=True)
        except User().DoesNotExist:
            return None

        if user.check_password(password) and not user.user_status == 'inactive':
            return user
        return None