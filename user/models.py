from django.db import models

from belka import settings
from utils.constants import ON_SAVE, ON_SAVE_SUM_30, ON_FULL_OPEN_FOUR, ON_FULL, ON_EGGS, ON_EGGS_OPEN_FOUR
from utils.time_utils import dt_to_timestamp


class GameSetting(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='game_setting', null=False, on_delete=models.CASCADE)
    on_save = models.IntegerField(choices=ON_SAVE, default=ON_SAVE_SUM_30)
    on_full = models.IntegerField(choices=ON_FULL, default=ON_FULL_OPEN_FOUR)
    ace_allowed = models.BooleanField(default=True)
    on_eggs = models.IntegerField(choices=ON_EGGS, default=ON_EGGS_OPEN_FOUR)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"Game setting {0} of user {1}".format(self.pk, self.owner_id)

    def json(self):
        return {
            "setting_id": self.pk,
            "user_id": self.owner_id,
            "on_save": self.on_save,
            "on_save_display": self.get_on_save_display(),
            "on_full": self.on_full,
            "on_full_display": self.get_on_full_display(),
            "ace_allowed": self.ace_allowed,
            "on_eggs": self.on_eggs,
            "on_eggs_display": self.get_on_eggs_display(),
            "timestamp": dt_to_timestamp(self.timestamp),
        }

    class Meta:
        ordering = ['timestamp']


