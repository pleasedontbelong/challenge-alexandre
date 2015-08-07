"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns

from segmentsconfigapp import views
from segmentsconfigapp.views import SegmentsConfigViewSet
from segmentsconfigapp.views import RulesResultViewSet

segmentsconfig_createrules = SegmentsConfigViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

applyrule = RulesResultViewSet.as_view({
    'post': 'list_matched',
})

urlpatterns = [

    url(r'^segments_config/$', segmentsconfig_createrules, name='segmentsconfig-viewset'),
    url(r'^segments_config/(?P<segments_config_id>.+)/check_urls', applyrule, name='segmentsconfig-viewset-applyrules'),
]

