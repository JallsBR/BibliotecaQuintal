"""2FA por e-mail — signin condicional e POST /api/v1/auth/2fa/verify."""

from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.hashers import make_password
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from users.models import TwoFactorChallenge, User
from users.services import OTP_MAX_ATTEMPTS


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    FRONTEND_URL="http://localhost:5173",
)
class TwoFactorApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="utilizador",
            email="utilizador@exemplo.com",
            password="SenhaSegura123!",
        )

    def test_post_login_com_2fa_retorna_challenge_sem_tokens(self):
        self.user.two_factor_enabled = True
        self.user.save(update_fields=["two_factor_enabled"])

        with (
            patch("users.services._gerar_otp_numerico", return_value="123456"),
            patch("users.services.secrets.token_urlsafe", return_value="link-token-fixo"),
        ):
            resp = self.client.post(
                reverse("signin"),
                {"email": self.user.email, "password": "SenhaSegura123!"},
                format="json",
            )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        body = resp.json()
        self.assertTrue(body.get("requires_2fa"))
        self.assertIn("challenge_id", body)
        self.assertNotIn("access", body)
        self.assertNotIn("refresh", body)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("123456", mail.outbox[0].body)
        self.assertIn("link-token-fixo", mail.outbox[0].body)
        self.assertIn("/auth/2fa-link", mail.outbox[0].body)
        self.assertTrue(mail.outbox[0].alternatives)
        self.assertEqual(mail.outbox[0].alternatives[0][1], "text/html")
        self.assertIn("123456", mail.outbox[0].alternatives[0][0])
        self.assertIn(self.user.email, mail.outbox[0].to)

    def test_post_login_sem_2fa_retorna_tokens(self):
        resp = self.client.post(
            reverse("signin"),
            {"email": self.user.email, "password": "SenhaSegura123!"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        body = resp.json()
        self.assertIn("access", body)
        self.assertIn("refresh", body)
        self.assertFalse(body.get("requires_2fa"))

    def test_post_2fa_verify_success(self):
        self.user.two_factor_enabled = True
        self.user.save(update_fields=["two_factor_enabled"])

        with patch("users.services._gerar_otp_numerico", return_value="654321"):
            signin = self.client.post(
                reverse("signin"),
                {"email": self.user.email, "password": "SenhaSegura123!"},
                format="json",
            )
        challenge_id = signin.json()["challenge_id"]

        resp = self.client.post(
            reverse("two_factor_verify"),
            {"challenge_id": challenge_id, "code": "654321"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        body = resp.json()
        self.assertIn("access", body)
        self.assertIn("refresh", body)
        self.assertEqual(body["user"]["id"], self.user.id)

        desafio = TwoFactorChallenge.objects.get(pk=challenge_id)
        self.assertIsNotNone(desafio.consumed_at)

    def test_post_2fa_verify_por_link_token(self):
        self.user.two_factor_enabled = True
        self.user.save(update_fields=["two_factor_enabled"])

        with (
            patch("users.services._gerar_otp_numerico", return_value="111222"),
            patch("users.services.secrets.token_urlsafe", return_value="meu-link-secreto"),
        ):
            signin = self.client.post(
                reverse("signin"),
                {"email": self.user.email, "password": "SenhaSegura123!"},
                format="json",
            )
        challenge_id = signin.json()["challenge_id"]

        resp = self.client.post(
            reverse("two_factor_verify"),
            {"challenge_id": challenge_id, "link_token": "meu-link-secreto"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp.json())

    def test_post_2fa_verify_codigo_errado(self):
        self.user.two_factor_enabled = True
        self.user.save(update_fields=["two_factor_enabled"])

        with patch("users.services._gerar_otp_numerico", return_value="111111"):
            signin = self.client.post(
                reverse("signin"),
                {"email": self.user.email, "password": "SenhaSegura123!"},
                format="json",
            )
        challenge_id = signin.json()["challenge_id"]

        resp = self.client.post(
            reverse("two_factor_verify"),
            {"challenge_id": challenge_id, "code": "000000"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        desafio = TwoFactorChallenge.objects.get(pk=challenge_id)
        self.assertEqual(desafio.attempts, 1)
        self.assertIsNone(desafio.consumed_at)

    def test_post_2fa_verify_expirado(self):
        desafio = TwoFactorChallenge.objects.create(
            user=self.user,
            code_hash=make_password("222222"),
            link_token_hash=make_password("tok"),
            expires_at=timezone.now() - timedelta(minutes=1),
        )
        resp = self.client.post(
            reverse("two_factor_verify"),
            {"challenge_id": str(desafio.id), "code": "222222"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_2fa_verify_max_attempts(self):
        desafio = TwoFactorChallenge.objects.create(
            user=self.user,
            code_hash=make_password("333333"),
            expires_at=timezone.now() + timedelta(minutes=10),
            attempts=OTP_MAX_ATTEMPTS,
        )
        resp = self.client.post(
            reverse("two_factor_verify"),
            {"challenge_id": str(desafio.id), "code": "333333"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_2fa_verify_campos_obrigatorios(self):
        resp = self.client.post(reverse("two_factor_verify"), {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
