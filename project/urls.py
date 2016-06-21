from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
import django.contrib.auth.views
from django.contrib import admin
from banana import urls as banana_urls

admin.autodiscover()

urlpatterns = [
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/login/$',
                           django.contrib.auth.views.login,
                           {'template_name':'login.html'},
                           name='login'),
                       url(r'^accounts/logout/$',
                           django.contrib.auth.views.logout, name='logout'),
                       #url(r'^silk/', include('silk.urls', namespace='silk')),
                       url(r'^', include(banana_urls)),
                       ] + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



handler500 = 'banana.views.etc.banana_500'
