from django.conf.urls import patterns, include, url
from django.contrib import admin
from optimum import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'optimum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='home'),
    url(r'', include('social_auth.urls')),
    #url(r'^routes', login_required(views.history_routes)),
    url(r'^tracks', login_required(views.tracks)),
    url(r'^path', login_required(views.path)),
    url(r'^notification', login_required(views.send_notification)),
    url(r'^getdata', login_required(views.get_facebook_data)),

    # Authentication module
    url(r'^accounts/', include('allauth.urls')),

)
