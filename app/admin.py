from django.contrib import admin
from .models import CustomUser, Organization


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone')
    filter_horizontal = ('organizations',)


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Organization)
