# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def updateSeenMessage(conversation, seen_by):
    conversation.message_conversations.last().seen_by.add(
        seen_by)
    conversation.message_conversations.last().unseen_by.remove(
        seen_by)


def createSeenMessage(message):
    message_participants = message.conversation.participants.exclude(
        pk=message.sender.pk)
    message.seen_by.add(message.sender)
    for user in message_participants:
        message.unseen_by.add(user)
