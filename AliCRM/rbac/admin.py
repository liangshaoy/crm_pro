from django.contrib import admin
from rbac import models


# Register your models here.

class UserinfoAdmin(admin.ModelAdmin):
    list_display = ["pk", "username", ]
    list_editable = ["username", ]


admin.site.register(models.UserInfo, UserinfoAdmin)


class RoleAdmin(admin.ModelAdmin):
    list_display = ["pk", "title"]
    list_editable = ["title"]


admin.site.register(models.Role, RoleAdmin)



class PermissionAdmin(admin.ModelAdmin):
    ordering = ('-parent',)
    list_filter = ('name',)
    list_display = ['id', 'name', 'url', 'icon', 'parent', 'show', 'priority']
    fields = ['name', 'url', 'icon', 'parent', 'show', 'priority']
    list_editable = ['name', 'url', 'icon', 'parent', 'show', 'priority']


admin.site.register(models.Permission, PermissionAdmin)
