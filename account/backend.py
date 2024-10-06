from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, token=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if token == request.session.get('token'):
                return user