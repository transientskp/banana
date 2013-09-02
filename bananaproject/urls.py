from django.conf.urls import patterns, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       (r'^admin/', include(admin.site.urls)),
                       (r'^sqlconsole/', include('sqlconsole.urls')),
                       (r'^accounts/login/$',
                            'django.contrib.auth.views.login',
                            {'template_name': 'login.html'}),
                       (r'^', include('banana.urls')),

                       ) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



handler500 = 'banana.views.etc.banana_500'