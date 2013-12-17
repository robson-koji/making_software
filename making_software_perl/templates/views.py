# -*- coding: utf-8 -*-

from django.db.models.loading import get_model
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.urlresolvers import resolve

#from guardian.mixins import PermissionRequiredMixin
#from guardian.shortcuts import assign_perm
from django.views import generic

from bsct.views import *
from myMixins.mixins import ChkObjOwnershipMixin

from [% views.slug %].models import [% views.slug %]

[% access_control = "" %]
[% created_by_id = "" %]
[% created_by_id_listview = "created_by_id = self.request.user ," %]

[% add_ChkObjOwnershipMixin = "ChkObjOwnershipMixin, " %]
[% view_ChkObjOwnershipMixin = "ChkObjOwnershipMixin, " %]
[% change_ChkObjOwnershipMixin = "ChkObjOwnershipMixin, " %]
[% delete_ChkObjOwnershipMixin = "ChkObjOwnershipMixin, " %]
[% add_PermissionRequiredMixin = "" %]
[% view_PermissionRequiredMixin = "" %]
[% change_PermissionRequiredMixin = "" %]
[% delete_PermissionRequiredMixin = "" %]

[% UNLESS views.access_control %]
# Define controle de acesso para o DetailView e ListView.
# Todos objetos que nao pertencerem ao usuario ADMIN ou STAFF, sao controlados.
# DetailView e ListView do ADMIN e STAFF sao publicos. Para nao mostrar, cortar url e deixar so na interface admin.
[% access_control = "ChkObjOwnershipMixin, " %]
[% created_by_id = "created_by_id = self.request.user ," %]
[% END %]



[% FOREACH relacionamento IN views.relacionamentos %]
from [% relacionamento.relates_to_id %].models import [% relacionamento.relates_to_id %]
[% END %] 

[% permission = views.slug %]
[% FOREACH elemento IN views.permissoes.keys  %]
from [% elemento %].models import [% elemento %]
# Se tiver permissoes setadas, zera o controle do ChkObjOwnershipMixin
    [% access_control = "" %]
    [% IF views.permissoes.$elemento.defined("add_$permission")  %]
        [% add_PermissionRequiredMixin = "PermissionRequiredMixin, " %]
    [% END %] 
    [% IF views.permissoes.$elemento.defined("view_$permission")  %]
        [% created_by_id_listview = "" %]
        [% view_ChkObjOwnershipMixin = "" %]
        [% view_PermissionRequiredMixin = "PermissionRequiredMixin, " %]
    [% END %] 
    [% IF views.permissoes.$elemento.defined("change_$permission")  %]
        [% created_by_id = "" %]
        [% change_ChkObjOwnershipMixin = "" %]
        [% change_PermissionRequiredMixin = "PermissionRequiredMixin, " %]
    [% END %] 
    [% IF views.permissoes.$elemento.defined("delete_$permission") %]
        [% delete_ChkObjOwnershipMixin = "" %]
        [% delete_PermissionRequiredMixin = "PermissionRequiredMixin, " %]
    [% END %] 
[% END %] 


[% IF views.group_perms.exists("add_") %]
    # Checa permissoes de grupo e configura variaveis locais.
    [% add_PermissionRequiredMixin = "PermissionRequiredMixin, " %]
[% END %] 
[% IF views.group_perms.exists("view_") %]
    [% created_by_id_listview = "" %]
    [% view_ChkObjOwnershipMixin = "" %]
    [% view_PermissionRequiredMixin = "PermissionRequiredMixin, " %]
[% END %] 
[% IF views.group_perms.exists("change_") %]
    [% change_ChkObjOwnershipMixin = "" %]
    [% change_PermissionRequiredMixin = "PermissionRequiredMixin, " %]
[% END %] 
[% IF views.group_perms.exists("delete_") %]
    [% delete_ChkObjOwnershipMixin = "" %]
    [% delete_PermissionRequiredMixin = "PermissionRequiredMixin, " %]
[% END %] 


[% IF views.todos_perms.defined("view_") %]
    [% created_by_id_listview = "" %]
    [% view_ChkObjOwnershipMixin = "" %]
[% END %] 
[% IF views.todos_perms.defined("change_") %]
    [% change_ChkObjOwnershipMixin = "" %]
[% END %] 
[% IF views.todos_perms.defined("delete_") %]
    [% delete_ChkObjOwnershipMixin = "" %]
[% END %] 
#import logging
#logger = logging.getLogger("mylog")

   
    
class CreateView_[% views.slug %]( CreateView ):
    return_403 = True    
    [% permission = views.slug %]
    [% FOREACH elemento IN views.permissoes.keys  %]
    [% IF views.permissoes.$elemento.defined("add_$permission") %]
    permission_required = '[% views.slug %].[% "add_$permission" %]'
    [% END %]
    [% END %]

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)

        textos = {}
        textos['app_desc'] = '[% views.app_desc %]'
        textos['subtitulo'] = '[% views.subtitulo %]'

        context.update({
            'textos': textos
        })
        
        # Configura o template de acordo com a interface que usa o sistema
        media_saida = self.kwargs['media_saida']
        self.template_name = 'bsct/plain/'+media_saida+'_form.html'
        return context

    [% IF views.elemento.eh_usuario || views.qt_elementos%]
    # Em caso de relacionamento 1to1 ou de opcao de somente um elemento por usuario,
    # essa funcao verifica se o elemento jah foi preenchido, e ao invehs de retornar o formulario para
    # preenchimento novamente, retorna a pg de detalhe.
    def dispatch(self, request, *args, **kwargs):
        try:
            [% views.slug %]_obj = [% views.slug %].objects.select_related().get(created_by_id = self.request.user)
            media_saida = self.kwargs['media_saida']
            reverso= media_saida+'_[% views.slug %]_detail'
            return HttpResponseRedirect(reverse(reverso, kwargs={'pk':[% views.slug %]_obj.id}))
        except:
            return super(CreateView_[% views.slug %], self).dispatch(request, *args, **kwargs)    
    [% END %]            

    group_field = ''
    user_field = ''
    def form_valid(self, form):
        [% IF views.relacionamentos.size %]
            [% UNLESS views.elemento.eh_usuario %]
        try:
            self.user_field = form.instance.[% relacionamento.relates_to_id %]_field.created_by
        except:
            self.user_field = self.request.user                
            [% END %]        
        [% ELSE %]
        self.user_field = self.request.user
        [% END %]
        [% IF views.elemento.grupo %]
        self.group_field = form.instance.grupo_[% views.slug %]
        [% END %]
        return super(CreateView_[% views.slug %], self).form_valid(form)   

    
    # Se gravou com sucesso, chama a pag de detalhe do objeto de acordo com a interface que usa o sistema
    def get_success_url(self):
        [% FOREACH elemento IN views.permissoes.keys  %]
        #recupera o usuario com base no campo created_by do elemento que estah sendo criado.
        #created_by_[% elemento %] = [% elemento %].objects.get(created_by = self.request.user)
        #usuario_[% elemento %] = created_by_[% elemento %].created_by
        
        usuario_[% elemento %] = self.user_field
        [% IF views.permissoes.$elemento.defined("view_$permission") %]
        # Assinala a permissao.        
        assign_perm("view_[% permission %]", usuario_[% elemento %], self.object)
        [% END %]
        [% IF views.permissoes.$elemento.defined("change_$permission") %]
        assign_perm("change_[% permission %]", usuario_[% elemento %], self.object)
        [% END %]
        [% IF views.permissoes.$elemento.defined("delete_$permission") %]
        assign_perm("delete_[% permission %]", usuario_[% elemento %], self.object)
        [% END %]
        [% END %]

        [% IF views.group_perms.exists("add_") %]
        assign_perm("add_[% permission %]", self.group_field, self.object)
        [% END %]
        [% IF views.group_perms.exists("view_") %]
        assign_perm("view_[% permission %]", self.group_field, self.object)
        [% END %]
        [% IF views.group_perms.exists("change_") %]
        assign_perm("change_[% permission %]", self.group_field, self.object)
        [% END %]
        [% IF views.group_perms.exists("delete_") %]
        assign_perm("delete_[% permission %]", self.group_field, self.object)
        [% END %]

        [% IF views.elemento.eh_usuario %]
        # se for sessao de usuario, sempre assinala todas as permissoes para o usuario.
        assign_perm("view_[% permission %]", self.request.user, self.object)
        assign_perm("change_[% permission %]", self.request.user, self.object)
        assign_perm("delete_[% permission %]", self.request.user, self.object)
        [% IF views.elemento.grupo %]
        g = Group.objects.get(name=self.group_field.name)
        u = self.request.user
        u.groups.add(g)
        [% END %]
        [% END %]
        
        media_saida = self.kwargs['media_saida']
        reverso = media_saida+'_[% views.slug %]_detail'
        return reverse(reverso, kwargs={'pk': (self.object.id)})            


    [% IF views.relacionamentos.size %] 
    def get_form(self, form_class):
        form = super(CreateView_[% views.slug %],self).get_form(form_class) #instantiate using parent
        [% FOREACH relacionamento IN views.relacionamentos %]
            [% IF relacionamento.validade %] 
        form.fields['[% relacionamento.relates_to_id %]_field'].queryset = [% relacionamento.relates_to_id %].objects.filter(validade_check=True)
            [% ELSE %]         
        form.fields['[% relacionamento.relates_to_id %]_field'].queryset = [% relacionamento.relates_to_id %].objects.filter()
            [% END %]         
        [% END %]
        
        return form    
    [% END %] 

 




class UpdateView_[% views.slug %]( [% change_PermissionRequiredMixin %] [% change_ChkObjOwnershipMixin %] UpdateView ):
    return_403 = True        
    [% FOREACH elemento IN views.permissoes.keys  %]
    [% IF views.permissoes.$elemento.defined("change_$permission") %]
    permission_required = '[% views.slug %].[% "change_$permission" %]'
    # Se permissoes estao setadas, desabilita o created_by
    [% END %]
    [% END %]


    [% IF views.group_perms.defined("change_") %]
    # Se tem grupo com permissao concedida eh porque a permissao eh requerida.
    # Enato aqui requere a permissao, com base no que foi configurado no create_project.pl
    permission_required = '[% views.slug %].[% "change_$permission" %]'
    [% END %]
    
    user_field = ''
    group_field = ''
    def form_valid(self, form):
        [% IF views.relacionamentos.size %]
            [% UNLESS views.elemento.eh_usuario %]        
        try:
            self.user_field = form.instance.[% relacionamento.relates_to_id %]_field.created_by
        except:
            self.user_field = self.request.user                
            [% END %]
        [% ELSE %]
        self.user_field = self.request.user
        [% END %]
        
        [% IF views.elemento.grupo %]
        self.group_field = form.instance.grupo_[% views.slug %]
        [% END %]
        return super(UpdateView_[% views.slug %], self).form_valid(form)    
    
    [% IF views.relacionamentos.size %]
    def get_form(self, form_class):
        form = super(UpdateView_[% views.slug %],self).get_form(form_class) #instantiate using parent
        [% FOREACH relacionamento IN views.relacionamentos %]
            [% IF relacionamento.validade %] 
        form.fields['[% relacionamento.relates_to_id %]_field'].queryset = [% relacionamento.relates_to_id %].objects.filter(validade_check=True)
            [% ELSE %]         
        form.fields['[% relacionamento.relates_to_id %]_field'].queryset = [% relacionamento.relates_to_id %].objects.filter()
            [% END %]         
        [% END %]
        return form
    [% END %]

    def get_success_url(self):
        from django.db import connection, transaction
        cursor = connection.cursor()

        [% IF views.elemento.eh_usuario %]
        # Se elemento for do tipo User e houver alteracao de grupo, utiliza API para mudar a tabela
        # auth_user_groups
        try:
            g = Group.objects.get(name=self.group_field.name)
            u = self.request.user
            u.groups.clear()
            u.groups.add(g)
        except:
                pass

        [% ELSE %]
        # Senao, apenas altera o fk do grupo no elemento em questao.
        # Nao tah reconhecendo o content_type. Acertar.
        content_type_id = cursor.execute("SELECT id FROM django_content_type WHERE model = '[% views.slug %]'" )
        #cursor.execute("UPDATE guardian_userobjectpermission SET user_id = %s WHERE object_pk = %s AND content_type_id = %s" , [self.user_field.id, self.kwargs['pk'], content_type_id])
        cursor.execute("UPDATE guardian_userobjectpermission SET user_id = %s WHERE object_pk = %s " , [self.user_field.id, self.kwargs['pk']])
        transaction.commit_unless_managed()
        
        [% IF views.elemento.grupo %]
        content_type_id = cursor.execute("SELECT id FROM django_content_type WHERE model = '[% views.slug %]'" )
        #cursor.execute("UPDATE guardian_groupobjectpermission SET group_id = %s WHERE object_pk = %s AND content_type_id = %s" , [self.group_field.id, self.kwargs['pk'], content_type_id])
        cursor.execute("UPDATE guardian_groupobjectpermission SET group_id = %s WHERE object_pk = %s" , [self.group_field.id, self.kwargs['pk']])
        transaction.commit_unless_managed()
        [% END %]
        [% END %]

        media_saida = self.kwargs['media_saida']
        reverso = media_saida+'_[% views.slug %]_detail'
        return reverse(reverso, kwargs={'pk': (self.object.id)})           


class ListView_[% views.slug %]( ListView ):
    return_403 = True    
    def get_context_data(self, **kwargs):
        media_saida = self.kwargs['media_saida']
        self.template_name = 'bsct/plain/'+media_saida+'_list.html'

        object_list = self.model.objects.filter( [% created_by_id_listview %] )

        reverso_detail = self.kwargs['reverso_detail']
        reverso_create = self.kwargs['reverso_create']

        context = super(ListView_[% views.slug %], self).get_context_data(**kwargs)
        context.update({
            'reverso_detail': reverso_detail, 'reverso_create': reverso_create, 'object_list': object_list
        })
        return context
    
    

class DetailView_[% views.slug %]( [% view_PermissionRequiredMixin %] [% view_ChkObjOwnershipMixin %] DetailView ):
    return_403 = True        
    [% permission = views.slug %]
    [% FOREACH elemento IN views.permissoes.keys  %]
    [% IF views.permissoes.$elemento.defined("view_$permission") %]
    permission_required = '[% views.slug %].[% "view_$permission" %]'
    [% END %]
    [% END %]

    [% IF views.group_perms.exists("view_") %]
    # Se tem grupo com permissao concedida eh porque a permissao eh requerida.
    # Enato aqui requere a permissao, com base no que foi configurado no create_project.pl
    permission_required = '[% views.slug %].[% "view_$permission" %]'
    [% END %]



class DeleteView_[% views.slug %]( [% delete_PermissionRequiredMixin %] [% delete_ChkObjOwnershipMixin %] DeleteView ):
    return_403 = True
    [% permission = views.slug %]
    [% FOREACH elemento IN views.permissoes.keys  %]
    [% IF views.permissoes.$elemento.defined("delete_$permission") %]
    permission_required = '[% views.slug %].[% "delete_$permission" %]'
    # Se permissoes estao setadas, desabilita o created_by
    [% END %]
    [% END %]

    [% IF views.group_perms.defined("delete_") %]
    # Se tem grupo com permissao concedida eh porque a permissao eh requerida.
    # Enato aqui requere a permissao, com base no que foi configurado no create_project.pl
    permission_required = '[% views.slug %].[% "delete_$permission" %]'
    [% END %]
