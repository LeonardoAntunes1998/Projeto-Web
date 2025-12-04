# 📦GOBox - Sistema de Gestão de Encomendas para Condomínios

<h2 id="visao-do-produto">🎯 Visão do Produto</h2>

Para o condomínio Morada do Parque, em Cuiabá--MT, **cujas operações logísticas manuais** da sala de mensagens enfrentam dificuldades com o aumento do volume de encomendas, **o GOBox!** **é um** sistema web de gestão e controle de encomendas, que busca **organizar, agilizar e automatizar** o fluxo de entrada, armazenamento e retirada de objetos pelos moradores. **Diferentemente de** registros manuais e uso de planilhas Excel, **o GOBox!** oferece **registros íntegros, rastreabilidade e notificações automáticas**, garantindo eficiência e transparência.

------------------------------------------------------------------------

## 📑 Sumário


1. [Problemática](#problemática)  
2. [Funcionalidades Principais](#funcionalidades-principais)  
3. [Perfis de Usuário](#perfis-de-usuário)  
4. [Estrutura de Dados](#estrutura-de-dados)  
5. [Documentação](#documentação)
    - Concepção do Produto  
    - Diagrama de Casos de Uso  
    - Stories e Casos de Uso  
    - Diagrama de Classes  
    - Modelos BPMN
6. [Arquitetura do Software](#arquitetura-do-software)  
7. [Tecnologias Utilizadas](#tecnologias-utilizadas)
8. [Instalação Rápida](#instalação-rápida)
9. [Protótipos de Tela](#protótipos-de-tela)
10. [Preparação do Ambiente](#preparação-do-ambiente)
11. [Testes](#testes)
12. [Licença](#licença)
13. [Equipe](#equipe)
14. [Agradecimentos](#agradecimentos)

------------------------------------------------------------------------

<h2 id="problematica">🧩 Problemática</h2>

O sistema surge a partir da realidade observada no **Condomínio Morada do Parque**, onde:

-   Encomendas são separadas apenas por tamanho.
-   Registro só ocorre no momento da retirada.
-   É comum filas de 5 a 8 pessoas, chegando a mais em períodos como Back Friday.
-   O contato é feito via WhatsApp manualmente.
-   Registros são anotados em cadernos.

O GOBox automatiza toda a operação, trazendo eficiência, organização e dados para tomada de decisão.

------------------------------------------------------------------------

<h2 id="funcionalidades-principais">🚀 Funcionalidades Principais</h2>

### **Funcionário**
Responsável pelo atendimento e pelo gerenciamento diário das encomendas do condomínio. Suas principais ações incluem:

- Cadastrar e atualizar moradores  
- Registrar entrada e retirada de encomendas  
- Enviar notificações automáticas aos moradores  
- Consultar relatórios operacionais, como:  
  - Volume de encomendas por torre  
  - Volume por bloco  
  - Volume por apartamento  
  - Volume por morador  
  - Volume total do condomínio  
- Acompanhar o tempo de armazenamento de cada encomenda  

### **Administrador / Síndico**
Usuário com permissões ampliadas, focado na gestão global do sistema. Pode:

- Gerenciar funcionários  
- Configurar torres, blocos e apartamentos  
- Acessar relatórios administrativos sobre a atuação da equipe  

### **Morador**
Usuário final do sistema. Tem acesso às informações destinadas ao seu apartamento e recebe:

- Notificações sobre novas encomendas via WhatsApp

------------------------------------------------------------------------

<h2 id="perfis-de-usuario">👥 Perfis de Usuário</h2>

-   **Administrador:** gestão completa do sistema.
-   **Funcionário:** controla entrada e retirada das encomendas.
-   **Morador:** recebe notificações e retira encomendas.

------------------------------------------------------------------------

<h2 id="documentacao">📘 Documentação</h2>

### Concepção do Produto

Desenvolvido para eliminar gargalos operacionais e trazer transparência à gestão de encomendas do condomínio.

### Diagrama de Casos de Uso

*(Inserir arquivo posteriormente)*

### Stories e Casos de Uso

## 📋 User Stories

| ID     | User Story                                        | Descrição                                                                                                                                                           |
|-------|---------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| US-01  | Registrar nova encomenda                          | Como funcionário, quero registrar a entrada de uma encomenda para manter o controle de todos os objetos recebidos no condomínio.                                   |
| US-02  | Registrar retirada de encomenda                   | Como funcionário, quero registrar a retirada de uma encomenda para garantir que a entrega ao morador fique registrada com integridade e rastreabilidade.           |
| US-03  | Visualizar lista de encomendas                    | Como funcionário, quero visualizar a lista de encomendas cadastradas para facilitar o gerenciamento e a localização das encomendas.                                |
| US-05  | Notificação de chegada de encomenda               | Como funcionário/sistema, quero que o sistema envie uma notificação ao morador informando a chegada de uma nova encomenda.                                         |
| US-07  | Gerenciar acesso de moradores e porteiros         | Como administrador, quero gerenciar o acesso de moradores e funcionários (porteiros) para controlar permissões e níveis de acesso ao sistema.                      |
| US-06  | Notificação de retirada                           | Como morador, quero receber confirmação/notificação quando uma encomenda for retirada em meu nome, para garantir segurança e conferência das entregas.            |
| US-08  | Painel com estatísticas de entregas               | Como administrador, quero visualizar um painel com estatísticas de entregas para analisar o volume de encomendas e apoiar decisões de gestão logística.           |
| US-09  | Acessar log de auditoria das entregas             | Como administrador, quero acessar um log de auditoria das entregas para rastrear ações realizadas pelos funcionários no sistema.                                   |
| US-12  | Configurar regras de trabalho do sistema          | Como administrador, quero configurar regras de trabalho (como prazos de retirada, políticas de notificação, etc.) para adaptar o sistema às necessidades do condomínio. |
| US-04  | Registrar múltiplas encomendas para uma unidade   | Como funcionário, quero registrar múltiplas encomendas para uma mesma unidade/morador de forma rápida para agilizar o cadastro em horários de pico.               |
| US-10  | Enviar lembrete de encomenda pendente             | Como sistema, quero enviar lembretes de encomenda pendente de retirada após determinado tempo para reduzir o acúmulo na sala de mensagens.                        |
| US-11  | Configurar câmera para leitura de códigos         | Como funcionário, quero configurar e utilizar uma câmera para leitura de código das encomendas (ex: código de barras ou QR Code) para agilizar o registro.        |



### Diagrama de Classes

*(Inserir arquivo posteriormente)*

### BPMN -- Fluxo Geral

*(Inserir arquivo posteriormente)*

------------------------------------------------------------------------

<h2 id="arquitetura-do-software">🏗️ Arquitetura do Software</h2>

```text
gobox/
├── blocos/                             # App de blocos, torres e unidades
│   ├── migrations/                     # Histórico de alterações do banco
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── encomendas/                         # App principal de encomendas
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── 0002_initial.py
│   ├── templates/
│   │   └── encomendas/
│   │       ├── dashboard.html
│   │       ├── encomenda_detail.html
│   │       └── encomenda_form.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── gobox/                              # Núcleo do projeto Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── notificacoes/                       # App de notificações aos moradores
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── 0002_initial.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│
```

------------------------------------------------------------------------

<h2 id="tecnologias-utilizadas">🧰 Tecnologias Utilizadas</h2>

### Backend
<p align="center">
  <img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white"/>
  <img src="https://img.shields.io/badge/Express.js-000000?style=for-the-badge&logo=express&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
</p>

### Frontend
<p align="center">
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black"/>
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white"/>
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>
</p>

### DevOps & Ferramentas
<p align="center">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shie



------------------------------------------------------------------------

<h2 id="instalacao-rapida">⚡ Instalação Rápida</h2>

``` bash
git clone https://github.com/ifmt-cba//gobox.git
cd gobox
npm install
npm run dev
```

------------------------------------------------------------------------

<h2 id="prototipos-de-tela">🎨 Protótipos de Tela</h2>

Adicionar arquivos no diretório `/docs/prototipos`.

------------------------------------------------------------------------

<h2 id="preparacao-do-ambiente">🛠️ Preparação do Ambiente</h2>

-   Criar `.env`\
-   Subir containers Docker\
-   Configurar banco\
-   Inserir usuários iniciais

------------------------------------------------------------------------
<h2 id="testes">🧪 Testes</h2>



------------------------------------------------------------------------

<h2 id="licenca">📄 Licença</h2>

Este é um projeto de caráter acadêmico, sem fins comerciais, licenciado apenas para uso educacional.

------------------------------------------------------------------------

<h2 id="equipe">👥 Equipe</h2>
-   Erick Gabriel Santiago de Araujo - Matricula: 2021178440241
-   Felipe Falcieri Macedo - Matricula: 2022178440134
-   Leonardo Jardim Antunes - Matricula: 2021278440308
  
------------------------------------------------------------------------

<h2 id="agradecimentos">🙏 Agradecimentos</h2>

Agradecimentos ao Condomínio Morada do Parque pelo apoio e disponibilização do fluxo real de trabalho, e ao IFMT Campus Cuiabá pelo Suporte institucional.
