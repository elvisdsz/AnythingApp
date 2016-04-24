from django.conf.urls import patterns,url

from cards import views

urlpatterns = patterns('',
                       url(r'^$',views.index,name='index'),
                       )
