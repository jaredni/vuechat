# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from messaging.models import Conversation, Message


class ConversationAdmin(admin.ModelAdmin):
    raw_id_fields = ('participants',)

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message)
