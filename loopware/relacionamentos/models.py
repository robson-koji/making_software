# -*- coding: utf-8 -*-

from django.db import models

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm
from myMixins.mixins import Model_GetRelatedObject_Mixin
from django.core.validators import MinValueValidator, MaxValueValidator

from bsct.models import BSCTModelMixin
from elemento.models import Elemento
from sistema.models import Sistema

class relacionamentos(BSCTModelMixin, Model_GetRelatedObject_Mixin, models.Model):
    created_by = models.ForeignKey(User, related_name='+', verbose_name=u'Criado por', editable=False, )
    sistema = models.ForeignKey(Sistema, related_name='+', verbose_name=u'Sistema', editable=False)

    elemento = models.ForeignKey(Elemento, null=True, blank=True, related_name='+', verbose_name=u'Sessão 1', \
                                 help_text=u'Deixe esse campo em branco caso você esteja definindo uma relação entre o próprio usuário\
                                 e a sessão 2')

    CHOICES_tipo_relacionamento = (
        ('1', 'Um -> Um'),
        ('2', 'Muitos -> Um'),
        ('3', 'Muitos -> Muitos'),
    )

    tipo_relacionamento = models.CharField(max_length=50, choices=CHOICES_tipo_relacionamento, verbose_name=u'Tipo do relacionamento', help_text=u'')

    relates_to = models.ForeignKey(Elemento, to_field='slug', verbose_name=u'Sessão 2')
    
    obrigatorio = models.BooleanField(default=True, verbose_name=u'Obrigatório', help_text=u'Se o relacionamento for opcional, desmarque esse campo.')

    def get_absolute_url(self):
        return reverse('relacionamentos_detail', kwargs={'pk': self.pk})
 
    class Meta:
        verbose_name = "Relacionamento"
        verbose_name_plural = "Relacionamentos"
 
    def meta(self):
        return self._meta
 
    # Esse metodo eh chamado no template detail.html
    def get_fields(self):
        # Definir os campos que nao serao mostrados no DetailView
        # Deve ser o atributo name, do field do model
        exclui_campo_da_view = ("created_by")

        list_of_tuples = []
        for field in relacionamentos._meta.fields:
            if not field.name in exclui_campo_da_view:
                list_of_tuples.append((field.verbose_name, field.value_to_string(self)))

        return list_of_tuples
 
    # Esse metodo eh chamado no list.html. Ele retorna todos os campos
    def get_fields_and_values(self):
        return [(field, field.value_to_string(self)) for field in relacionamentos._meta.fields]

    def __unicode__( self ):
        return '%s' % ( self.tipo_relacionamento )
