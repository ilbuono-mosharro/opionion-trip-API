from datetime import datetime, timedelta
from django.utils import timezone

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class ShortLivedTokenAuthentication(TokenAuthentication):
    token_timeout = timedelta(minutes=1)
    print(datetime.utcnow())

    def authenticate_credentials(self, key):
        try:
            token = self.get_model().objects.get(key=key)
        except self.get_model().DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')

        # Verifica se il token è scaduto
        if token.created < timezone.now() - self.token_timeout:
            token.delete()
            raise AuthenticationFailed('Token has expired.')

        return (token.user, token)
