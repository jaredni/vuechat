# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db.models import Count
from django.views import generic

from messaging.models import Conversation
from messaging.utils.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'messaging/index.html'
    model = User

    def get_queryset(self):
        # User.objects.all()
        queryset = super(IndexView, self).get_queryset()
        # User.objects.all().filter()
        queryset = queryset.filter(
            username__istartswith=self.request.GET.get('searched_user', ''))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['SEARCHEDUSER'] = self.request.GET.get('searched_user', '')
        context['GROUP_CONVO'] = Conversation.objects.annotate(
            num_participants=Count('participants')).filter(
            num_participants__gt=2).filter(
            participants=self.request.user)
        context['PRIVATE_CONVO'] = Conversation.objects.annotate(
            num_participants=Count('participants')).filter(
            num_participants=2).filter(
            participants=self.request.user)
        context['LOGGED_IN'] = self.request.user
        return context


class ErrorView(generic.TemplateView):
    template_name = 'messaging/error.html'
