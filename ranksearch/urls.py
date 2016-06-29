from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^fixer/(?P<slug>[\w\-]+)/$', views.fixer, name='fixer'),
    url(r'^owner/(?P<slug>[\w\-]+)/$', views.owner, name='owner'),
    url(r'^property/(?P<slug>[\w\-]+)/$', views.property, name='property'),
]
