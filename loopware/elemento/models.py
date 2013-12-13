# -*- coding: utf-8 -*- 

# Django modules
from django.template.defaultfilters import slugify
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models

# My modules
from myMixins.mixins import Model_GetRelatedObject_Mixin
from extend_models import ExtendModels
from sistema.models import Sistema

# 3rd part modules
from bsct.models import BSCTModelMixin
   
   
class Elemento(ExtendModels, BSCTModelMixin, Model_GetRelatedObject_Mixin, models.Model):
    created_by = models.ForeignKey(User, editable=False)
    slug = models.SlugField(max_length=50, unique=True, editable=False)
    sistema = models.ForeignKey(Sistema, editable=False)
    nome = models.CharField(max_length=30, verbose_name=u'Título', help_text=u'Título da sessão')
    descricao_curta = models.CharField(max_length=100, verbose_name=u'Subtítulo da sessão', help_text=u'Tamanho máximo= 100 caracteres', null=True, blank=True)  
    descricao_completa = models.TextField((u'Descrição detalhada'), max_length=1000, help_text=u'Tamanho máximo= 1000 caracteres', null=True, blank=True)  

    def __unicode__( self ):
        return '%s' % ( self.nome )

    def get_absolute_url(self):
        return reverse('elemento_detail', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = "Sessão"
        verbose_name_plural = "Sessões"

    def meta(self):
        return self._meta

    # Esse metodo eh chamado no template detail.html
    def get_fields(self):
        # Definir os campos que nao serao mostrados no DetailView
        # Deve ser o atributo name, do field do model
        exclui_campo_da_view = ("id", "created_by", "nome", "sistema")

        list_of_tuples = []
        for field in Elemento._meta.fields:
            if not field.name in exclui_campo_da_view:
                list_of_tuples.append((field.verbose_name, field.value_to_string(self)))
                
        return list_of_tuples

    def save(self, *args, **kwargs):
        import re
        slug = unicode(self.nome)
        self.slug = slugify(slug)

        # Substitui sujeira "-" que eh gerada no unicode e dah pau no nome da app.
        self.slug = re.sub("-", "_", self.slug)
        
        self.slug += '_'+str(self.id)
        super(Elemento, self).save(*args, **kwargs)
        
    """
    def get_related_objects(self):
         #a[0].model._meta.verbose_name
        #return self._meta.get_all_related_objects()[0].model._meta.verbose_name
        return self._meta.get_all_related_objects()
    """

class ElementoForm(ModelForm):
    class Meta:
        model = Elemento
        #exclude = ('created_by', 'sistema')
