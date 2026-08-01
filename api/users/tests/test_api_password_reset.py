"""Recuperação de senha por e-mail."""

from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.hashers import make_password
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from users.models import PasswordResetChallenge, User
from users.services import PASSWORD_RESET_GENERIC_MSG


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    FRONTEND_URL="http://localhost:11666",
)
class PasswordResetApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="utilizador",
            email="utilizador@exemplo.com",
            password="SenhaSegura123!",
        )

    def test_password_reset_request_envia_email(self):
        with patch("users.services.secrets.token_urlsafe", return_value="token-reset-fixo"):
            resp = self.client.post(
                reverse("password_reset_request"),
                {"email": self.user.email},
                format="json",
            )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()["detail"], PASSWORD_RESET_GENERIC_MSG)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.user.email, mail.outbox[0].to)
        self.assertIn("token-reset-fixo", mail.outbox[0].body)
        self.assertIn("/auth/redefinir-senha", mail.outbox[0].body)
        self.assertTrue(mail.outbox[0].alternatives)
        self.assertEqual(
            PasswordResetChallenge.objects.filter(user=self.user).count(), 1
        )

    def test_password_reset_request_email_inexistente_nao_vaza(self):
        resp = self.client.post(
            reverse("password_reset_request"),
            {"email": "naoexiste@example.com"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()["detail"], PASSWORD_RESET_GENERIC_MSG)
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_confirm_success(self):
        with patch("users.services.secrets.token_urlsafe", return_value="abc123token"):
            self.client.post(
                reverse("password_reset_request"),
                {"email": self.user.email},
                format="json",
            )
        desafio = PasswordResetChallenge.objects.filter(user=self.user).latest(
            "created_at"
        )

        resp = self.client.post(
            reverse("password_reset_confirm"),
            {
                "challenge_id": str(desafio.id),
                "token": "abc123token",
                "new_password": "NovaSenhaSegura456!",
                "new_password_confirm": "NovaSenhaSegura456!",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NovaSenhaSegura456!"))
        desafio.refresh_from_db()
        self.assertIsNotNone(desafio.consumed_at)

        login = self.client.post(
            reverse("signin"),
            {"email": self.user.email, "password": "NovaSenhaSegura456!"},
            format="json",
        )
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        body = login.json()
        self.assertTrue("access" in body or body.get("requires_2fa"))

    def test_password_reset_confirm_token_invalido(self):
        desafio = PasswordResetChallenge.objects.create(
            user=self.user,
            token_hash=make_password("certo"),
            expires_at=timezone.now() + timedelta(minutes=30),
        )
        resp = self.client.post(
            reverse("password_reset_confirm"),
            {
                "challenge_id": str(desafio.id),
                "token": "errado",
                "new_password": "NovaSenhaSegura456!",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_password_reset_confirm_expirado(self):
        desafio = PasswordResetChallenge.objects.create(
            user=self.user,
            token_hash=make_password("tok"),
            expires_at=timezone.now() - timedelta(minutes=1),
        )
        resp = self.client.post(
            reverse("password_reset_confirm"),
            {
                "challenge_id": str(desafio.id),
                "token": "tok",
                "new_password": "NovaSenhaSegura456!",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
