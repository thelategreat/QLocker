from django.conf.urls.defaults import patterns, include, url
from views import editorView, ajaxEquationView
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qlocker.views.home', name='home'),
    # url(r'^qlocker/', include('qlocker.foo.urls')),
    #url(r'^accounts/login/nav/$', 'atrium.views.auth_nav_partial', name='auth_login_nav'),
    url(r'^qlocker/editor', editorView.as_view(), name='editorView'),
    url(r'^qlocker/convert', ajaxEquationView.as_view(), name='ajaxEquationView'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
