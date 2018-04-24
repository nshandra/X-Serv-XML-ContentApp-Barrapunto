# project URL Configuration

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'ContentApp.views.main'),
    url(r'^update$', 'ContentApp.views.update'),
    url(r'^(.+)$', 'ContentApp.views.get_page')
]
