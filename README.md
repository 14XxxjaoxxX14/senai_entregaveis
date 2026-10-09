# 🛠️ SENAI Entregáveis — Painel de Administração Customizado

Este projeto é uma aplicação web desenvolvida em **Django** e **MySQL**, focada na gestão de tarefas e equipes. O objetivo principal foi reestruturar e estilizar integralmente a interface nativa do **Django Admin** para atender à identidade visual do **SENAI** (paleta azul `#0056b3` e branco), garantindo alta usabilidade, ocultação de permissões sensíveis do sistema e automação de testes com integração contínua.

---

## 🚀 Funcionalidades Principais

* **Identidade Visual SENAI**: Sobrescrita completa do CSS do Django Admin com suporte a temas claros e escuros com alto contraste.
* **Simplificação do Admin**: Remoção da interface nativa de permissões complexas e exibição simplificada dos cadastros de **Usuários**, **Grupos** e **Tarefas**.
* **Fluxo de Trabalho Otimizado**: Redirecionamento automático (`RedirectToAdminIndexMixin`) para a página inicial do painel ao salvar/editar registros.
* **Banco de Dados Relacional**: Modelagem de dados com integrações `ForeignKey` e `ManyToManyField` entre Usuários, Grupos e Tarefas.
* **Qualidade e Testes Automatizados**: Suíte de testes automatizados com `pytest` e cobertura de modelos, views e customizações do Admin.
* **Integração Contínua (CI)**: GitHub Actions configurado para executar o `pytest` automaticamente a cada novo `push` ou `pull request`.

---

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:

* [Python 3.11+](https://www.python.org/)
* [MySQL Server 8.0+](https://dev.mysql.com/downloads/installer/)
* [Git](https://git-scm.com/)

---

## 🗄️ Configuração do Banco de Dados (MySQL)

O projeto está configurado no arquivo `meusegundoprojeto/settings.py` para conectar ao MySQL local com os seguintes dados:

* **Banco de Dados**: `senai_entregaveis`
* **Usuário**: `root`
* **Senha**: `1811`
* **Host**: `127.0.0.1` | **Porta**: `3306`

### Como Restaurar o Banco de Dados

Um *dump* completo com a estrutura e os dados de teste está incluído na raiz do projeto como **`banco_senai.sql`**.

#### Pelo MySQL Workbench:
1. Abra o **MySQL Workbench** e conecte-se à sua instância local.
2. Vá em **Server** > **Data Import**.
3. Selecione **Import from Self-Contained File** e busque o arquivo `banco_senai.sql`.
4. Clique em **Start Import**.

#### Pelo Terminal / Prompt de Comando:
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS senai_entregaveis;"
mysql -u root -p senai_entregaveis < banco_senai.sql
