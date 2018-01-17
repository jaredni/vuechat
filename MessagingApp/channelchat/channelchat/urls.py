"""channelchat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from messaging import views as messaging_views

urlpatterns = [
    url(r'^messaging/', include('messaging.urls', namespace="messaging")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^$', messaging_views.base.IndexView.as_view(), name='home'),
]

handler400 = messaging_views.base.ErrorView.as_view()
handler403 = messaging_views.base.ErrorView.as_view()
# handler404 = messaging_views.base.ErrorView.as_view()
handler500 = messaging_views.base.ErrorView.as_view()
