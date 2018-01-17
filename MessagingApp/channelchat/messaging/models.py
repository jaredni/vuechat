# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Conversation(models.Model):
    title = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='conversations', blank=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "{}".format(self.pk)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='message_sent')
    conversation = models.ForeignKey(
        Conversation, related_name='message_conversations', null=True)
    text = models.TextField(null=True)
    when = models.DateTimeField(auto_now=True, null=True)
    # Default should include sender
    seen_by = models.ManyToManyField(
        User, related_name='message_seen', blank=True)
    # Default should at least include all participants
    unseen_by = models.ManyToManyField(
        User, related_name='message_unseen', blank=True)

    def __str__(self):
        if self.text:
            return self.text
        else:
            return "{}".format(self.pk)
