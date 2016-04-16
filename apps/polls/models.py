# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
from mezzanine.core.models import RichText
from mezzanine.pages.models import Page


class Poll(Page, RichText):
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Poll')


class Choice(models.Model):
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=256, default='')

    def __str__(self):
        return '{choice} in Poll {poll}'.format(
            choice=self.text,
            poll=self.poll.title
        )


class Vote(models.Model):
    choice = models.ForeignKey('Choice')
    user = models.ForeignKey(User)

    def __str__(self):
        return 'Vote by {user} for Choice {choice} in Poll {poll}'.format(
            user=self.user,
            choice=self.choice.text,
            poll=self.choice.poll.title
        )
