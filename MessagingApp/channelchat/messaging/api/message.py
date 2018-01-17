import json

from django.http import HttpResponse

from django.utils import timezone
from django.views import generic
from django.conf import settings

from messaging.models import Conversation
from messaging.utils.seen import updateSeenMessage


class GetNewMessages(generic.View):
    def get(self, request, *args, **kwargs):
        data = []

        poll_time = timezone.now() - timezone.timedelta(
            seconds=settings.LONG_POLLING_SECS)

        c_pk = self.request.GET.get('conversation', '')

        if not c_pk:
            return HttpResponse(
                json.dumps([]), content_type='application/json')

        conversation = Conversation.objects.get(pk=c_pk)

        new_messages = conversation.message_conversations.filter(
            when__gte=poll_time).order_by('when')

        m_pk = self.request.GET.get('latestMessage', '')
        if m_pk:
            new_messages = new_messages.filter(pk__gt=m_pk)

        for msg in new_messages:
            date_string = timezone.localtime(msg.when).\
                strftime('%b. %d, %Y, %I:%M %p').\
                replace("AM", "a.m.").replace("PM", "p.m.")
            data.append({
                'id': msg.pk,
                'text': msg.text,
                'date': date_string,
                'sender': msg.sender.username
            })

        if(conversation.message_conversations.count() != 0):
            updateSeenMessage(conversation, self.request.user)
        return HttpResponse(json.dumps(data), content_type='application/json')


class LoadPreviousMessages(generic.View):
    def get(self, request, *args, **kwargs):
        # get 5 older messages based on the date given by template
        data = []

        first_message_pk = request.GET.get('firstMessagePK', '')
        c_pk = self.request.GET.get('conversation', '')
        if not c_pk:
            return HttpResponse(
                json.dumps([]), content_type='application/json')

        conversation = Conversation.objects.get(pk=c_pk)
        first_message = conversation.message_conversations.get(
            pk=first_message_pk)
        previous_messages = conversation.message_conversations.filter(
            when__lt=first_message.when).order_by('-when')[:5]

        for msg in previous_messages:
            date_string = timezone.localtime(msg.when).\
                strftime('%b. %d, %Y, %I:%M %p').\
                replace("AM", "a.m.").replace("PM", "p.m.")
            data.append({
                'id': msg.pk,
                'text': msg.text,
                'date': date_string,
                'sender': msg.sender.username
            })
        return HttpResponse(json.dumps(data), content_type='application/json')
