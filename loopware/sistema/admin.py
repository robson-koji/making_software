from django.contrib import admin
from sistema.models import Sistema

#http://stackoverflow.com/questions/9563935/removing-buttons-links-in-django-admin
class MyAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super(MyAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
    
admin.site.register(Sistema, MyAdmin)
#admin.site.register(Sistema)
