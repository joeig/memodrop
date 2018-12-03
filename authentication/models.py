from django.contrib.auth.models import User
from django.db import models


class UserGUISettings(models.Model):
    """UserGUISettings

    Extend the user model with particular GUI settings.

    Null = Use system's default
    True = Enable feature explicitly
    False = Disable feature explicitly
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    enable_markdown_editor = models.NullBooleanField(verbose_name='Enable Markdown editor', null=True)

    class Meta:
        verbose_name = "User GUI settings"
        verbose_name_plural = verbose_name
