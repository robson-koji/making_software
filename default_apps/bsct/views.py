"""
These views do nothing other than provide members of the 'plain' BSCT template
set as default template names.
"""
from django.views import generic
from myMixins.mixins import LoginRequiredMixin, ChkObjOwnershipMixin, OverrideSaveMixin, UpdateContextMixin
from django.core.urlresolvers import resolve
from django.db.models.loading import get_model
from django.core.urlresolvers import reverse

from django.shortcuts import get_object_or_404



#import logging
#logger = logging.getLogger("mylog")

class CreateView( UpdateContextMixin, OverrideSaveMixin, LoginRequiredMixin, generic.CreateView ):
    #template_name = 'bsct/plain/form.html'
        
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

class UpdateView( UpdateContextMixin, LoginRequiredMixin, generic.UpdateView ):
    def dispatch(self, *args, **kwargs):
        media_saida = self.kwargs['media_saida']
        self.template_name = 'bsct/plain/'+media_saida+'_form.html'
        return super(UpdateView, self).dispatch(*args, **kwargs)               
    
    def get_success_url(self):
        reverso = self.kwargs['reverso_detail']
        return reverse(reverso, kwargs={'pk': (self.object.id)})             
          
class ListView( LoginRequiredMixin, generic.ListView ):
    """
    def get_queryset(self):
        media_saida = self.kwargs['media_saida']
        self.template_name = 'bsct/plain/'+media_saida+'_list.html'

        object_list = self.model.objects.filter( created_by_id = self.request.user )
        return object_list
    def get_context_data(self, **kwargs):
        media_saida = self.kwargs['media_saida']
        self.template_name = 'bsct/plain/'+media_saida+'_list.html'

        object_list = self.model.objects.filter( created_by_id = self.request.user )

        reverso_detail = self.kwargs['reverso_detail']
        reverso_create = self.kwargs['reverso_create']

        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'reverso_detail': reverso_detail, 'reverso_create': reverso_create, 'object_list': object_list
        })
        return context
    """


class DetailView( LoginRequiredMixin, generic.DetailView ):
    #template_name = 'bsct/plain/detail.html'
    
    def dispatch(self, *args, **kwargs):
        #logger.error("Dispatch:")
        media_saida = self.kwargs['media_saida']
        self.template_name = 'bsct/plain/'+media_saida+'_detail.html'
        
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


    def get_context_data(self, **kwargs):
        reverso_update = self.kwargs['reverso_update']
        reverso_delete = self.kwargs['reverso_delete']
        reverso_list = self.kwargs['reverso_list']

        context = super(DetailView, self).get_context_data(**kwargs)
        context.update({
            'reverso_update': reverso_update, 'reverso_delete': reverso_delete, 'reverso_list': reverso_list
        })
        return context


    """
    # Update no contexto, retornando lista de elementos e formularios relacionados.
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        elemento_lista = []
        if hasattr(self, 'related_model'):
            for elemento in Elemento.objects.all():
                forms = Form.objects.filter( elemento_id = elemento.id)
                    if forms:
                    setattr(elemento, 'forms', forms)
                            
                elemento_lista.append(elemento)

            context.update({
                'objeto_lista': elemento_lista
            })
        return context
    """

class DeleteView( LoginRequiredMixin, generic.DeleteView ):
    #template_name = 'bsct/plain/confirm_delete.html'
    def dispatch(self, *args, **kwargs):
        media_saida = self.kwargs['media_saida']
        self.template_name = 'bsct/plain/'+media_saida+'_confirm_delete.html'
        return super(DeleteView, self).dispatch(*args, **kwargs)               
        
