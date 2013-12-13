

from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from [% urls.slug %] import models
from bsct import views
from [% urls.slug %].views import CreateView_[% urls.slug %], UpdateView_[% urls.slug %], \
                                    ListView_[% urls.slug %], DetailView_[% urls.slug %], DeleteView_[% urls.slug %]

from [% urls.project_name %].decorators import superuser_only, staff_only





urlpatterns = patterns('',
    #                       
    ## Conjunto de URLS para a aplicacao web default
    #
    
    # Se digitar o raiz da app, cai na pagina de instrucoes
    url(r'^$', RedirectView.as_view(url='flat/instrucoes/')), 

    url( r'^add$', [% urls.access_control %](CreateView_[% urls.slug %].as_view( model=models.[% urls.slug %])),
        {'acao': 'Cadastrar', 'media_saida': 'web'}, name = 'web_[% urls.slug %]_create'),
    
    url( r'^update/(?P<pk>\d+)$', [% urls.access_control %](UpdateView_[% urls.slug %].as_view( model=models.[% urls.slug %], success_url = reverse_lazy('fb_app_[% urls.slug %]_list'))),
        {'acao': 'Editar', 'media_saida': 'web',
         'reverso_detail': 'web_[% urls.slug %]_detail'}, name = 'web_[% urls.slug %]_update'),

    url( r'^delete/(?P<pk>\d+)$', [% urls.access_control %](DeleteView_[% urls.slug %].as_view( model=models.[% urls.slug %], success_url = reverse_lazy('web_[% urls.slug %]_list'))),
        {'media_saida': 'web'}, name = 'web_[% urls.slug %]_delete'),
        
    url( r'^list$', (ListView_[% urls.slug %].as_view( model=models.[% urls.slug %], paginate_by = 10 )),
        {'media_saida': 'web',
         'reverso_detail': 'web_[% urls.slug %]_detail',
         'reverso_create': 'web_[% urls.slug %]_create'}, name = 'web_[% urls.slug %]_list'),
    
    url( r'^(?P<pk>\d+)$', (DetailView_[% urls.slug %].as_view( model=models.[% urls.slug %] )),
        {'media_saida': 'web',
         'reverso_update': 'web_[% urls.slug %]_update',
         'reverso_delete': 'web_[% urls.slug %]_delete',
         'reverso_list': 'web_[% urls.slug %]_list'}, name = 'web_[% urls.slug %]_detail'),

    # Se digitar o raiz de update, sem chamar objeto, cai na pagina de listagem
    url( r'^update/$', [% urls.access_control %](ListView_[% urls.slug %].as_view( model=models.[% urls.slug %], paginate_by = 10 )),
        {'media_saida': 'web',
         'reverso_detail': 'web_[% urls.slug %]_detail',
         'reverso_create': 'web_[% urls.slug %]_create'}, name = 'web_[% urls.slug %]_update'),

    
    # Se digitar o raiz de delete, sem chamar objeto, cai na pagina de listagem
    url( r'^delete/$', [% urls.access_control %](ListView_[% urls.slug %].as_view( model=models.[% urls.slug %], paginate_by = 10 )),
        {'media_saida': 'web',
         'reverso_detail': 'web_[% urls.slug %]_detail',
         'reverso_create': 'web_[% urls.slug %]_create'}, name = 'web_[% urls.slug %]_delete'),


    # Se digitar o raiz da app, cai na pagina de cadastro
    #url( r'^$', CreateView_[% urls.slug %].as_view( model=models.[% urls.slug %]),
    #    {'acao': 'Cadastrar'}, name = '[% urls.slug %]_create'),


    #                       
    ## Conjunto de URLS para a aplicacao facebook app
    #
    
    # Se digitar o raiz da app, cai na pagina de instrucoes
    url(r'^fb_app$', RedirectView.as_view(url='flat/fb_app/instrucoes/'), name = 'fb_app_instrucoes'),
    
    url( r'^fb_app/add$', [% urls.access_control %](CreateView_[% urls.slug %].as_view( model=models.[% urls.slug %])),
        {'acao': 'Cadastrar', 'media_saida': 'fb_app'}, name = 'fb_app_[% urls.slug %]_create'),
    
    url( r'^fb_app/update/(?P<pk>\d+)$', [% urls.access_control %](UpdateView_[% urls.slug %].as_view( model=models.[% urls.slug %], success_url = reverse_lazy('fb_app_[% urls.slug %]_list'))),
        {'acao': 'Editar', 'media_saida': 'fb_app',
         'reverso_detail': 'fb_app_[% urls.slug %]_detail'}, name = 'fb_app_[% urls.slug %]_update'),

    url( r'^fb_app/delete/(?P<pk>\d+)$', [% urls.access_control %](DeleteView_[% urls.slug %].as_view( model=models.[% urls.slug %], success_url = reverse_lazy('fb_app_[% urls.slug %]_list'))),
        {'media_saida': 'fb_app'}, name = 'fb_app_[% urls.slug %]_delete'),

    url( r'^fb_app/list$', (ListView_[% urls.slug %].as_view( model=models.[% urls.slug %], paginate_by = 10 )),
        {'media_saida': 'fb_app',
         'reverso_detail': 'fb_app_[% urls.slug %]_detail',
         'reverso_create': 'fb_app_[% urls.slug %]_create'}, name = 'fb_app_[% urls.slug %]_list'),
    
    url( r'^fb_app/(?P<pk>\d+)$', (DetailView_[% urls.slug %].as_view( model=models.[% urls.slug %] )),
        {'media_saida': 'fb_app',
         'reverso_update': 'fb_app_[% urls.slug %]_update',
         'reverso_delete': 'fb_app_[% urls.slug %]_delete',
         'reverso_list': 'fb_app_[% urls.slug %]_list'}, name = 'fb_app_[% urls.slug %]_detail'),

    # Se digitar o raiz de update, sem chamar objeto, cai na pagina de listagem
    url( r'^fb_app/update/$', [% urls.access_control %](ListView_[% urls.slug %].as_view( model=models.[% urls.slug %], paginate_by = 10 )),
        {'media_saida': 'fb_app',
         'reverso_detail': 'fb_app_[% urls.slug %]_detail',
         'reverso_create': 'fb_app_[% urls.slug %]_create'}, name = 'fb_app_[% urls.slug %]_update'),
    
    # Se digitar o raiz de delete, sem chamar objeto, cai na pagina de listagem
    url( r'^fb_app/delete/$', [% urls.access_control %](ListView_[% urls.slug %].as_view( model=models.[% urls.slug %], paginate_by = 10 )),
        {'media_saida': 'fb_app',
         'reverso_detail': 'fb_app_[% urls.slug %]_detail',
         'reverso_create': 'fb_app_[% urls.slug %]_create'}, name = 'fb_app_[% urls.slug %]_delete'),

)
