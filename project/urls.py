from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/login/$',
                           'django.contrib.auth.views.login',
                           {'template_name':'login.html'},
                           name='login'),
                       url(r'^accounts/logout/$',
                           'django.contrib.auth.views.logout', name='logout'),
                       url(r'^', include('banana.urls')),
                       ) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



handler500 = 'banana.views.etc.banana_500'
