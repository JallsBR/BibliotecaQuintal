import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    two_factor_enabled = models.BooleanField(
        "autenticação em dois fatores",
        default=False,
        db_index=True,
        help_text=(
            "Se verdadeiro, o login exige um código OTP enviado ao e-mail cadastrado."
        ),
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["username"]

    def __str__(self):
        return self.email


class TwoFactorChallenge(models.Model):
    """Desafio OTP de login. O código em claro nunca é persistido."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="two_factor_challenges",
        verbose_name="usuário",
    )
    code_hash = models.CharField("hash do código", max_length=128)
    link_token_hash = models.CharField(
        "hash do link mágico",
        max_length=128,
        blank=True,
        default="",
        help_text="Token do link de login no e-mail; nunca em claro.",
    )
    expires_at = models.DateTimeField("expira em", db_index=True)
    consumed_at = models.DateTimeField("consumido em", null=True, blank=True)
    attempts = models.PositiveSmallIntegerField("tentativas", default=0)
    created_at = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "desafio 2FA"
        verbose_name_plural = "desafios 2FA"
        indexes = [
            models.Index(fields=["user", "expires_at"], name="users_twofa_user_exp_idx"),
        ]

    def __str__(self):
        return f"2fa:{self.id} user={self.user_id}"


class PasswordResetChallenge(models.Model):
    """Desafio de redefinição de senha. Token em claro nunca é persistido."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_challenges",
        verbose_name="usuário",
    )
    token_hash = models.CharField("hash do token", max_length=128)
    expires_at = models.DateTimeField("expira em", db_index=True)
    consumed_at = models.DateTimeField("consumido em", null=True, blank=True)
    created_at = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "desafio de redefinição de senha"
        verbose_name_plural = "desafios de redefinição de senha"
        indexes = [
            models.Index(
                fields=["user", "expires_at"], name="users_pwdreset_user_exp_idx"
            ),
        ]

    def __str__(self):
        return f"pwdreset:{self.id} user={self.user_id}"
