from django.contrib import admin
from relacionamentos.models import relacionamentos
class relacionamentos_Admin(admin.ModelAdmin):
    list_display = ["id", "created_by", "get_tipo_relacionamento_display", ]
    
    def get_actions(self, request):
        actions = super(relacionamentos_Admin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
    
    pass
admin.site.register(relacionamentos, relacionamentos_Admin)
from allauth.account.models import *
#admin.site.unregister(EmailAddress)
#admin.site.unregister(EmailConfirmation)

from allauth.socialaccount.models import *
#admin.site.unregister(SocialApp)
#admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)

from django.contrib.sites.models import Site
admin.site.unregister(Site)

from django.contrib.auth.models import * 
#admin.site.unregister(User)
#admin.site.unregister(Group)


