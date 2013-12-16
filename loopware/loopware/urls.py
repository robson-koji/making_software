from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',

    # To be used on development environment only
    (r'^static_files/making_software(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),

    # Should not be used on development environment
    # url(  r'^(?i)relacionamentos/', include( 'relacionamentos.urls' ) ),


    url(  r'^(?i)sistema/', include( 'sistema.urls' ) ),    
    url(  r'^(?i)elemento/', include( 'elemento.urls' ) ),
    
    # Se digitar o raiz da app, cai na pagina de instrucoes
    url(  r'^$', TemplateView.as_view(template_name="loopware/html/inicio.html")),

    url(  r'^faq$', TemplateView.as_view(template_name="loopware/html/faq.html")),


    
    url(r'^/flat/instrucoes$', RedirectView.as_view(url='flat/instrucoes/'), name = 'instrucoes'),
    # Isso eh para compatibilizar com o allauth. Ele sempre manda para fb_app_instrucoes apohs o login.
    url(r'^/flat/instrucoes$', RedirectView.as_view(url='flat/instrucoes/'), name = 'fb_app_instrucoes'),

    # Flatpages
    url(r'^flat/', include('django.contrib.flatpages.urls')),

    (r"^wysiwyg_forms/", include("wysiwyg_forms.urls")),

    #All Auth URLS
    url(r'^accounts/', include('allauth.urls')),

    #Admin Urls
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
)
