from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView

#from django.views import generic
from sistema import models
#from crud.views import CreateView2
from bsct import views

from sistema.views import SistemaCreateView, SistemaListView, SistemaDetailListView, SistemaPublicarView, SistemaPublicarConfirmaView,SistemaMudaTemplateView,SistemaUpdateView


urlpatterns = patterns('',
    url( r'^mudar_template/(?P<template>\w+)$', SistemaMudaTemplateView.as_view(),
         name = 'mudar_template'),

    url( r'^publicar_confirma/(?P<pk>\d+)$', SistemaPublicarConfirmaView.as_view( ),
         name = 'sistema_publicar_confirma'),
    
    url( r'^publicar/(?P<pk>\d+)$', SistemaPublicarView.as_view(),
         name = 'sistema_publicar'),
    
    url( r'^add/$', SistemaCreateView.as_view( model=models.Sistema),
        {'acao': 'Criar'}, name = 'sistema_create'),

    url( r'^update/(?P<pk>\d+)$', SistemaUpdateView.as_view( model=models.Sistema ),
        {'acao': 'Editar'}, name = 'sistema_update'),
    
    # Essas duas urls _template sao somente para apresentar o template na tela do formulario.
    # Seja na criacao ou na edicao do sistema.
    url( r'^add/(?P<template>\d+)/$', SistemaCreateView.as_view( model=models.Sistema),
        {'acao': 'Criar'}, name = 'sistema_create_template'),

    url( r'^update/(?P<pk>\d+)/(?P<template>\d+)/$', SistemaUpdateView.as_view( model=models.Sistema ),
        {'acao': 'Editar'}, name = 'sistema_update_template'),

    # Se digitar a home de entidade, cai na listagem.
    # Qdo faz o login, o urls.py do projeto joga aqui.
    url( r'^$', views.ListView.as_view( model=models.Sistema, paginate_by = 3 ), 
        name = 'sistema_list_inicial'),

    url( r'^list$', SistemaListView.as_view( paginate_by = 3 ), 
        name = 'sistema_list'),

    #url( r'^list$', views.ListView.as_view( model=models.Sistema, paginate_by = 3 ), 
    #    name = 'sistema_list'),

    url( r'^(?P<pk>\d+)$', SistemaDetailListView.as_view( model=models.Sistema ),        
        name = 'sistema_detail'),

    url( r'^delete/(?P<pk>\d+)$', views.DeleteView.as_view( model=models.Sistema, success_url = reverse_lazy('sistema_list')),
        name = 'sistema_delete'
    ),
)
