import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from core.models import Grupo, Tarefas
from core.admin import GrupoAdmin, CustomUserAdmin

@pytest.mark.django_db
class TestModelos:

    def test_criar_grupo_e_representacao_str(self):
        """Testa a criação de um Grupo e o método __str__."""
        grupo = Grupo.objects.create(nome="Equipe de Automação")
        assert str(grupo) == "Equipe de Automação"
        assert grupo.membros.count() == 0

    def test_adicionar_membros_ao_grupo(self):
        """Testa a associação de utilizadores (membros) a um Grupo."""
        grupo = Grupo.objects.create(nome="Desenvolvimento")
        usuario1 = User.objects.create_user(username="marcos", password="123")
        usuario2 = User.objects.create_user(username="julia", password="123")

        grupo.membros.add(usuario1, usuario2)

        assert grupo.membros.count() == 2
        assert usuario1 in grupo.membros.all()
        assert usuario2 in grupo.membros.all()

    def test_criar_tarefa_sem_usuario_e_str(self):
        """Testa a criação de uma Tarefa sem utilizador atribuído."""
        tarefa = Tarefas.objects.create(
            titulo="Manutenção Preventiva",
            descricao="Verificar painel elétrico"
        )
        assert str(tarefa) == "Manutenção Preventiva - Sem usuário"
        assert tarefa.concluida is False
        assert tarefa.usuario is None
        assert tarefa.grupo is None

    def test_criar_tarefa_com_usuario_e_grupo(self):
        """Testa o relacionamento de Tarefa com Utilizador e Grupo."""
        usuario = User.objects.create_user(username="carlos", password="123")
        grupo = Grupo.objects.create(nome="Elétrica")
        
        tarefa = Tarefas.objects.create(
            titulo="Troca de Disjuntor",
            usuario=usuario,
            grupo=grupo,
            concluida=True
        )

        assert str(tarefa) == "Troca de Disjuntor - carlos"
        assert tarefa.usuario == usuario
        assert tarefa.grupo == grupo
        assert tarefa.concluida is True



@pytest.mark.django_db
class TestViews:

    def test_pagina_inicial_status_code_e_template(self, client):
        """Testa se a rota principal responde com status 200 e usa o template correto."""
        url = reverse('index')
        response = client.get(url)
        assert response.status_code == 200
        assert 'core/index.html' in [template.name for template in response.templates]

    def test_pagina_inicial_listagem_de_tarefas(self, client):
        """Testa se as tarefas salvas no banco são enviadas no contexto da view."""
        Tarefas.objects.create(titulo="Tarefa A")
        Tarefas.objects.create(titulo="Tarefa B")

        url = reverse('index')
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.context['tarefas']) == 2


# ==============================================================================
# 3. TESTES DE CUSTOMIZAÇÃO DO DJANGO ADMIN
# ==============================================================================
@pytest.mark.django_db
class TestAdminCustomizacoes:

    def test_grupo_admin_metodo_exibir_membros(self):
        """Testa a formatação dos membros exibida na listagem do Admin."""
        grupo = Grupo.objects.create(nome="Robótica")
        site = AdminSite()
        grupo_admin = GrupoAdmin(Grupo, site)

        # Caso 1: Sem membros
        assert grupo_admin.exibir_membros(grupo) == "Sem membros"

        # Caso 2: Com membros
        u1 = User.objects.create_user(username="ana", password="123")
        u2 = User.objects.create_user(username="pedro", password="123")
        grupo.membros.add(u1, u2)

        resultado = grupo_admin.exibir_membros(grupo)
        assert "ana" in resultado
        assert "pedro" in resultado

    def test_custom_user_admin_remocao_de_permissoes(self):
        """Garante que a seção de Permissões foi removida do CustomUserAdmin."""
        site = AdminSite()
        user_admin = CustomUserAdmin(User, site)

        # Extrai os nomes das seções (fieldsets)
        titulos_fieldsets = [f[0] for f in user_admin.fieldsets if f[0] is not None]

        assert "Permissões" not in titulos_fieldsets
        assert "Permissions" not in titulos_fieldsets

    def test_redirecionamento_apos_salvar_no_admin(self, admin_client):
        """Testa se o Mixin redireciona para /admin/ ao criar um novo grupo."""
        url = reverse('admin:core_grupo_add')
        dados_formulario = {'nome': 'Grupo Teste Redirecionamento'}

        response = admin_client.post(url, dados_formulario)

        # Status HTTP 302 indica redirecionamento com sucesso
        assert response.status_code == 302
        assert response.url == reverse('admin:index')