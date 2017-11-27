from django.conf.urls import *
from django.contrib import admin
from optimum import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Examples:
    # url(r'^$', 'optimum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='home'),
    url(r'^survey/$', views.survey_redirect, name='survey_redirect'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),    
    #url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

]
