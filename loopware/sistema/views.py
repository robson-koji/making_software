# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic.base import View
from django.shortcuts import redirect

from django.conf import settings
from django.views import generic
import re #regex


# Meus pacotes
from myMixins.mixins import LoginRequiredMixin, ChkObjOwnershipMixin
from sistema.models import Sistema, SistemaForm
from elemento.models import Elemento

# Pacotes de terceiro
from bsct import views    
from wysiwyg_forms.models import Form, Field

import logging
logger = logging.getLogger("mylog")



class SistemaMudaTemplateView(LoginRequiredMixin, ChkObjOwnershipMixin, DetailView):
    def get(self, request, *args, **kwargs):
        res = ''
        url = ''
        m_create = re.compile("add")
        m_update = re.compile("update")
        if m_create.search(request.META.get('HTTP_REFERER')):
            res = 'sistema_create_template'
            url = reverse(res, kwargs={'template':'1'})
        
        elif m_update.search(request.META.get('HTTP_REFERER')):
            res = 'sistema_update_template'
            pk = re.findall('^.*/update/([0-9]+)', request.META.get('HTTP_REFERER'))
            url = reverse(res, kwargs={'pk': pk[0], 'template':'1'})

        request.session['template'] = self.kwargs['template']
        return HttpResponseRedirect(url)



class SistemaPublicarConfirmaView(LoginRequiredMixin, ChkObjOwnershipMixin, DetailView):
    model = Sistema
    template_name = 'loopware/sistema_publicar_confirma.html'        
    #def get(self, request, *args, **kwargs):
    
        
    def get_context_data(self, **kwargs):
        context = super(SistemaPublicarConfirmaView, self).get_context_data(**kwargs)
        
        sistema = Sistema.objects.get(id=self.kwargs['pk'])
        #return render_to_response('loopware/sistema_publicar_confirma.html', {'sistema':sistema})

        sistema_finalizado = ''

        # Verifica se existem fields no final da cadeia do sistema.
        # Caso positivo o sistema estah finalizado.
        elementos = Elemento.objects.filter( sistema_id = sistema.id)
        if elementos:
            for elemento in elementos:
                forms = Form.objects.filter( elemento_id = elemento.id)
                if forms:
                    fields = Field.objects.filter( form_id = forms[0].id)
                    if fields:
                        sistema_finalizado = '1'
                            


        # Isso aqui precisa passar para uma classe e herdar dessa classe.
        sistema_status = {}
        elementos = Elemento.objects.filter( sistema_id = sistema.id)
        if elementos:
            sistema_status['elementos'] = '<span class="label label-success"> OK!  </span>'

            for elemento in elementos:
                forms = Form.objects.filter( elemento_id = elemento.id)
                if forms:
                    sistema_status['forms'] = '<span class="label label-success"> OK!  </span>'

                    # Nao sei pq merda, aqui soh funciona se colocar o forms[0].
                    # se tentar iterar forms dah merda e nao funciona.
                    #for form in forms:
                    fields = Field.objects.filter( form_id = forms[0].id)
                    if fields:
                        sistema_status['fields'] = '<span class="label label-success"> OK!  </span>'
                    else:
                        sistema_status['fields'] = '<span class="label label-danger"> NOK!  </span>'

                else:
                    sistema_status['forms'] = '<span class="label label-danger"> NOK!  </span>'
                    sistema_status['fields'] = '<span class="label label-danger"> NOK!  </span>'

        else:
            sistema_status['elementos'] = '<span class="label label-danger"> NOK!  </span>'
            sistema_status['forms'] = '<span class="label label-danger"> NOK!  </span>'
            sistema_status['fields'] = '<span class="label label-danger"> NOK!  </span>'
                                
        context.update({
            'sistema_finalizado': sistema_finalizado, 'sistema':sistema, 'sistema_status': sistema_status

        })
        return context



class SistemaPublicarView(LoginRequiredMixin, ChkObjOwnershipMixin, DetailView):
    def get(self, request, *args, **kwargs):
        import subprocess

        #pipe = subprocess.Popen(['/usr/bin/sudo', '/usr/bin/perl', '/devel/inteliform_perl/create_project.pl', self.kwargs['pk']], stdout=subprocess.PIPE)
        pipe = subprocess.Popen(['/usr/bin/sudo', '/usr/bin/perl', settings.PERL_CREATE_PROJECT, self.kwargs['pk'], settings.INTELIFORM_PERL_DIR], stdout=subprocess.PIPE)
        result = pipe.stdout.read() # this is the output of the process

        sistema = Sistema.objects.get(id=self.kwargs['pk'])
        
        return render_to_response('loopware/sistema_inicializacao.html', {'result':result, 'sistema':sistema, 'subdominio_projetos': settings.SUBDOMINIO_PROJETOS, 'ambiente':settings.AMBIENTE, 'id':self.kwargs['pk'] })



class SistemaCreateView( views.CreateView ):
    form_class = SistemaForm
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        if not 'template' in self.request.session:
                self.request.session['template'] = 'flatly'
        
        obj.template = self.request.session['template']
        obj.save()
        return super(SistemaCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(SistemaCreateView, self).get_context_data(**kwargs)

        textos = {}
        textos['app_desc'] = 'Digite as informações abaixo para criar o seu sistema. <br> Lembre-se que em apenas 4 passos você cria o seu sistema, e você está no passo número 2.'
        textos['template'] = '1'

        # Nao entendo aqui.
        # Ele deveria pegar o kwargs template e setar a variavel template que estah
        # sendo monitorada no base.html. Porem nao pega no kwargs o template, entao setando fora da verificacao mesmo.
        template = '1'

        # Primeira criacao de sistema. Ainda nao tem sessao, entao usa o template default no base.html
        if 'template' not in self.request.session:
            template = ''

            
        context.update({
            'textos': textos, 'template': template
        })
        return context        


class SistemaUpdateView( views.UpdateView) :
    form_class = SistemaForm
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        if not 'template' in self.request.session:
                self.request.session['template'] = 'flatly'
                
        obj.template = self.request.session['template']
        obj.save()
        return super(SistemaUpdateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(SistemaUpdateView, self).get_context_data(**kwargs)

        textos = {}
        textos['app_desc'] = 'Edite as informações abaixo e clique no botão salvar.'
        textos['template'] = '1'
        
        # Nao entendo aqui.
        # Ele deveria pegar o kwargs template e setar a variavel template que estah
        # sendo monitorada no base.html. Porem nao pega no kwargs o template, entao setando fora da verificacao mesmo.
        template = '1'


        # Primeira edicao de sistema, pode nao ter sessao, entao usa o template default no base.html
        if 'template' not in self.request.session:
            template = ''
            
            
            
        context.update({
            'textos': textos, 'template': template
        })
        return context        


class SistemaListView( views.ListView ):
    model = Sistema
    template_name = 'loopware/sistema_list.html'    

    """
    def get_context_object_name(self, object_list):
        for sistema in object_list:
            setattr(sistema, 'foo', 'bar')

        pass
        #for sistema in object_list:
        #    sistema.foo = 'bar'
        
    """

    # Update no contexto, retornando lista de elementos e formularios relacionados.
    def get_context_data(self, **kwargs):
        context = super(SistemaListView, self).get_context_data(**kwargs)

        sistema_lista = []

        # Dah para iterar direto por objeto.
        # Corrigir.
        #for sistema in Sistema.objects.all():
        for sistema in Sistema.objects.filter( created_by_id = self.request.user ):
            elementos = Elemento.objects.filter( sistema_id = sistema.id)
            if elementos:
                setattr(sistema, 'elementos', '<span class="label label-success"> OK!  </span>')

                for elemento in elementos:
                    forms = Form.objects.filter( elemento_id = elemento.id)
                    if forms:
                        setattr(sistema, 'forms', '<span class="label label-success"> OK!  </span>')

                        # Nao sei pq merda, aqui soh funciona se colocar o forms[0].
                        # se tentar iterar forms dah merda e nao funciona.
                        #for form in forms:
                        fields = Field.objects.filter( form_id = forms[0].id)
                        if fields:
                            setattr(sistema, 'fields', '<span class="label label-success"> OK!  </span>')
                        else:
                            setattr(sistema, 'fields', '<span class="label label-danger"> NOK!  </span>')

                    else:
                        setattr(sistema, 'forms', '<span class="label label-danger"> NOK!  </span>')
                        setattr(sistema, 'fields', '<span class="label label-danger"> NOK!  </span>')

            else:
                setattr(sistema, 'elementos', '<span class="label label-danger"> NOK!  </span>')
                setattr(sistema, 'forms', '<span class="label label-danger"> NOK!  </span>')
                setattr(sistema, 'fields', '<span class="label label-danger"> NOK!  </span>')
                                
            sistema_lista.append(sistema)

        context.update({
            'objeto_lista': sistema_lista, 'subdominio_projetos': settings.SUBDOMINIO_PROJETOS
        })
        return context
    

        
class SistemaDetailListView( views.DetailView ):
    model = Sistema
    template_name = 'loopware/sistema_detail_list.html'    

    def get_context_data(self, **kwargs):
        context = super(SistemaDetailListView, self).get_context_data(**kwargs)
        
        sistema = Sistema.objects.get(id=self.kwargs['pk'])
        #return render_to_response('loopware/sistema_publicar_confirma.html', {'sistema':sistema})

        sistema_finalizado = ''

        # Verifica se existem fields no final da cadeia do sistema.
        # Caso positivo o sistema estah finalizado.
        elementos = Elemento.objects.filter( sistema_id = sistema.id)
        if elementos:
            for elemento in elementos:
                forms = Form.objects.filter( elemento_id = elemento.id)
                if forms:
                    fields = Field.objects.filter( form_id = forms[0].id)
                    if fields:
                        sistema_finalizado = '1'
                            


        # Isso aqui precisa passar para uma classe e herdar dessa classe.
        sistema_status = {}
        elementos = Elemento.objects.filter( sistema_id = sistema.id)
        if elementos:
            sistema_status['elementos'] = '<span class="label label-success"> OK!  </span>'

            for elemento in elementos:
                forms = Form.objects.filter( elemento_id = elemento.id)
                if forms:
                    sistema_status['forms'] = '<span class="label label-success"> OK!  </span>'

                    # Nao sei pq merda, aqui soh funciona se colocar o forms[0].
                    # se tentar iterar forms dah merda e nao funciona.
                    #for form in forms:
                    fields = Field.objects.filter( form_id = forms[0].id)
                    if fields:
                        sistema_status['fields'] = '<span class="label label-success"> OK!  </span>'
                    else:
                        sistema_status['fields'] = '<span class="label label-danger"> NOK!  </span>'

                else:
                    sistema_status['forms'] = '<span class="label label-danger"> NOK!  </span>'
                    sistema_status['fields'] = '<span class="label label-danger"> NOK!  </span>'

        else:
            sistema_status['elementos'] = '<span class="label label-danger"> NOK!  </span>'
            sistema_status['forms'] = '<span class="label label-danger"> NOK!  </span>'
            sistema_status['fields'] = '<span class="label label-danger"> NOK!  </span>'
                                
        context.update({
            'sistema_finalizado': sistema_finalizado, 'sistema':sistema, 'sistema_status': sistema_status, 'subdominio_projetos': settings.SUBDOMINIO_PROJETOS
        })
        return context

    
    
