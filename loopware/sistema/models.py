# -*- coding: utf-8 -*- 

from myMixins.mixins import Model_GetRelatedObject_Mixin
from django.template.defaultfilters import slugify
from django.core.validators import RegexValidator

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models

# Meus pacotes

# Pacotes de terceiro
from bsct.models import BSCTModelMixin
import os

class Sistema(BSCTModelMixin, Model_GetRelatedObject_Mixin,  models.Model):
    def generate_path(instance, filename):
        return os.path.join("logos", instance.logo, filename)    
    
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Somente caracteres alfanuméricos são permitidos.')
    
    created_by = models.ForeignKey(User, editable=False)
    slug = models.SlugField(max_length=50, unique=True, editable=False)
    #nome = models.CharField(max_length=30, verbose_name=u'Título', validators=[alphanumeric])

    logotipo = models.ImageField(upload_to=generate_path ,null=True, blank=True , verbose_name=u'Logotipo', help_text=u'Faça o upload do logotipo da sua empresa ou do seu sistema. Ele será apresentado na barra superior de menus')
    
    nome = models.CharField(max_length=30, verbose_name=u'Título', help_text=u'Título do sistema')
    descricao_curta = models.CharField(max_length=100, verbose_name=u'Subtítulo', help_text=u'Tamanho máximo= 100 caracteres', null=True, blank=True)   
    #descricao_completa = models.TextField((u'Descrição detalhada'), max_length=1000, help_text=u'Tamanho máximo= 1000 caracteres', null=True, blank=True)  

    boas_vindas = models.TextField((u'Boas-vindas'), max_length=1000, null=True, blank=True,\
        help_text=u'Esse texto é apresentado na primeira página, quando o usuário ainda não está logado.<br> \
            Altere o texto padrão e use esse campo para explicar um pouco sobre o seu sistema, e dar boas vindas ao usuário.<br> \
            Utilize tags HTML para formatar o texto. Tamanho máximo = 1000 caracteres.', \
        default = u'Seja bem-vindo ao nosso sistema, cadastre-se para ter acesso. <br>\n\
Você terá controle total sobre as suas informações e poderá criar, editar e excluir os seus conteúdos quando desejar.'\
        )
    
    instrucoes = models.TextField((u'Instruções'), max_length=1000, null=True, blank=True,\
        help_text=u'Esse texto é apresentado quando o usuário se loga no seu sistema.<br> \
            Altere o texto padrão e utilize esse campo para passar instruções de uso do seu sistema, para o seu usuário.<br> \
            Utilize tags HTML para formatar o texto. Tamanho máximo = 1000 caracteres.',
        default = u'Seja bem-vindo ao nosso sistema. <br>\n\
Para navegar, clique nos itens do menu acima.'\
        )  

    template = models.TextField(max_length=20, verbose_name=u'Template', editable=False)    

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(auto_now=True)

    def __unicode__( self ):
        return '%s' % ( self.nome )

    def get_absolute_url(self):
        return reverse('sistema_detail', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = "Sistema"
        verbose_name_plural = "Sistemas"

    def meta(self):
        return self._meta

    # Esse metodo eh chamado no template detail.html
    def get_fields(self):
        # Definir os campos que nao serao mostrados no DetailView
        # Deve ser o atributo name, do field do model
        
        """
        #exclui_campo_da_view = ("id", "created_by" )
        exclui_campo_da_view = '';
        
        list_of_tuples = []
        for field in Sistema._meta.fields:
            if not field.name in exclui_campo_da_view:
                list_of_tuples.append((field.verbose_name, field.value_to_string(self)))
                
        return list_of_tuples
        """
    
    """
    def get_related_objects(self):
         #a[0].model._meta.verbose_name
        #return self._meta.get_all_related_objects()[0].model._meta.verbose_name
        return self._meta.get_all_related_objects()
    """

    def save(self, *args, **kwargs):
        import re
        slug = unicode(self.nome)
        self.slug = slugify(slug)
        self.logo = slugify(slug)
        # Substitui sujeira "-" que eh gerada no unicode e dah pau no nome da app.
        self.slug = re.sub("-", "_", self.slug)
        
        self.slug += '_'+str(self.id)
        super(Sistema, self).save(*args, **kwargs)


class SistemaForm(ModelForm):
    class Meta:
        model = Sistema
        exclude = ('created_by',)
