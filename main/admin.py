from django.contrib import admin

from main.models import Todo


class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_active']
    


admin.site.register(Todo, TodoAdmin)
