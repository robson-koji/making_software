# -*- coding: utf-8 -*-

# Django modules
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

# My modules
from django.core.urlresolvers import reverse

# Meus pacotes
from elemento.models import Elemento, ElementoForm

# 3rd part modules
from bsct import views    

"""
import logging
logger = logging.getLogger("mylog")
logger.error("")

"""

class ElementoDetailListView( views.DetailView ):
    model = Elemento
    context_object_name = 'detailview'
    template_name = 'loopware/elemento_detail_list.html'      


class ElementoDetailView( views.DetailView ):
    def get_success_url(self):
            return '/%s/%s' % (self.kwargs['pai'], self.kwargs['id'])
        

class ElementoCreateView( views.CreateView ):
    def get_success_url(self):
        return reverse('sistema_detail', kwargs={'pk': self.kwargs['id']})
    
    def get_context_data(self, **kwargs):
        context = super(ElementoCreateView, self).get_context_data(**kwargs)

        textos = {}
        textos['app_desc'] = 'Digite as informações abaixo para criar uma sessão do seu sistema. Você pode criar quantas sessões quiser. <br> \
        Esse é o terceiro passo na criação do seu sistema. \
        Após definir as sessões, você criará os formulários do sistema.'

        context.update({
            'textos': textos
        })
        return context   


class ElementoUpdateView( views.UpdateView ):
    def get_success_url(self):
        return reverse('sistema_detail', kwargs={'pk': self.kwargs['id']}) 
        