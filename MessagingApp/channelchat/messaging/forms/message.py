from django import forms
from django.contrib.auth.models import User

from messaging.models import Conversation, Message


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('text',)


class ConversationForm(forms.ModelForm):

    def __init__(self, uid, *args, **kwargs):
        super(ConversationForm, self).__init__(*args, **kwargs)
        self.fields['participants'].queryset = User.objects.exclude(id=uid)

    class Meta:
        model = Conversation
        fields = '__all__'
