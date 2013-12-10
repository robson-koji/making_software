# -*- coding: utf-8 -*-

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models.loading import get_model
from django.http import HttpResponse, Http404
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.core.exceptions import PermissionDenied


import logging
logger = logging.getLogger("mylog")



# Identificando que o Mixin eh para ser utilizado por uma classe Model.
class Model_GetRelatedObject_Mixin(object):
    def get_related_objects(self):
         #a[0].model._meta.verbose_name
        #return self._meta.get_all_related_objects()[0].model._meta.verbose_name
        return self._meta.get_all_related_objects()
    
    

#http://brack3t.com/our-custom-mixins.html
class LoginRequiredMixin(object):
    """
    View mixin which verifies that the user has authenticated.

    NOTE:
        This should be the left-most mixin of a view.
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
        
        

#http://stackoverflow.com/questions/5531258/example-of-django-class-based-deleteview    
class ChkObjOwnershipMixin(object):    
    def get_object(self, queryset=None):
        # Hook to ensure object is owned by request.user. 
        obj = super(ChkObjOwnershipMixin, self).get_object()
        if not obj.created_by == self.request.user:
            raise PermissionDenied
        return obj


class UpdateContextMixin( object ):
    # Passa no contexto a acao que estah sendo executada
    # Cadastra ou Edita.
    # Como o formulario eh o mesmo para as duas acoes,
    # a acao eh identificada atraves de argumento passado na url
    def get_context_data(self, **kwargs):
        context = super(UpdateContextMixin, self).get_context_data(**kwargs)
        context.update({
            'acao': self.kwargs['acao'],
        })
        return context
    

class OverrideSaveMixin( object ):
    # Seta dinamicamente os campos created_by e o campo FK.
    def form_valid(self, form):
        obj = form.save(commit=False)

        # Captura o valor created_by no request.
        obj.created_by = self.request.user



        if 'pai' in self.kwargs:
            # Captura o model atraves da string passada na URL. p.ex:
            # http://192.168.43.100:8090/elemento/add/sistema/1
            # self.kwargs['pai'] = "sistema" da URL
            # self.kwargs['id'] = "1" da URL            
            model = get_model(self.kwargs['pai'], self.kwargs['pai'])
            
            # Captur o campo PK e o valor atraves dos parametros do request (formato da URL conforme descrito acima),
            # e demais methodos auxiliares utilizados.
            # Seta o valor do campo "campo" com o valor do self.pai_id no objeto obj.            
            self.pai_id = get_object_or_404(model, pk=self.kwargs['id'])
            campo = model._meta.app_label
            setattr(obj, campo, self.pai_id) 

            """
            logger.error("PAI:")
            logger.error(self.kwargs['pai'])
            logger.error(campo)
            logger.error(self.pai_id)
            """

        try:
            obj.save()
            return super(OverrideSaveMixin, self).form_valid(form)
        
        except IntegrityError, e:
            #return render_to_response("error/template.html", {"message": e.message})
            return render_to_response("error/template.html", {"message": "Esse formulário já foi preenchido"})
        
        
#        obj.save()
#        return super(OverrideSaveMixin, self).form_valid(form)        



    """        
    def dispatch(self, *args, **kwargs):
        #logger.error("PAI:")
        logger.error(self.kwargs['acao'])
        
        self.extra_context = {'acao':'asdfasdfasdf'}
        
      
        return super(OverrideSaveMixin, self).dispatch(*args, **kwargs)
    """
    
    
    """
    def get_queryset(self):
        campo = self.args[0]
        valor = self.args[1]
    """
        
