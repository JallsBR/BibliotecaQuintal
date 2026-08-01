from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from users.services import autenticar_signin


class SigninThrottle(AnonRateThrottle):
    scope = "auth_signin"


class Signin(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [SigninThrottle]

    def post(self, request):
        def _strip(v):
            if v is None:
                return ""
            return str(v).strip()

        email = _strip(request.data.get("email"))
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"detail": "Informe o e-mail e a senha."},
                status=HTTP_400_BAD_REQUEST,
            )

        payload = autenticar_signin(email=email, password=password)
        return Response(payload)
