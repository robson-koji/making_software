# -*- coding: utf-8 -*-

from bsct.views import *
from django.core.urlresolvers import resolve
from django.db.models.loading import get_model
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from elemento.models import Elemento

#import logging
#logger = logging.getLogger("mylog")


class CreateView_relacionamentos( CreateView ):
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)

        textos = {}
        textos['app_desc'] = ''
        textos['subtitulo'] = ''

        context.update({
            'textos': textos
        })
        
        # Configura o template de acordo com a interface que usa o sistema
        self.template_name = 'bsct/plain/form.html'
    
        return context
    
    # Se gravou com sucesso, chama a pag de detalhe do objeto de acordo com a interface que usa o sistema
    def get_success_url(self):
        reverso = 'relacionamentos_detail'
        return reverse(reverso, kwargs={'pk': (self.object.id)})            

    def get_form(self, form_class):
        form = super(CreateView_relacionamentos,self).get_form(form_class) #instantiate using parent
        form.fields['elemento'].queryset = Elemento.objects.filter(sistema_id=self.kwargs['id'])
        form.fields['relates_to'].queryset = Elemento.objects.filter(sistema_id=self.kwargs['id'])
        return form
    
    """
    def dispatch(self, *args, **kwargs):
        #logger.error("PAI:")
        #logger.error(self.kwargs['pai'])
        
        
        from django.db.models.loading import get_model
        model = get_model(self.kwargs['pai'], self.kwargs['pai'])
        #logger.error(self)
        #logger.error(model)
        

        # Esse objeto Sistema precisa ir para o urls.py e passar como argumento
        self.pai_id = get_object_or_404(model, pk=kwargs['id'])

        return super(CreateView, self).dispatch(*args, **kwargs)
    """
        
    """    
    def form_valid(self, form):
        
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        
        obj.sistema = self.pai_id
        
        obj.save()
        #return super(ElementoCreateView, self).form_valid(form)
        return super(OverrideSaveMixin, self).form_valid(form)
    
    
    def get_success_url(self):
            return '/%s/%s' % (self.kwargs['pai'], self.kwargs['id'])
    """

class UpdateView_relacionamentos( UpdateView ):
    def get_form(self, form_class):
        form = super(UpdateView_relacionamentos,self).get_form(form_class) #instantiate using parent
        form.fields['elemento'].queryset = Elemento.objects.filter(sistema_id=self.kwargs['id'])
        form.fields['relates_to'].queryset = Elemento.objects.filter(sistema_id=self.kwargs['id'])
        return form
    

    
    """
    def get_success_url(self):
            return '/%s/%s' % (self.kwargs['pai'], self.kwargs['id'])
    """


class ListView_relacionamentos( ListView ):
    template_name = 'loopware/relacionamentos_list.html'

    """
    def get_success_url(self):
            return '/%s/%s' % (self.kwargs['pai'], self.kwargs['id'])
    """


class DetailView_relacionamentos( DetailView ):
    template_name = 'loopware/relacionamentos_detail.html'

    """
    def dispatch(self, *args, **kwargs):
        #logger.error("Dispatch:")
        
        if self.model._meta.get_all_related_objects():
            #if self.model._meta.get_all_related_objects():
            #logger.error(self.model._meta.get_all_related_objects())
    
            # Captura uma lista de objetos relacionados via FK
            objeto_lista = self.model._meta.get_all_related_objects()
            
            # Precisa iterar. Por enquanto pegando somente o primeiro
            model_label = objeto_lista[0].model._meta.app_label
    
            # Recupera o model do objeto relacionado
            self.related_model = get_model(model_label, model_label)    
        return super(DetailView, self).dispatch(*args, **kwargs)               

    """
    # Update no contexto, retornando lista de elementos e formularios relacionados.
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        textos = {}
        textos['app_desc'] = ''

        context.update({
            'textos': textos
        })
        return context

class DeleteView( DeleteView ):
    """
    def get_success_url(self):
            return '/%s/%s' % (self.kwargs['pai'], self.kwargs['id'])
    """
