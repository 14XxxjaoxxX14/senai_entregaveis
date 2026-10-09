# core/admin.py
from django.contrib import admin
from django.contrib.auth.models import User, Group as AuthGroup
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Tarefas, Grupo  


class RedirectToAdminIndexMixin:
    def response_add(self, request, obj, post_url_continue=None):
        if "_addanother" not in request.POST and "_continue" not in request.POST:
            return HttpResponseRedirect(reverse('admin:index'))
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if "_addanother" not in request.POST and "_continue" not in request.POST:
            return HttpResponseRedirect(reverse('admin:index'))
        return super().response_change(request, obj)



admin.site.unregister(AuthGroup)

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(RedirectToAdminIndexMixin, UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
    )


@admin.register(Grupo)
class GrupoAdmin(RedirectToAdminIndexMixin, admin.ModelAdmin):
    list_display = ('nome', 'exibir_membros')
    filter_horizontal = ('membros',)
    fields = ('nome', 'membros')  

    def exibir_membros(self, obj):
        membros = [m.username for m in obj.membros.all()]
        return ", ".join(membros) if membros else "Sem membros"
    
    exibir_membros.short_description = 'Membros do Grupo'


# 4. Configuração de Tarefas
@admin.register(Tarefas)
class TarefaAdmin(RedirectToAdminIndexMixin, admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'grupo', 'concluida', 'criado_em')
    list_filter = ('grupo', 'usuario', 'concluida')
    search_fields = ('titulo', 'descricao')