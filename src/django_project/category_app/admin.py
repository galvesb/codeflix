from django.contrib import admin


from django_project.category_app.models import Category



class CategoryAdmin(admin.ModelAdmin):

    
    list_display = ('id', 'name', 'description', 'is_active')

    list_filter = ('is_active',)

    search_fields = ('name', 'description')
    

    # ação para ativar e desativar
    actions = ['activate', 'deactivate']

    def activate(self, request, queryset):
        queryset.update(is_active=True)

    def deactivate(self, request, queryset):
        queryset.update(is_active=False)

    activate.short_description = 'Ativar categorias selecionadas'
    deactivate.short_description = 'Desativar categorias selecionadas'



admin.site.register(Category, CategoryAdmin)

