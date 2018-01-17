# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.views import generic

from messaging.models import Conversation, Message
from messaging.forms.message import MessageForm
from messaging.utils.mixins import LoginRequiredMixin
from messaging.utils.seen import createSeenMessage, updateSeenMessage


class SendView(LoginRequiredMixin, generic.CreateView):
    template_name = 'messaging/private/send.html'
    model = Message
    form_class = MessageForm
    success_url = None

    def get_context_data(self, **kwargs):
        context = super(SendView, self).get_context_data(**kwargs)
        receiver = User.objects.get(id=self.kwargs['pk'])
        conversation = Conversation.objects.annotate(
            num_participants=Count('participants')).filter(
            num_participants=2).filter(
            participants=self.request.user).filter(
            participants=receiver).first()
        if conversation:
            updateSeenMessage(conversation, self.request.user)
            context['MESSAGES'] = conversation.message_conversations.all()\
                .order_by('-when')

        context['CONVERSATION'] = conversation
        context['RECEIVER'] = receiver
        poll_time = timezone.now() - timezone.timedelta(
            seconds=settings.LONG_POLLING_SECS)
        context['POLL_TIME'] = poll_time
        return context

    def form_valid(self, form):
        receiver = User.objects.get(id=self.kwargs['pk'])
        # filter conversations between 2 users
        conversation = Conversation.objects.annotate(
            num_participants=Count('participants')).filter(
            num_participants=2).filter(
            participants=self.request.user).filter(
            participants=receiver).first()

        self.object = form.save(commit=False)
        self.object.sender = self.request.user
        if not conversation:
            q = Conversation(title='Private Message: {}/{}'.format(
                self.request.user, receiver))
            q.save()
            q.participants.add(self.request.user, receiver)
            # add new conversation if no convo exists yet
            self.object.conversation = q
        else:
            # print previous chats
            self.object.conversation = conversation

        self.object.save()
        createSeenMessage(self.object)

        self.success_url = reverse(
            'messaging:send-private-message', args=(receiver.pk,))
        date_string = timezone.localtime(self.object.when).\
            strftime('%b. %d, %Y, %I:%M %p').\
            replace("AM", "a.m.").replace("PM", "p.m.")
        data = {'id': self.object.pk,
                'text': self.object.text,
                'date': date_string,
                'sender': self.object.sender.username}
        return HttpResponse(json.dumps(data), content_type='application/json')
