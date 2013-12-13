from django.contrib import admin
from [% admin.slug %].models import [% admin.slug %]


class [% admin.slug %]_Admin(admin.ModelAdmin):
    list_display = [[% admin.fields %]]
    
    def get_actions(self, request):
        actions = super([% admin.slug %]_Admin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()


admin.site.register([% admin.slug %], [% admin.slug %]_Admin)

[% IF admin.idx == '0' %]
from allauth.account.models import *
#admin.site.unregister(EmailAddress)
#admin.site.unregister(EmailConfirmation)

from allauth.socialaccount.models import *
#admin.site.unregister(SocialApp)
#admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)

from django.contrib.sites.models import Site
#admin.site.unregister(Site)

from django.contrib.auth.models import * 
#admin.site.unregister(User)
#admin.site.unregister(Group)

from django.contrib.flatpages.models import *
#admin.site.unregister(FlatPage)

[% END %]
