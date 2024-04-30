from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Token
from django.utils.timezone import now

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'token':
            return None

        token_value = parts[1]
        try:
            token = Token.objects.get(token=token_value)
            if token.expires_at < now():
                raise AuthenticationFailed('Token has expired')
            return (token.user, token)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Token not found')