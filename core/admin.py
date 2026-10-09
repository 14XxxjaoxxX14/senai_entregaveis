# core/admin.py
from django.contrib import admin
from django.contrib.auth.models import User, Group as AuthGroup
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Tarefas, Grupo  # Se no seu models.py estiver 'Tarefas', altere para Tarefas


class RedirectToAdminIndexMixin:
    def response_add(self, request, obj, post_url_continue=None):
        if "_addanother" not in request.POST and "_continue" not in request.POST:
            return HttpResponseRedirect(reverse('admin:index'))
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if "_addanother" not in request.POST and "_continue" not in request.POST:
            return HttpResponseRedirect(reverse('admin:index'))
        return super().response_change(request, obj)


# 1. Remover o Grupo nativo do Django (evita caixas de permissões do sistema)
admin.site.unregister(AuthGroup)

# 2. Reconfigurar Usuários sem a aba de Permissões
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(RedirectToAdminIndexMixin, UserAdmin):
    # Restringe a exibição apenas a dados básicos e pessoais (sem permissões)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
    )


# 3. Reconfigurar Grupos (exibe apenas Nome e seleção de Membros)
@admin.register(Grupo)
class GrupoAdmin(RedirectToAdminIndexMixin, admin.ModelAdmin):
    list_display = ('nome', 'exibir_membros')
    filter_horizontal = ('membros',)
    fields = ('nome', 'membros')  # Garante que não haverá caixa de permissões

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