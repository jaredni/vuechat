from django.conf.urls import url

from . import views, api

urlpatterns = [
    url(r'^$', views.base.IndexView.as_view(), name='index'),
    url(r'^error/$',
        views.base.ErrorView.as_view(), name='error'),
    url(r'^private/message/(?P<pk>\d+)/$',
        views.private.SendView.as_view(), name='send-private-message'),
    url(r'^group/message/create/$',
        views.group.CreateView.as_view(),
        name='create-group-conversation'),
    url(r'^group/message/send/(?P<conversation_pk>\d+)/$',
        views.group.SendView.as_view(),
        name='send-group-conversation'),
    url(r'^group/message/(?P<conversation_pk>\d+)/remove/(?P<user_pk>\d+)/$',
        views.group.RemoveParticipant.as_view(), name='remove-participant'),
    url(r'^group/message/(?P<conversation_pk>\d+)/add/(?P<user_pk>\d+)/$',
        views.group.AddParticipant.as_view(), name='add-participant'),

    # API urls
    url(r'^api/newmessage$',
        api.message.GetNewMessages.as_view(), name='new-messages'),
    url(r'^api/loadpreviousmessages$',
        api.message.LoadPreviousMessages.as_view(),
        name='load-previous-messages'),
    url(r'^api/searchuser$',
        api.search.SearchUser.as_view(), name='search-user'),
]
