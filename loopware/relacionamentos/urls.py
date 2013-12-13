from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from relacionamentos import models
from bsct import views
from relacionamentos.views import CreateView_relacionamentos, DetailView_relacionamentos, ListView_relacionamentos, UpdateView_relacionamentos


urlpatterns = patterns('',
    # Se digitar o raiz da app, cai na pagina de instrucoes
    url(r'^$', RedirectView.as_view(url='flat/instrucoes/')),

    url( r'^add/(?P<pai>\w+)/(?P<id>\d+)$', (CreateView_relacionamentos.as_view( model=models.relacionamentos)),
        {'acao': 'Cadastrar'}, name = 'relacionamentos_create'),

    # Add sem definir Sistema, vai para listagem.
    url( r'^add$', (ListView_relacionamentos.as_view( model=models.relacionamentos, paginate_by = 10 )),
        {'acao': 'Cadastrar'}, name = 'relacionamentos_create'),

    url( r'^update/(?P<pk>\d+)$', (UpdateView_relacionamentos.as_view( model=models.relacionamentos, success_url = reverse_lazy('relacionamentos_list'))),
        {'acao': 'Editar', 'reverso_detail': 'relacionamentos_detail'}, name = 'relacionamentos_update'),

    url( r'^update/(?P<pk>\d+)/(?P<pai>\w+)/(?P<id>\d+)$', (UpdateView_relacionamentos.as_view( model=models.relacionamentos, success_url = reverse_lazy('relacionamentos_list'))),
        {'acao': 'Editar', 'reverso_detail': 'relacionamentos_detail'}, name = 'relacionamentos_update'),


    # Se digitar o raiz de update, sem chamar objeto, cai na pagina de listagem
    url( r'^update/$', (ListView_relacionamentos.as_view( model=models.relacionamentos, paginate_by = 10 )),
        name = 'relacionamentos_update'),

        
    url( r'^list$', (ListView_relacionamentos.as_view( model=models.relacionamentos, paginate_by = 10 )),
        name = 'relacionamentos_list'),
    
    url( r'^(?P<pk>\d+)$', (DetailView_relacionamentos.as_view( model=models.relacionamentos )),
        name = 'relacionamentos_detail'),


    url( r'^delete$',  (ListView_relacionamentos.as_view( model=models.relacionamentos, paginate_by = 10 )),
        name = 'relacionamentos_delete'),
    
    url( r'^delete/(?P<pk>\d+)$', views.DeleteView.as_view( model=models.relacionamentos, success_url = reverse_lazy('relacionamentos_list')),
        name = 'relacionamentos_delete'),
    
    
)

