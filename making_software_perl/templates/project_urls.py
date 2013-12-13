
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

# Monta URL para chamar cada APP
[% FOREACH app = urls.apps %]
    [% NEXT UNLESS app.forms %]
    url(  r'^(?i)[% app.slug %]/', include( '[% app.slug %].urls' ) ),
[% END %]

    # Essa parte de flatpage nao estah boa, precisa refazer.
    # Se digitar o raiz da app, cai na pagina de instrucoes
    url(r'^$', RedirectView.as_view(url='flat/bem-vindo/'), name='bem-vindo'),
    url(r'^/instrucoes$', RedirectView.as_view(url='flat/instrucoes/'), name = 'instrucoes'),
    
    url(r'^fb_app$', RedirectView.as_view(url='flat/fb_app/bem-vindo/'), name='fb_app_bem-vindo'),     
    url(r'^/fb_app/instrucoes$', RedirectView.as_view(url='flat/fb_app/instrucoes/'), name = 'fb_app_instrucoes'),

    # Flatpages
    url(r'^flat/', include('django.contrib.flatpages.urls')),

    #All Auth URLS
    url(r'^accounts/', include('allauth.urls')),
    
    #Admin Urls
    url(r'^administrativo/', include(admin.site.urls)),
)
