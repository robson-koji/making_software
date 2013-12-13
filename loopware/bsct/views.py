"""
These views do nothing other than provide members of the 'plain' BSCT template
set as default template names.
"""
from django.views import generic
from myMixins.mixins import LoginRequiredMixin, ChkObjOwnershipMixin, OverrideSaveMixin, UpdateContextMixin
from django.core.urlresolvers import resolve
from django.db.models.loading import get_model
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from sistema.models import Sistema
from elemento.models import Elemento


from wysiwyg_forms.models import Form

import logging
logger = logging.getLogger("mylog")


class CreateView( UpdateContextMixin, OverrideSaveMixin, LoginRequiredMixin, generic.CreateView ):
    template_name = 'bsct/plain/form.html'
        
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
    """
    
    #def get_success_url(self):
    #        return '/%s/%s' % (self.kwargs['pai'], self.kwargs['id'])
    

class UpdateView( UpdateContextMixin, LoginRequiredMixin, ChkObjOwnershipMixin, generic.UpdateView ):
    template_name = 'bsct/plain/form.html'
    #def get_success_url(self):
    #        return '/%s/%s' % (self.kwargs['pai'], self.kwargs['id'])



class ListView( LoginRequiredMixin, ChkObjOwnershipMixin, generic.ListView ):
    template_name = 'bsct/plain/list.html'



class DetailView( LoginRequiredMixin, ChkObjOwnershipMixin, generic.DetailView ):
    template_name = 'bsct/plain/detail_list.html'
    
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


    # Update no contexto, retornando lista de elementos e formularios relacionados.
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        elemento_lista = []
        if hasattr(self, 'related_model'):
            for elemento in Elemento.objects.filter(sistema_id=self.kwargs['pk']):
            #for elemento in Elemento.objects.all():
                forms = Form.objects.filter( elemento_id = elemento.id)
                if forms:
                    setattr(elemento, 'forms', forms)
                    
                elemento_lista.append(elemento)

            context.update({
                'objeto_lista': elemento_lista
            })
        return context


        
        



class DeleteView( LoginRequiredMixin, ChkObjOwnershipMixin, generic.DeleteView ):
    template_name = 'bsct/plain/confirm_delete.html'
    def get_success_url(self):
        if 'pai' in self.kwargs:
            return '/making_software/%s/%s' % (self.kwargs['pai'], self.kwargs['id'])
        else:
            return reverse('sistema_list')
            
