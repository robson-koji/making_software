# -*- coding: utf-8 -*-

from django.db import models

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.forms import ModelForm
from myMixins.mixins import Model_GetRelatedObject_Mixin
from django.core.validators import MinValueValidator, MaxValueValidator


# Pacotes de terceiro
from bsct.models import BSCTModelMixin


# Cria classe M2M qdo o campo eh MultipleChoiceField
[% FOREACH field_id = models.fields.keys.nsort %]
    [% IF models.fields.$field_id.type == "MultipleChoiceField" %]
    [% choices_text = models.fields.$field_id.slug %]
class Choices_[% models.fields.$field_id.slug %]( models.Model ):
    choice_desc = models.CharField(max_length=300)

    def __unicode__(self):
        return self.choice_desc
    [% END %]
[% END %]  


class [% models.slug %](BSCTModelMixin, Model_GetRelatedObject_Mixin, models.Model):
    [% created_by = "" %]    
    [% IF models.qt_elementos == '1' %]
        # Essa chave eh definida para o ForeignKey created_by.
        # Caso o elemento seja filho direto do usuario e tenha somente um elemento
        # (OneToOne, ou nesse caso ForeignKey com Unique=True)
        [% created_by = "unique=True," %]    
    [% END %]    

    [% IF models.elemento.eh_usuario %]
    created_by = models.OneToOneField(User, related_name='[% models.slug %]_created_by_set', verbose_name=u'Criado por', editable=False)
    [% ELSE %]        
    created_by = models.ForeignKey(User, [% created_by %] related_name='[% models.slug %]_created_by_set', verbose_name=u'Criado por', editable=False)
    [% END %]    
   

    [% FOREACH field_id = models.fields.keys.nsort %]
    [% max_length = "" %]
    [% choices = "" %]
    [% upload_to = "" %]
    [% required = "" %]
    [% max_min_validator = "" %]
    [% default = "" %]
    
    
    [% UNLESS models.fields.$field_id.required == 1 %]
        [% required = "null=True, blank=True , "%]
    [% END %]    
    
    [% IF models.fields.$field_id.type == "BooleanField" %]
    # Precisa ficar abaixo da definicao do required, pq ele sobreescreve
        [% default = "default=False , " %]
        [% required = ""%]        
    [% END %]
    
    [% IF models.fields.$field_id.type == "FileField" %]
        [% upload_to = "upload_to='$models.slug' ," %]
    [% END %]    
    
    [% IF models.fields.$field_id.type == "ImageField" %]
        [% upload_to = "upload_to='$models.slug' ," %]
    [% END %]    
    
    [% IF models.fields.$field_id.widget == "Textarea" %]
       [% models.fields.$field_id.type = "TextField" %]
       [% max_length = "max_length=5000, " %]
    [% END %]
    
    [% IF models.fields.$field_id.type == "CharField" %]
       [% max_length = "max_length=100, " %]
    [% END %]

    [% IF models.fields.$field_id.type == "IntegerField" %]
        [% max_min_validator = "validators=[MinValueValidator(1), MaxValueValidator(999999999)] , " %]    
    [% END %]


    [% IF models.fields.$field_id.type == "ChoiceField" %]
        #http://stackoverflow.com/questions/5776333/django-choices-for-models
        # there can be only one selection
       [% models.fields.$field_id.type = 'CharField' %]
       [% max_length = "max_length=50, " %]
       [% form_id = models.form_id %]
       [% choices_text = models.fields.$field_id.slug %]
       [% choices = "choices=CHOICES_$choices_text, " %]
    CHOICES_[% models.fields.$field_id.slug %] = (    
        [% FOREACH choice_id = models.fields.$field_id.choices.keys.nsort %]
        ('[% models.fields.$field_id.choices.$choice_id.slug %]', '[% models.fields.$field_id.choices.$choice_id.label %]'),
        [% END %]
    )
    [% END %]

    [% IF models.fields.$field_id.type == "MultipleChoiceField" %]
        # Usa isso para criar e popular o M2M MultipleChoiceField
        #https://docs.djangoproject.com/en/dev/howto/initial-data/
        [% models.fields.$field_id.type = "ManyToManyField" %]
        [% choices_text = models.fields.$field_id.slug %]
        [% choices = "Choices_$choices_text, " %]

        # Mostra na listView o campo que eh unicode.
        # Se tiver mais de um, mostra o primeiro da lista. O problema eh que o usuario pode ordenar os campos do form,
        # entao precisa pegar o primeiro na ordenacao, e nao na ordem de insercao.
        # Colocando aqui no if para nao ficar imprimindo no loop
    [% END %]
    
    [% IF models.fields.$field_id.type == "CharField" || models.fields.$field_id.type == "DateTimeField" || models.fields.$field_id.type == "BooleanField"
     || models.fields.$field_id.type == "ChoiceField" || models.fields.$field_id.type == "FileField" || models.fields.$field_id.type == "ImageField" %]
    
    def __unicode__( self ):
        return '%s' % ( self.[% models.fields.$field_id.slug %] )
    [% END %]
     
    [% models.fields.$field_id.slug %] = models.[% models.fields.$field_id.type %]([% max_length %][% upload_to %][% choices %][% required %][% max_min_validator %][% default %]verbose_name=u'[% models.fields.$field_id.label %]', help_text=u'[% models.fields.$field_id.help_text %]')
    [% END %]
 

    [% FOREACH relacionamento IN models.relacionamentos %] 
    [% UNLESS relacionamento.relates_to_id == "User" %]

    [% IF relacionamento.obrigatorio == 1 %]
        [% required = ""%]
    [% ELSE %]    
        [% required = "null=True, blank=True , "%]
    [% END %]    

    [% IF relacionamento.tipo_relacionamento == 1 %]
    # Relacionamentos 1to1, 1tom m2m
    from [% relacionamento.relates_to_id %].models import [% relacionamento.relates_to_id %] # Se for User, nao precisa importar
    [% relacionamento.relates_to_id %]_field = models.OneToOneField([%relacionamento.relates_to_id %],verbose_name=u'[% relacionamento.related_slug %]',[% required %])
    [% ELSIF relacionamento.tipo_relacionamento == 2 %]
    from [% relacionamento.relates_to_id %].models import [% relacionamento.relates_to_id %] # Se for User, nao precisa importar    
    [% relacionamento.relates_to_id %]_field = models.ForeignKey([% relacionamento.relates_to_id %], verbose_name=u'[% relacionamento.related_slug %]',[% required %])
    [% ELSIF relacionamento.tipo_relacionamento == 3 %]
    from [% relacionamento.relates_to_id %].models import [% relacionamento.relates_to_id %] # Se for User, nao precisa importar    
    [% relacionamento.relates_to_id %]_field = models.ManyToManyField([% relacionamento.relates_to_id %], verbose_name=u'[% relacionamento.related_slug %]',[% required %])
    
    def [% relacionamento.relates_to_id %]_m2m_reverso(self):
        # Ao inves do id, precisa pegar o campo que mais convem, que eh o primeiro unicode field.
        # Eh muito foda pegar esse campo.
        # http://stackoverflow.com/questions/6611986/whats-the-difference-between-queryset-tuple-dictionary-in-django-template
        # Estah pegando o terceiro elemento (indice numero dois pq considera que o 0=id e 1=created_by e o proximo eh algum que
        # tenha unicode.
        return "\n".join([a[2] for a in self.[% relacionamento.relates_to_id %]_field.values_list()])
        #return ', '.join([a.id for a in self.[% relacionamento.relates_to_id %]_field.all()])
    [% relacionamento.relates_to_id %]_m2m_reverso.short_description = "[% relacionamento.related_slug %]"
    [% END %]
    [% END %] 
    [% END %]

    [% IF models.validade %]
    validade_check = models.BooleanField(default=False , verbose_name=u'Válido', help_text=u'O usuário poderá criar somente objetos válidos (checados).<br>\
                                         Porém ele sempre poderá listar todos os objetos e ver os seus respectivos detalhes. <br>\
                                         Se não quiser mais listar algum objeto, você deverá excluí-lo definitivamente.')
    [% END %]

    [% IF models.elemento.grupo %]
    grupo_[% models.slug %] = models.ForeignKey(Group, verbose_name=u'[% models.elemento.grupo %]')
    [% END %] 
    
    def get_absolute_url(self):
        return reverse('[% models.slug %]_detail', kwargs={'pk': self.pk})
 
    class Meta:
        verbose_name = "[% models.app_nickname %]"
        verbose_name_plural = "[% models.app_nickname %]"
        permissions = (
            ('view_[% models.slug %]', 'View [% models.app_nickname %]'),
            ('list_[% models.slug %]', 'List [% models.app_nickname %]'),
        )
 
    def meta(self):
        return self._meta

 
    # Esse metodo eh chamado nos templates detail.html e list.html
    def get_fields(self):
        # Definir os campos que nao serao mostrados no DetailView
        # Deve ser o atributo name, do field do model
        exclui_campo_da_view = ("created_by")

        list_of_tuples = []
        for field in [% models.slug %]._meta.fields:
            if not field.name in exclui_campo_da_view:
                # Esse nao consegue retornar o valor de FK
                #list_of_tuples.append((field.verbose_name, field.value_to_string(self)))
                list_of_tuples.append((field.verbose_name, getattr(self, field.name)))
        
        # Captura os valores dos campos relacionados m2m.
        #http://stackoverflow.com/questions/8474013/loop-in-manytomany-fields-in-django-model
        for field in [% models.slug %]._meta.many_to_many:
                if not field.name in exclui_campo_da_view:
                    m2m_field = getattr(self, field.name)   
                    concatenados = ', '.join([str(i) for i in m2m_field.all()])
                    list_of_tuples.append((field.verbose_name, concatenados))

        return list_of_tuples   