# GymAccess

Sistema de controle de acesso para academias desenvolvido com Django.

O GymAccess permite o cadastro de alunos, gerenciamento de pacotes de acesso, geração de QR Codes individuais e validação das entradas de forma simples e organizada.

---

## Funcionalidades

- Cadastro de alunos
- Edição e exclusão de alunos
- Cadastro de pacotes de acesso
- Controle de acessos restantes
- Geração de QR Code para acesso
- Validação de QR Code
- Bloqueio de QR Code já utilizado
- Histórico de acessos
- Dashboard com informações do sistema

---

## Tecnologias Utilizadas

- Python 3
- Django 6
- SQLite
- Bootstrap 5
- HTML5
- CSS3
- JavaScript
- Pillow
- QRCode

---

## Estrutura do Projeto

```
GymAccess/
│
├── alunos/
├── config/
├── media/
├── static/
├── templates/
├── manage.py
├── requirements.txt
└── README.md
```

---

## Instalação

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd GymAccess
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual.

Windows:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute as migrações:

```bash
python manage.py migrate
```

Inicie o servidor:

```bash
python manage.py runserver
```

Abra no navegador:

```
http://127.0.0.1:8000/
```

---

## Objetivo

Este projeto foi desenvolvido para fins de estudo e construção de portfólio, simulando um sistema de controle de acesso para academias utilizando QR Code.

---

## Melhorias Futuras

- Login de administradores
- Diferentes níveis de acesso
- Relatórios em PDF
- Painel financeiro
- API REST
- Integração com catracas físicas

---

## Autor

João Paulo Peixoto Bezerra

LinkedIn:
https://www.linkedin.com/in/jo%C3%A3o-paulo-peixoto-dev/

GitHub:
https://github.com/JUAOPAULLO