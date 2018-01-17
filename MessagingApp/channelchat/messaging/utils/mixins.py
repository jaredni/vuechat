# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404

from messaging.models import Conversation


class LoginRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return HttpResponseRedirect(reverse('login'))

        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class GroupPermissionRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        try:
            conversation = Conversation.objects.get(
                pk=kwargs['conversation_pk'])
        except ObjectDoesNotExist:
            raise Http404

        if request.user not in conversation.participants.all():
            raise Http404

        return super(GroupPermissionRequiredMixin, self).dispatch(
            request, *args, **kwargs)
