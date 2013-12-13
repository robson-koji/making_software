from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy

#from elemento.views import ElementoCreateView, ElementoDetailListView, ElementoUpdateView

from elemento.views import ElementoDetailListView, ElementoDetailView, ElementoCreateView, ElementoUpdateView
from elemento import models

from bsct import views




urlpatterns = patterns('',
    url( r'^add$', views.CreateView.as_view( model=models.Elemento),
        {'acao': 'Cadastrar'}, name = 'elemento_create'),        
    
    url( r'^update/(?P<pk>\d+)$', views.UpdateView.as_view( model=models.Elemento ),
        {'acao': 'Editar'}, name = 'elemento_update', ),

    url( r'^update/(?P<pk>\d+)/(?P<pai>\w+)/(?P<id>\d+)$', ElementoUpdateView.as_view( model=models.Elemento ),
        {'acao': 'Editar'}, name = 'elemento_update', ),

    # Estah herdando a classe CreateView na View e redirecionando para o Detail de Sistema.
    url( r'^add/(?P<pai>\w+)/(?P<id>\d+)$', ElementoCreateView.as_view( model=models.Elemento),
        {'acao': 'Cadastrar'}, name = 'elemento_create'),        

    url( r'^(?P<pk>\d+)$', ElementoDetailListView.as_view( model=models.Elemento ),        
        name = 'elemento_detail'),

    url( r'^delete/(?P<pk>\d+)$', views.DeleteView.as_view( model=models.Elemento, success_url = reverse_lazy('sistema_list')),
        name = 'elemento_delete'
    ),
    
    url( r'^delete/(?P<pk>\d+)/(?P<pai>\w+)/(?P<id>\d+)$', views.DeleteView.as_view( model=models.Elemento, success_url = reverse_lazy('sistema_list')),
        name = 'elemento_delete'
    ),
)




    
