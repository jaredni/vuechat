# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils import timezone
from django.views import generic

from messaging.models import Conversation, Message
from messaging.forms.message import ConversationForm, MessageForm
from messaging.utils.mixins import (
    LoginRequiredMixin, GroupPermissionRequiredMixin)
from messaging.utils.seen import createSeenMessage, updateSeenMessage


class CreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'messaging/group/create.html'
    model = Conversation
    form_class = ConversationForm
    success_url = None

    def get_form(self, form_class=None):
        form = ConversationForm(
            uid=self.request.user.id, **self.get_form_kwargs())
        return form

    def form_valid(self, form):
        self.object = form.save()
        participants = json.loads(self.request.POST['participant_pks'])

        for user_pk in participants:
            user = User.objects.get(pk=user_pk)
            self.object.participants.add(user)

        self.object.participants.add(self.request.user)
        self.success_url = reverse(
            'messaging:send-group-conversation', args=(self.object.pk,))
        return HttpResponse(
            json.dumps(self.success_url), content_type='application/json')


class SendView(
        LoginRequiredMixin, GroupPermissionRequiredMixin, generic.CreateView):
    template_name = 'messaging/group/send.html'
    model = Message
    form_class = MessageForm
    success_url = None

    def form_valid(self, form):
        c = Conversation.objects.get(pk=self.kwargs['conversation_pk'])
        self.object = form.save(commit=False)
        self.object.sender = self.request.user
        self.object.conversation = c
        self.object.save()

        createSeenMessage(self.object)

        self.success_url = reverse(
            'messaging:send-group-conversation', args=(c.pk,))
        date_string = timezone.localtime(self.object.when).\
            strftime('%b. %d, %Y, %I:%M %p').\
            replace("AM", "a.m.").replace("PM", "p.m.")
        data = {'id': self.object.pk,
                'text': self.object.text,
                'date': date_string,
                'sender': self.object.sender.username}
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(SendView, self).get_context_data(**kwargs)
        conversation = Conversation.objects.get(
            pk=self.kwargs['conversation_pk'])
        if conversation:
            if conversation.message_conversations.exists():
                updateSeenMessage(conversation, self.request.user)
            context['MESSAGES'] = conversation.message_conversations.all()\
                .order_by('-when')
        context['USER'] = User.objects.all()
        context['CONVERSATION'] = conversation
        context['PK'] = self.kwargs['conversation_pk']
        poll_time = timezone.now() - timezone.timedelta(
            seconds=settings.LONG_POLLING_SECS)
        context['POLL_TIME'] = poll_time
        return context


class RemoveParticipant(
        LoginRequiredMixin,
        GroupPermissionRequiredMixin, generic.RedirectView):

    def post(self, request, *args, **kwargs):
        c = Conversation.objects.get(pk=kwargs['conversation_pk'])
        user = User.objects.get(pk=kwargs['user_pk'])
        c.participants.remove(user)
        return HttpResponse(user.username)


class AddParticipant(
        LoginRequiredMixin,
        GroupPermissionRequiredMixin, generic.RedirectView):

    def post(self, request, *args, **kwargs):
        data = []
        c = Conversation.objects.get(pk=kwargs['conversation_pk'])
        user = User.objects.get(pk=kwargs['user_pk'])
        c.participants.add(user)
        data = {
            'id': user.pk,
            'username': user.username
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
