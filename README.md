🚗 Locadora SpeedCar - Sistema de Locação de Veículos
📋 Sobre o Projeto
Locadora SpeedCar é um sistema web desenvolvido como trabalho acadêmico para a disciplina de Programação Web do curso de Engenharia da Computação. O projeto consiste em uma aplicação completa para gerenciamento de locação de veículos, implementada utilizando o framework Django.

🎯 Objetivos Acadêmicos
Desenvolver habilidades em desenvolvimento web full-stack

Aplicar conceitos de arquitetura MVC (Model-View-Controller)

Implementar interface responsiva com Bootstrap

Gerenciar versionamento com Git

Praticar deploy de aplicações web

🛠️ Tecnologias Utilizadas
Backend
Python 3.x - Linguagem de programação

Django 4.x - Framework web

SQLite - Banco de dados (desenvolvimento)

Frontend
HTML5 - Estrutura

CSS3 - Estilização

Bootstrap 5 - Framework CSS

JavaScript - Interatividade

Font Awesome - Ícones

Ferramentas de Desenvolvimento
Git - Controle de versão

GitHub Codespaces - Ambiente de desenvolvimento

VS Code - Editor de código

📁 Estrutura do Projeto
text
locadora/
├── 📁 locadora/                 # Configurações do projeto
│   ├── settings.py             # Configurações da aplicação
│   ├── urls.py                 # URLs principais
│   └── ...
├── 📁 meu_app/                 # Aplicação principal
│   ├── models.py              # Modelos de dados
│   ├── views.py               # Lógica das views
│   ├── urls.py                # URLs da aplicação
│   └── ...
├── 📁 templates/              # Templates HTML
│   ├── base.html             # Template base
│   ├── home.html             # Página inicial
│   └── includes/
│       └── navbar.html       # Componente navbar
├── 📁 static/                # Arquivos estáticos
│   ├── css/
│   │   └── style.css        # Estilos personalizados
│   ├── js/
│   │   └── script.js        # JavaScript customizado
│   └── images/              # Imagens do projeto
├── 📁 media/                # Uploads de usuários
├── manage.py               # Script de gerenciamento
└── requirements.txt        # Dependências do projeto
🚀 Funcionalidades Implementadas
✅ Concluídas
Layout Responsivo com Bootstrap 5

Navbar com menu de navegação

Página Inicial com seções:

Hero section com call-to-action

Carros em destaque

Estatísticas da locadora

Processo de locação (como funciona)

Seção de promoções

Sistema de Templates Django

Arquivos Estáticos organizados (CSS, JS, Images)

Design System com cores temáticas (azul/laranja)

🔄 Em Desenvolvimento
Sistema de autenticação de usuários

Catálogo completo de veículos

Sistema de reservas online

Painel administrativo

Integração com pagamento

⚙️ Configuração e Instalação
Pré-requisitos
Python 3.8+

pip (gerenciador de pacotes Python)

Git

Passos para Executar
Clone o repositório

bash
git clone https://github.com/seu-usuario/locadora-speedcar.git
cd locadora-speedcar
Crie um ambiente virtual

bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
Instale as dependências

bash
pip install -r requirements.txt
Execute as migrações

bash
python manage.py migrate
Crie um superusuário

bash
python manage.py createsuperuser
Execute o servidor

bash
python manage.py runserver
Acesse a aplicação

text
http://localhost:8000
🎨 Design e Interface
Paleta de Cores
Primary: #1e40af (Azul principal)

Secondary: #3b82f6 (Azul secundário)

Accent: #fbbf24 (Laranja/destaque)

Background: #f8fafc (Cinza claro)

Componentes
Navbar fixo com logo e menu de navegação

Cards para exibição de veículos

Botões com efeitos hover e gradientes

Seções com espaçamento consistente

📚 Aprendizados Acadêmicos
Este projeto permitiu o desenvolvimento das seguintes competências:

Habilidades Técnicas
Desenvolvimento full-stack com Django

Criação de interfaces responsivas

Gerenciamento de arquivos estáticos

Versionamento com Git

Estruturação de projetos web

Conceitos Aplicados
Padrão MVC/MVT

Templates e herança em Django

Roteamento de URLs

Organização de projetos escaláveis

Deploy e configuração de ambientes

📄 Licença
Este projeto foi desenvolvido para fins acadêmicos como parte da disciplina de Programação Web do curso de Engenharia da Computação.

