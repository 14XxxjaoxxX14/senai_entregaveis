# core/tests/test_funcionalidade.py
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Tarefas, Grupo

@pytest.mark.django_db
def test_usuario_em_multiplos_grupos_e_tarefas():
    # 1. Cria os usuários
    joao = User.objects.create_user(username='joao', password='123')
    maria = User.objects.create_user(username='maria', password='123')
    pedro = User.objects.create_user(username='pedro', password='123')


    grupo_backend = Grupo.objects.create(nome='Equipe Backend')
    grupo_backend.membros.add(joao, maria)

    grupo_frontend = Grupo.objects.create(nome='Equipe Frontend')
    grupo_frontend.membros.add(joao, pedro)  

    
    tarefa1 = Tarefas.objects.create(
        titulo='Modelagem MySQL',
        descricao='Criar tabelas no banco',
        usuario=joao,
        grupo=grupo_backend
    )

    tarefa2 = Tarefas.objects.create(
        titulo='Estilização CSS',
        descricao='Criar layout responsivo',
        usuario=joao,
        grupo=grupo_frontend
    )

    # Asserções de validação
    assert joao.grupos_pertencentes.count() == 2  
    assert tarefa1.grupo.nome == 'Equipe Backend'
    assert tarefa2.grupo.nome == 'Equipe Frontend'
    assert tarefa1.usuario == tarefa2.usuario == joao


@pytest.mark.django_db
def test_exibicao_membros_na_view(client):
    aluno1 = User.objects.create_user(username='aluno1', password='senha123')
    grupo = Grupo.objects.create(nome='Grupo Teste')
    grupo.membros.add(aluno1)

    Tarefas.objects.create(
        titulo='Tarefa Teste',
        descricao='Descrição da Tarefa',
        grupo=grupo
    )

    url = reverse('index')
    response = client.get(url)

    assert response.status_code == 200
    assert 'Grupo Teste' in response.content.decode('utf-8')
    assert 'aluno1' in response.content.decode('utf-8')
