# AGV Prompt: OrchestratorHelper v3.5 (Granularidade Máxima)

**Tarefa Principal:** Analisar o `@Blueprint_Arquitetural.md`, que é a fonte única da verdade sobre a arquitetura. Suas responsabilidades são: (1) Derivar uma ordem de implementação lógica e (2) Gerar cenários chave para os Testes de Integração.

**Input Principal (Blueprint Arquitetural):**

## --- Conteúdo do Blueprint Arquitetural ---

# **Blueprint Arquitetural: IABANK v1.0.0**

Este documento define a arquitetura técnica e de produto para o `IABANK`, um sistema de gestão de empréstimos SaaS. Ele serve como a fonte única da verdade (SSOT) para o desenvolvimento do sistema, garantindo consistência, manutenibilidade e escalabilidade.

---

## 1. Visão Geral da Arquitetura

A arquitetura escolhida para o `IABANK` é um **Monólito Modular com uma API bem definida**, também conhecido como "Majestic Monolith". O frontend será uma **Single-Page Application (SPA)** completamente desacoplada.

**Justificativa:**

- **Coesão e Simplicidade Inicial:** Para um produto complexo como um sistema de gestão de empréstimos, manter a lógica de negócio principal em um único codebase (Django) no início do projeto reduz drasticamente a complexidade operacional (deploy, monitoramento, transações distribuídas) em comparação com uma abordagem de microsserviços.
- **Performance:** A comunicação intra-processo dentro do monólito é significativamente mais rápida do que chamadas de rede entre microsserviços, o que é crucial para as operações financeiras e relatórios.
- **Preparado para o Futuro:** A arquitetura é projetada em módulos lógicos (Operacional, Financeiro, etc.) que seguem o princípio de alta coesão e baixo acoplamento. Isso significa que, no futuro, se um módulo como "Análise de Risco com IA" se tornar suficientemente complexo, ele poderá ser extraído como um microsserviço separado com um esforço de refatoração mínimo.

**Estratégia de Organização do Código-Fonte:**

Será utilizado um **Monorepo**.

- **Justificativa:** Um monorepo (contendo o backend Django e o frontend React no mesmo repositório Git) simplifica a gestão de dependências, facilita a execução de mudanças atômicas que afetam tanto a API quanto a UI, e unifica o processo de CI/CD. Isso é ideal para a equipe de desenvolvimento inicial, garantindo que o contrato da API e seu consumidor (o frontend) evoluam em sincronia.

---

## 2. Diagramas da Arquitetura (Modelo C4)

### 2.1. Nível 1: Diagrama de Contexto do Sistema (C1)

Este diagrama mostra o `IABANK` em seu ambiente, interagindo com usuários e sistemas externos.

```mermaid
graph TD
    style Gestor fill:#1f77b4,stroke:#000,stroke-width:2px,color:#fff
    style Consultor fill:#ff7f0e,stroke:#000,stroke-width:2px,color:#fff
    style ClienteFinal fill:#2ca02c,stroke:#000,stroke-width:2px,color:#fff
    style IABANK fill:#d62728,stroke:#000,stroke-width:2px,color:#fff

    subgraph "Ecossistema IABANK"
        IABANK[Sistema IABANK]
    end

    Gestor(👤 Gestor / Administrador) -- "Gerencia o sistema via" --> IABANK
    Consultor(👤 Consultor / Cobrador) -- "Executa operações via" --> IABANK
    ClienteFinal(👤 Cliente Final) -- "Futuro: Originação Self-Service via" --> IABANK

    IABANK -- "Consulta dados para análise de risco via API" --> Bureaus[🏦 Bureaus de Crédito]
    IABANK -- "Processa pagamentos e transferências via API" --> Banking[💳 Plataforma Bancária (Pix, Open Finance)]
    IABANK -- "Envia notificações e interage via Chatbot" --> Comms[📱 Sistemas de Comunicação (WhatsApp)]
```

### 2.2. Nível 2: Diagrama de Containers (C2)

Este diagrama detalha as principais peças tecnológicas que compõem o sistema `IABANK`.

```mermaid
graph TD
    subgraph "Sistema IABANK"
        direction LR
        spa[Frontend SPA<br><br><b>React / TypeScript</b><br><i>(Executa no navegador do usuário)</i>]
        api[Backend API<br><br><b>Django / Python</b><br><i>(Container Docker)</i>]
        db[(Banco de Dados<br><br><b>PostgreSQL</b><br><i>(Container Docker)</i>)]
        queue[Fila de Tarefas<br><br><b>Celery / Redis</b><br><i>(Container Docker)</i>]
        webserver[Servidor Web<br><br><b>Nginx</b><br><i>(Container Docker)</i>]
    end

    user(👤 Usuário) -- "HTTPS" --> webserver
    webserver -- "Serve arquivos estáticos" --> spa
    webserver -- "/api/* (Reverse Proxy)" --> api

    spa -- "API REST (JSON/HTTPS)" --> api
    api -- "Lê/Escreve dados via ORM" --> db
    api -- "Enfileira tarefas assíncronas" --> queue
    queue -- "Processa tarefas em background" --> api
```

### 2.3. Nível 3: Diagrama de Componentes (C3) - Backend API

Este diagrama detalha os principais módulos internos do container `Backend API`, seguindo uma arquitetura em camadas.

```mermaid
graph TD
    subgraph "Container: Backend API (Django)"
        direction TB
        presentation[<b>Camada de Apresentação</b><br><i>(DRF ViewSets, Serializers)</i><br>Responsável por endpoints HTTP, validação de entrada e serialização de saída.]
        application[<b>Camada de Aplicação</b><br><i>(Services)</i><br>Orquestra a lógica de negócio, coordena fluxos de trabalho e interage com a camada de infraestrutura.]
        domain[<b>Camada de Domínio</b><br><i>(Django Models, DTOs Pydantic)</i><br>Contém as entidades de negócio, regras e a fonte da verdade dos dados.]
        infrastructure[<b>Camada de Infraestrutura</b><br><i>(Django ORM, Celery Tasks, Clients de API Externa)</i><br>Lida com a persistência de dados, comunicação com sistemas externos e tarefas em background.]
    end

    presentation -- "Chama" --> application
    application -- "Utiliza" --> domain
    application -- "Delega persistência/tarefas para" --> infrastructure
    infrastructure -- "Retorna/Manipula" --> domain
```

---

## 3. Descrição dos Componentes, Interfaces e Modelos de Domínio

### 3.1. Consistência dos Modelos de Dados (SSOT do Domínio)

Esta seção é a Fonte Única da Verdade para todas as estruturas de dados do projeto. Todos os componentes devem usar ou mapear para estes modelos.

**Tecnologia Padrão:** Pydantic `BaseModel` para DTOs e Contratos de API; Django `models.Model` para persistência.

```python
# Local: iabank/domain/models/core.py

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal

# --- Modelos de Domínio Principais (DTOs) ---

class Tenant(BaseModel):
    id: int
    name: str
    created_at: datetime

class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    role: str # Ex: 'admin', 'manager', 'consultant'

class Customer(BaseModel):
    id: int
    full_name: str
    document: str # CPF/CNPJ
    birth_date: date
    email: Optional[EmailStr] = None
    phone: str
    address_zip_code: str
    address_street: str
    # ... outros campos de endereço e contato

class Loan(BaseModel):
    id: int
    customer_id: int
    consultant_id: int
    principal_amount: Decimal = Field(..., max_digits=10, decimal_places=2)
    interest_rate: Decimal = Field(..., max_digits=5, decimal_places=2)
    iof_amount: Decimal = Field(..., max_digits=10, decimal_places=2)
    number_of_installments: int
    status: str # Ex: 'pending', 'active', 'paid_off', 'in_arrears'
    origination_date: date
    first_installment_date: date

class Installment(BaseModel):
    id: int
    loan_id: int
    installment_number: int
    due_date: date
    amount: Decimal = Field(..., max_digits=10, decimal_places=2)
    status: str # Ex: 'pending', 'paid', 'overdue'
    payment_date: Optional[date] = None

class FinancialAccount(BaseModel):
    id: int
    name: str # Ex: "Caixa Matriz", "Banco do Brasil"
    balance: Decimal = Field(..., max_digits=12, decimal_places=2)
```

### 3.2. Descrição dos Componentes do Backend

A estrutura do backend será organizada em "apps" Django, que funcionam como módulos.

- **Módulo: `iabank.core`**

  - **Responsabilidade Principal:** Contém a lógica de negócio mais fundamental e compartilhada, como o gerenciamento de multi-tenancy, modelos base, e serviços utilitários.
  - **Tecnologias Chave:** Python (Lógica Pura), Django (Models, Middleware).
  - **Dependências Diretas:** Nenhuma (é a base).

- **Módulo: `iabank.users`**

  - **Responsabilidade Principal:** Gerenciamento de usuários, autenticação (JWT), autorização (perfis e permissões).
  - **Tecnologias Chave:** Django REST Framework (Serializers, Views), `djangorestframework-simplejwt`.
  - **Dependências Diretas:** `iabank.core`

- **Módulo: `iabank.loans`**

  - **Responsabilidade Principal:** Encapsula toda a lógica de negócio do domínio de empréstimos: originação, gestão de parcelas, clientes, consultores e cobrança.
  - **Tecnologias Chave:** Django (Models, ORM), Pydantic (DTOs), Django REST Framework (Views).
  - **Dependências Diretas:** `iabank.core`, `iabank.users`, `iabank.finance`

- **Módulo: `iabank.finance`**
  - **Responsabilidade Principal:** Gestão de contas a pagar/receber, fluxo de caixa, contas bancárias e transações financeiras. Mapeia os eventos de `loans` (liberação, pagamento) para lançamentos financeiros.
  - **Tecnologias Chave:** Django (Models, ORM), Django REST Framework.
  - **Dependências Diretas:** `iabank.core`

### 3.3. Descrição dos Componentes da UI (Frontend)

- **Módulo: `frontend.ui.loans`**

  - **Responsabilidade Principal:** Agrupa todas as telas e componentes relacionados à gestão de empréstimos, como o painel de listagem, o assistente de "Novo Empréstimo" e a tela de detalhes.
  - **Tecnologias Chave:** React, TypeScript, TanStack Query, React Hook Form, Zod.
  - **Interação com Serviços:** `LoanService`, `CustomerService`.
  - **Contrato de Dados da View (ViewModel):**

    - `LoanListItemViewModel`: Representa uma única linha na tabela do painel de gestão de empréstimos.

      ```typescript
      // ViewModel para a tabela de Empréstimos
      interface LoanListItemViewModel {
        id: number;
        customerName: string;
        customerDocument: string;
        principalAmountFormatted: string; // Ex: "R$ 5.000,00"
        status: "finalizado" | "em_andamento" | "em_cobranca";
        statusLabel: string; // Ex: "Em Andamento"
        installmentsProgress: string; // Ex: "3/12"
        nextDueDate: string; // Ex: "15/09/2024"
        consultantName: string;
      }
      ```

    - **Mapeamento de Origem:** Um hook customizado (ex: `useLoansList`) será responsável por chamar o endpoint da API (`/api/v1/loans/`), que retorna uma lista de `Loan` (do SSOT). O hook então mapeia cada `Loan` para um `LoanListItemViewModel`, formatando valores monetários, calculando o progresso das parcelas e traduzindo o status para uma representação amigável na UI.

---

## 4. Descrição Detalhada da Arquitetura Frontend

A arquitetura do frontend seguirá o padrão **Feature-Sliced Design**, que promove escalabilidade, baixo acoplamento e alta coesão.

- **Padrão Arquitetural:** O código é organizado por fatias de negócio (features), não por tipo técnico. Isso torna a base de código um reflexo direto do produto, facilitando a navegação e a manutenção. A distinção entre componentes de UI (burros/presentational) e de lógica (inteligentes/container) é feita dentro de cada _feature_ ou na camada `shared`.

- **Estrutura de Diretórios Proposta (`frontend/src/`):**

  ```markdown
  src/
  ├── app/ # 1. Camada de Aplicação: Configuração global
  │ ├── providers/ # Provedores de contexto (TanStack Query, Router, Auth)
  │ ├── styles/ # Estilos globais, configuração do Tailwind
  │ └── main.tsx # Ponto de entrada da aplicação
  │
  ├── pages/ # 2. Camada de Roteamento: Mapeia rotas para layouts de página
  │ ├── DashboardPage.tsx
  │ ├── LoansPage.tsx
  │ └── ...
  │
  ├── features/ # 3. Camada de Funcionalidades: Lógica de negócio da UI
  │ ├── loan-creation/ # Ex: Wizard de Novo Empréstimo
  │ │ ├── api/ # Hooks de API (mutations) específicos para esta feature
  │ │ ├── components/ # Componentes orquestradores do wizard
  │ │ └── index.ts
  │ ├── loan-list/ # Ex: Tabela de empréstimos com filtros
  │ └── ...
  │
  ├── entities/ # 4. Camada de Entidades: Componentes e lógica de domínio do cliente
  │ ├── loan/ # Lógica/componentes de um Empréstimo (ex: LoanStatusBadge)
  │ ├── customer/ # Lógica/componentes de um Cliente (ex: CustomerAvatar)
  │ └── ...
  │
  └── shared/ # 5. Camada Compartilhada: Código reutilizável e agnóstico
  ├── api/ # Configuração do Axios, tipos de API gerados, hooks genéricos
  ├── config/ # Constantes, variáveis de ambiente
  ├── lib/ # Helpers, hooks utilitários (ex: useDebounce)
  └── ui/ # Biblioteca de componentes de UI puros (Button, Input, Table)
  ```

- **Estratégia de Gerenciamento de Estado:**

  - **Estado do Servidor:** **TanStack Query (React Query)** será a fonte única da verdade para todos os dados que vêm da API. Ele gerenciará caching, revalidação, e estados de loading/error de forma automática e eficiente.
  - **Estado Global do Cliente:** Para estados síncronos compartilhados (ex: dados do usuário logado, tema da UI), será utilizado **Zustand**. É uma biblioteca leve e simples que evita o boilerplate do Redux.
  - **Estado Local do Componente:** Estados efêmeros (ex: estado de um input de formulário, visibilidade de um modal) serão gerenciados com os hooks nativos do React (`useState`, `useReducer`).
  - **Estado de Formulários:** **React Hook Form** em conjunto com **Zod** para validação de schema será o padrão para todos os formulários.

- **Fluxo de Dados Típico (Ex: Filtrar Empréstimos):**
  1. O usuário interage com um componente de filtro na `features/loan-list`.
  2. O estado do filtro (local ou na URL) é atualizado.
  3. O hook `useQuery` (de TanStack Query), localizado em `features/loan-list/api`, tem o estado do filtro como parte de sua `queryKey`. A mudança na chave faz com que o hook automaticamente refaça a chamada à API (`GET /api/v1/loans/?status=active`).
  4. TanStack Query gerencia o estado de `loading`.
  5. A API responde com os dados. TanStack Query armazena os dados em cache e atualiza o estado `data`.
  6. Os componentes de UI na `features/loan-list`, que consomem o hook, re-renderizam para exibir a nova lista de empréstimos.

---

## 5. Definição das Interfaces Principais

As interfaces definem os contratos entre as camadas. As dependências e configurações devem ser injetadas via construtor (`__init__`).

### Exemplo: Interface para o Serviço de Aplicação de Empréstimos

```python
# Local: iabank/loans/services.py

from iabank.domain.models.core import Loan, Customer, User
from iabank.loans.repositories import LoanRepository, CustomerRepository # Abstrações de acesso a dados
from iabank.finance.services import FinancialTransactionService

class LoanApplicationService:
    """
    Serviço de aplicação para orquestrar a criação e gestão de empréstimos.
    """
    def __init__(
        self,
        loan_repo: LoanRepository,
        customer_repo: CustomerRepository,
        finance_service: FinancialTransactionService,
        default_iof_rate: float, # Configuração injetada
    ):
        self.loan_repo = loan_repo
        self.customer_repo = customer_repo
        self.finance_service = finance_service
        self.default_iof_rate = default_iof_rate

    def originate_loan(self, *, customer_data: Customer, loan_data: Loan, created_by: User) -> Loan:
        """
        Orquestra o fluxo completo de criação de um novo empréstimo.
        - Valida o cliente
        - Calcula taxas
        - Cria o empréstimo e suas parcelas
        - Gera a transação financeira de liberação do valor
        - Retorna o empréstimo criado
        """
        # ... Lógica de negócio ...
        # Ex: customer = self.customer_repo.get_or_create(customer_data)
        # Ex: new_loan = self.loan_repo.create(loan_data)
        # Ex: self.finance_service.record_loan_disbursement(loan=new_loan)
        return new_loan # Retorna o modelo de domínio
```

---

## 6. Gerenciamento de Dados

- **Persistência:** O acesso aos dados será feito através do **ORM do Django**. Para promover a separação de responsabilidades, a lógica de queries complexas pode ser encapsulada em classes `Repository` (Padrão Repository), que são chamadas pelos serviços da camada de aplicação.
- **Gerenciamento de Schema:** O sistema de **`migrations` do Django** (`makemigrations`, `migrate`) será utilizado para gerenciar a evolução do schema do banco de dados de forma controlada e versionada.
- **Seed de Dados:** Para o ambiente de desenvolvimento, serão criados **scripts de `management command` do Django** (ex: `python manage.py seed_data`) que utilizarão a biblioteca **`factory-boy`** para popular o banco de dados com dados fictícios consistentes e realistas, facilitando testes manuais e desenvolvimento da UI.

---

## 7. Estrutura de Diretórios Proposta (Monorepo)

```markdown
iabank/
├── .github/ # Configurações de CI/CD (GitHub Actions)
│ └── workflows/
│ └── main.yml
├── .vscode/ # Configurações do VS Code
├── backend/
│ ├── src/
│ │ └── iabank/ # Pacote Python principal
│ │ ├── core/
│ │ ├── users/
│ │ ├── loans/
│ │ ├── finance/
│ │ ├── reports/
│ │ ├── domain/
│ │ │ └── models/
│ │ ├── settings/
│ │ └── manage.py
│ ├── Dockerfile
│ └── ...
├── frontend/
│ ├── src/ # Código-fonte do React (conforme seção 4)
│ ├── public/
│ ├── Dockerfile
│ ├── package.json
│ └── ...
├── .env.example # Exemplo de variáveis de ambiente
├── .gitignore
├── .pre-commit-config.yaml # Configuração dos hooks de pre-commit
├── docker-compose.yml
├── LICENSE
├── CONTRIBUTING.md
├── README.md
└── CHANGELOG.md
```

---

## 8. Arquivo `.gitignore` Proposto

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.eggs/
.egg-info/
dist/
build/
*.egg
*.whl

# Django
*.log
db.sqlite3
db.sqlite3-journal
media/

# Node.js / Frontend
node_modules/
.npm/
dist/
.vite/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

# IDEs & Editors
.idea/
.vscode/
*.swp
*.swo
*~

# Sistema Operacional
.DS_Store
Thumbs.db

# Variáveis de Ambiente
.env
.env.*
!.env.example

# Testes
.pytest_cache/
.coverage
htmlcov/
```

---

## 9. Arquivo `README.md` Proposto

````markdown
# IABANK

[![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellowgreen.svg)](https://shields.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-darkgreen.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Sistema de gestão de empréstimos moderno e eficiente, projetado como uma plataforma Web SaaS robusta e segura.

## Sobre o Projeto

O `IABANK` é uma plataforma para gestão completa de empréstimos (end-to-end), concebida para ser escalável, intuitiva e adaptável às necessidades de diversas instituições financeiras. A visão futura do projeto inclui a integração com agentes de IA para automação completa do ciclo de vida do empréstimo.

## Stack Tecnológica

- **Backend:** Python, Django, Django REST Framework
- **Frontend:** React, TypeScript, Vite, Tailwind CSS
- **Banco de Dados:** PostgreSQL
- **Filas:** Celery, Redis
- **Infraestrutura:** Docker, Nginx

## Como Começar

### Pré-requisitos

- Docker
- Docker Compose

### Instalação e Execução

1.  Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/iabank.git
    cd iabank
    ```

2.  Crie o arquivo de variáveis de ambiente a partir do exemplo:

    ```bash
    cp .env.example .env
    ```

    _Obs: Ajuste as variáveis no arquivo `.env` se necessário._

3.  Suba os contêineres com Docker Compose:
    ```bash
    docker-compose up --build
    ```

A aplicação estará disponível em `http://localhost:8000`.

- **Backend API:** `http://localhost:8000/api/`
- **Frontend App:** `http://localhost:8000/`

## Como Executar os Testes

Para executar os testes do backend, acesse o contêiner da aplicação e rode o `pytest`:

```bash
docker-compose exec backend pytest
```

## Estrutura do Projeto

O projeto é um monorepo com duas pastas principais:

- `backend/`: Contém a aplicação Django (API).
- `frontend/`: Contém a aplicação React (SPA).

Consulte o Blueprint Arquitetural para mais detalhes sobre a estrutura interna de cada parte.
````

---

## 10. Arquivo `LICENSE` Proposto

A licença **MIT** é uma excelente escolha padrão, pois é permissiva e amplamente utilizada.

```text
MIT License

Copyright (c) 2024 IABANK

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 11. Arquivo `CONTRIBUTING.md` Proposto

````markdown
# Como Contribuir para o IABANK

Agradecemos o seu interesse em contribuir! Para manter a qualidade e a consistência do projeto, pedimos que siga estas diretrizes.

## Filosofia de Desenvolvimento

Este projeto segue a metodologia **AGV (Arquitetura Guiando o Valor)**. Isso significa que todas as contribuições devem estar alinhadas com o **Blueprint Arquitetural** definido. Antes de iniciar uma nova feature ou uma refatoração significativa, consulte o Blueprint. Se uma mudança arquitetural for necessária, ela deve ser discutida e o Blueprint deve ser atualizado.

## Fluxo de Trabalho

1.  Crie um _fork_ do repositório.
2.  Crie um _branch_ para a sua feature (`git checkout -b feature/nome-da-feature`).
3.  Implemente suas mudanças.
4.  Adicione testes para cobrir as novas funcionalidades.
5.  Garanta que todos os testes existentes continuem passando.
6.  Faça o _commit_ de suas mudanças seguindo um padrão claro (ex: `feat: Adiciona wizard de novo empréstimo`).
7.  Faça o _push_ para o seu _fork_ e abra um _Pull Request_ para o branch `main` do repositório original.

## Padrões e Qualidade de Código

A qualidade do código é imposta automaticamente para garantir a manutenibilidade.

### Linters e Formatadores

- **Backend (Python):** Utilizamos `Ruff` para linting e `Black` para formatação.
- **Frontend (TypeScript):** Utilizamos `ESLint` para linting e `Prettier` para formatação.

### Hooks de Pre-commit

O projeto está configurado com `pre-commit` para executar essas checagens automaticamente antes de cada commit. Para instalar, rode:

```bash
pip install pre-commit
pre-commit install
```

Qualquer código que não esteja em conformidade com os padrões será rejeitado, e o `pre-commit` tentará corrigi-lo automaticamente quando possível.

### Documentação de Código

- **Funções e Métodos Públicos:** Devem possuir _docstrings_ explicando seu propósito, parâmetros (`Args`) e o que retornam (`Returns`).
- **Classes:** Devem possuir uma _docstring_ no topo explicando sua responsabilidade principal.

O objetivo é que o código seja o mais claro e autoexplicativo possível, com a documentação servindo de apoio para a lógica mais complexa.
````

---

## 12. Estrutura do `CHANGELOG.md`

```markdown
# Changelog

Todos as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

-

### Changed

-

### Deprecated

-

### Removed

-

### Fixed

-

### Security

-

## [0.1.0] - YYYY-MM-DD

### Added

- Estrutura inicial do projeto e Blueprint Arquitetural.
```

---

## 13. Estratégia de Configuração e Ambientes

As configurações serão gerenciadas de forma segura e flexível entre os ambientes.

- **Tecnologia:** A biblioteca `django-environ` será utilizada no backend.
- **Mecanismo:**
  1. Um arquivo `.env` na raiz do projeto (listado no `.gitignore`) conterá as variáveis de ambiente para desenvolvimento local (ex: `DATABASE_URL`, `SECRET_KEY`, `DEBUG=True`).
  2. Um arquivo `.env.example` será versionado, servindo como template.
  3. Em ambientes de produção e homologação, as configurações serão injetadas diretamente como **variáveis de ambiente no contêiner Docker**, garantindo que nenhum segredo seja armazenado em código.
- **Frontend:** A configuração do Vite permite o uso de variáveis de ambiente prefixadas com `VITE_` (ex: `VITE_API_BASE_URL`), que serão lidas de um arquivo `.env` na pasta `frontend/`.

---

## 14. Estratégia de Observabilidade Completa

- **Logging Estruturado:** Todos os logs gerados pelo Django serão em formato **JSON**. Isso facilita a ingestão, busca e análise por plataformas como Sentry, Datadog ou um stack ELK. Os logs incluirão contexto relevante, como `tenant_id`, `user_id` e `request_id`. Em produção, o nível de log será `INFO`, enquanto em desenvolvimento será `DEBUG`.

- **Métricas de Negócio:** Serão expostas métricas chave através de um endpoint `/metrics` (usando `django-prometheus`) para monitoramento contínuo da saúde do negócio:

  - `loans_created_total`: Contador de novos empréstimos.
  - `payments_processed_total`: Contador de pagamentos de parcelas.
  - `active_users_gauge`: Número de usuários ativos na última hora.
  - `api_request_latency_histogram`: Histograma de latência das principais APIs.

- **Distributed Tracing:** Embora seja um monólito, a base para tracing será estabelecida usando **OpenTelemetry**. Cada requisição receberá um `trace_id` único, que será propagado para os logs e para as chamadas a sistemas externos. Isso será crucial quando os agentes de IA forem extraídos como serviços separados.

- **Health Checks e SLIs/SLOs:**

  - Será implementado um endpoint `/health` que verificará a conectividade com o banco de dados e Redis.
  - **SLI (Indicador):** Disponibilidade do endpoint de login. Latência da API de criação de empréstimo.
  - **SLO (Objetivo):** 99.9% de uptime mensal. 95% das chamadas à API de criação de empréstimo devem responder em menos de 300ms.

- **Alerting Inteligente:** Alertas serão configurados em uma ferramenta como Grafana, Prometheus Alertmanager ou Datadog. Os alertas não serão apenas sobre limiares fixos (ex: CPU > 90%), mas também sobre anomalias (ex: "queda de 50% no número de empréstimos criados por hora em comparação com a semana anterior").

---

## 15. Estratégia de Testes Detalhada

- **Testes Unitários:**

  - **Onde:** Camada de Domínio e Aplicação.
  - **O que:** Funções puras, regras de negócio, lógica de cálculo (ex: cálculo de juros), validações de serializers.
  - **Ferramentas:** `pytest`. Dependências externas (como banco de dados ou APIs) serão mockadas.

- **Testes de Integração:**

  - **Onde:** Camada de Apresentação (API) e Aplicação.
  - **O que:** Validam a interação entre componentes, especialmente o fluxo de uma requisição HTTP até o banco de dados e de volta. Ex: "Um POST em `/api/v1/loans/` cria corretamente um registro no banco e retorna um status 201".
  - **Ferramentas:** `pytest` com o `APIClient` do Django REST Framework. O banco de dados de teste será utilizado.

- **Testes End-to-End (E2E):**

  - **Onde:** Aplicação completa, do navegador ao banco de dados.
  - **O que:** Simulam o fluxo real do usuário (ex: "Logar, criar um novo cliente, solicitar um empréstimo, e verificar se ele aparece na listagem").
  - **Ferramentas:** `Playwright` ou `Cypress`. Serão executados em um pipeline de CI separado, com menor frequência (ex: antes de um deploy para produção).

- **Padrões de Teste de Integração:**
  - **Uso de Factories:** A biblioteca `factory-boy` será **obrigatória** para criar instâncias de modelos Django nos testes. Isso garante a criação de dados de teste consistentes e desacopla os testes das mudanças no schema do modelo.
  - **Simulação de Autenticação:** Para testar endpoints protegidos, o método `force_authenticate` do `APIClient` do DRF será utilizado. Isso evita a necessidade de simular o fluxo de login em cada teste, tornando-os mais rápidos e focados.
  - **Escopo de Teste:** Um teste para o endpoint de criação de empréstimos deve focar em validar o contrato desse endpoint e seus efeitos colaterais diretos. Ele assume que a autenticação e o multi-tenancy (testados em seus próprios módulos) funcionam corretamente. O middleware de multi-tenancy será ativado, mas seu teste exaustivo é feito em outro lugar.

---

## 16. Estratégia de CI/CD (Integração e Implantação Contínuas)

- **Ferramenta Sugerida:** **GitHub Actions**, com o arquivo de workflow em `.github/workflows/main.yml`.

- **Gatilhos do Pipeline:**

  - Em cada `push` para qualquer branch (executa testes e lint).
  - Em cada abertura/atualização de `Pull Request` para `main` (executa todos os checks de qualidade).
  - Em cada `merge` para o branch `main` (inicia o processo de deploy para homologação).

- **Estágios do Pipeline:**
  1. **Integração Contínua (Em cada PR):**
     - **Lint & Format Check:** Roda `Ruff`, `Black`, `ESLint`, `Prettier` para garantir a conformidade do código.
     - **Test:** Executa testes unitários e de integração para o backend e frontend.
     - **Build:** Constrói as imagens Docker de produção para garantir que o build não está quebrado.
     - **Security Scan:** Roda ferramentas como `Snyk` ou `Trivy` nas imagens Docker e dependências para detectar vulnerabilidades.
  2. **Entrega Contínua (Após merge em `main`):**
     - **Tag & Version:** Cria uma nova tag Git (ex: `v0.1.1`).
     - **Build & Push:** Constrói as imagens Docker de produção, tagueia com a nova versão e envia para um registro de contêineres (ex: Docker Hub, AWS ECR).
  3. **Implantação (Deployment):**
     - **Deploy to Staging:** Implanta automaticamente a nova versão no ambiente de homologação.
     - **Deploy to Production:** Requer uma aprovação manual (usando "environments" do GitHub Actions) para implantar a mesma imagem testada em homologação para o ambiente de produção.
  4. **Rollback:** O mecanismo de rollback será baseado na implantação da tag da versão anterior estável, que já existe no registro de contêineres.

---

## 17. Estratégia de Versionamento da API

A API será versionada via URL para garantir clareza e evitar quebras de contrato com clientes existentes.

- **Formato:** `/api/v1/{recurso}` (ex: `/api/v1/loans/`)
- **Implementação:** Em Django, isso será gerenciado usando `namespaces` no `urls.py`, permitindo que diferentes versões da API coexistam.
- **Evolução:** Mudanças que quebram o contrato (ex: remover um campo, renomear um endpoint) exigirão um incremento na versão da API (ex: para `/api/v2/`). Mudanças aditivas (adicionar um novo campo opcional ou um novo endpoint) podem ser feitas dentro da mesma versão.

---

## 18. Padrão de Resposta da API e Tratamento de Erros

Todas as respostas da API seguirão um formato JSON padronizado para consistência.

- **Resposta de Sucesso (2xx):**

  ```json
  {
    "status": "success",
    "data": {
      // Objeto ou lista de objetos
    }
  }
  ```

  _Para respostas de listagem, `data` pode conter um objeto com `count`, `next`, `previous`, `results`._

- **Resposta de Erro (4xx, 5xx):**

  ```json
  {
    "status": "error",
    "error_code": "validation_error", // Código de erro padronizado
    "message": "Um ou mais campos são inválidos.",
    "details": {
      // Opcional, para erros de validação
      "field_name": ["Esta é a mensagem de erro específica do campo."]
    }
  }
  ```

- **Tratamento de Exceções:** Um _exception handler_ customizado do Django REST Framework será implementado para capturar todas as exceções (ex: `ValidationError`, `PermissionDenied`, `NotFound`, e exceções genéricas de 500) e mapeá-las para o formato de resposta de erro padronizado.

---

## 19. Estratégia de Segurança Abrangente

- **Threat Modeling Básico:**

| Ameaça                                      | Mitigação                                                                                                                                                                                                |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Vazamento de Dados entre Tenants**        | Implementação rigorosa de Multi-tenancy na camada de dados (filtro por `tenant_id` em todas as queries via um Model Manager customizado). Testes de integração para validar o isolamento.                |
| **Acesso Não Autorizado (Insider/Externo)** | RBAC (Role-Based Access Control) granular imposto no backend. Autenticação forte com JWTs (curta duração + refresh tokens). Futura implementação de 2FA. Logs de auditoria para todas as ações críticas. |
| **Injeção de SQL**                          | Uso exclusivo do ORM do Django, que parametriza todas as queries, prevenindo esta classe de ataque.                                                                                                      |
| **Dados Sensíveis Expostos**                | Senhas hasheadas com `bcrypt`. Dados sensíveis em trânsito protegidos com HTTPS (imposto pelo Nginx). Futura avaliação de criptografia em nível de coluna para dados PII críticos.                       |

- **Estratégia de Secrets Management:**

  - **Desenvolvimento:** Arquivo `.env` local.
  - **Produção:** Segredos injetados como variáveis de ambiente no orquestrador de contêineres. Para maior segurança, será utilizado um serviço dedicado como **HashiCorp Vault** ou **AWS Secrets Manager**, onde a aplicação obtém suas credenciais em tempo de execução.

- **Compliance Framework (LGPD):**

  - A arquitetura suporta LGPD desde o início, com cada dado associado a um `Customer` (titular).
  - **Logs de Auditoria:** O módulo "Logs de Atividade" registrará quem acessou/modificou quais dados e quando.
  - **RBAC:** O princípio do menor privilégio será aplicado, garantindo que usuários só acessem os dados estritamente necessários para sua função.
  - **Retenção/Purga de Dados:** Serão criados scripts para anonimização ou exclusão de dados de clientes mediante solicitação, conforme exigido pela lei.

- **Security by Design:**
  - Toda entrada de dados da API é validada pelos Serializers do DRF (usando Zod no frontend como primeira barreira).
  - O Nginx será configurado com headers de segurança (CSP, HSTS, X-Frame-Options).
  - As dependências serão escaneadas continuamente por vulnerabilidades (CI/CD).

---

## 20. Justificativas e Trade-offs

- **Monólito vs. Microsserviços:**

  - **Decisão:** Monólito Modular.
  - **Justificativa:** Reduz a complexidade operacional e de desenvolvimento inicial, permitindo focar na entrega de valor de negócio. Garante consistência transacional (ACID) de forma nativa.
  - **Trade-off:** Em escala extrema, a implantação de todo o sistema para uma pequena mudança pode ser um gargalo. A arquitetura modular mitiga isso, permitindo a futura extração de serviços se necessário.

- **Monorepo vs. Multi-repo:**
  - **Decisão:** Monorepo.
  - **Justificativa:** Simplifica o gerenciamento de dependências e a sincronia entre API e frontend.
  - **Trade-off:** O tamanho do repositório pode crescer, e os tempos de CI podem aumentar. Isso pode ser mitigado com pipelines de CI/CD inteligentes que só testam/constroem o que mudou.

---

## 21. Exemplo de Bootstrapping/Inicialização (Conceitual)

Um exemplo de como os serviços poderiam ser instanciados e as configurações injetadas, promovendo o desacoplamento.

```python
# Local: iabank/config/service_provider.py (conceitual)

from django.conf import settings
from iabank.loans.services import LoanApplicationService
from iabank.loans.repositories import DjangoLoanRepository # Implementação concreta
from iabank.finance.services import FinancialTransactionService

class AppServices:
    """
    Container de serviços para injeção de dependência.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppServices, cls).__new__(cls)
            cls._instance._initialize_services()
        return cls._instance

    def _initialize_services(self):
        # Instanciação das dependências
        loan_repo = DjangoLoanRepository()
        finance_service = FinancialTransactionService() # Pode ter suas próprias dependências

        # Injeção de dependências e configurações via __init__
        self.loan_service = LoanApplicationService(
            loan_repo=loan_repo,
            customer_repo=..., # Outro repo
            finance_service=finance_service,
            default_iof_rate=settings.DEFAULT_IOF_RATE # Configuração vinda do settings.py
        )

# Uso em uma view do DRF
# from iabank.config.service_provider import AppServices
#
# class LoanViewSet(viewsets.ModelViewSet):
#     def create(self, request, *args, **kwargs):
#         service = AppServices().loan_service
#         ...
```

---

## 22. Estratégia de Evolução do Blueprint

- **Versionamento Semântico do Blueprint:** Este documento será versionado (ex: `IABANK-Blueprint-v1.0.0.md`).

  - **PATCH (v1.0.x):** Correções e esclarecimentos.
  - **MINOR (v1.x.0):** Adição de novos componentes ou estratégias que não quebram a arquitetura existente.
  - **MAJOR (vX.0.0):** Mudanças fundamentais (ex: decidir extrair um microsserviço, mudar o framework principal).

- **Processo de Evolução Arquitetural:** Mudanças significativas devem ser propostas através de um **Architectural Decision Record (ADR)**. Um ADR é um documento curto que descreve o contexto de uma decisão, as opções consideradas e a decisão final com sua justificativa. Os ADRs aprovados são a base para uma nova versão do blueprint.

- **Compatibilidade e Deprecação:** Quando uma interface (ex: API v1) for substituída, ela será marcada como `deprecated`. Será mantida uma política de suporte por um período definido (ex: 6 meses) antes de ser removida, garantindo tempo para os clientes migrarem.

---

## 23. Métricas de Qualidade e Quality Gates

- **Métricas de Cobertura de Código:**

  - **Meta:** Mínimo de **85%** de cobertura de testes para todo o backend.
  - **Exceções:** Código de migração do Django, arquivos de configuração.
  - **Ferramenta:** `pytest-cov`.

- **Métricas de Complexidade:**

  - **Complexidade Ciclomática:** Máximo de **10** por função/método.
  - **Tamanho da Função:** Máximo de **50 linhas** de código (excluindo docstrings e comentários).
  - **Ferramenta:** `Ruff` pode ser configurado para impor esses limites.

- **Quality Gates Automatizados (no Pipeline de CI):** Um Pull Request só poderá ser mesclado se:

  - Todos os testes unitários e de integração passarem.
  - A cobertura de código for igual ou superior à meta.
  - A análise de linting (`Ruff`, `ESLint`) não reportar erros.
  - A varredura de segurança (`Snyk`/`Trivy`) não encontrar vulnerabilidades de severidade alta ou crítica.

- **Métricas de Performance:**
  - **Tempo de Resposta da API (p95):** < 500ms para endpoints de leitura, < 800ms para endpoints de escrita.
  - **Queries de Banco de Dados por Requisição:** Alertas serão gerados se uma requisição executar um número anômalo de queries (N+1), usando ferramentas como `django-debug-toolbar` em desenvolvimento e APM em produção.

---

## 24. Análise de Riscos e Plano de Mitigação

| Categoria       | Risco Identificado                                                                  | Probabilidade (1-5) | Impacto (1-5) | Score (P×I) | Estratégia de Mitigação                                                                                                                                                                                           |
| :-------------- | :---------------------------------------------------------------------------------- | :-----------------: | :-----------: | :---------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Segurança**   | **Violação de dados e acesso não autorizado entre tenants.**                        |          3          |       5       |     15      | Implementação rigorosa de multi-tenancy na camada de acesso a dados. Testes de integração específicos para isolamento. Auditoria de acesso. RBAC granular.                                                        |
| **Negócio**     | **Cálculos financeiros incorretos (juros, multas, parcelas).**                      |          2          |       5       |     10      | Testes unitários exaustivos para toda a lógica de cálculo. Uso do tipo `Decimal` para todas as operações monetárias. Revisão por pares (peer review) obrigatória para código financeiro.                          |
| **Técnico**     | **Débito técnico acumulado devido a prazos, dificultando a manutenção.**            |          4          |       3       |     12      | Adoção estrita dos Quality Gates (lint, testes, cobertura). Refatoração contínua como parte do processo de desenvolvimento (regra do escoteiro). Alocação de tempo (ex: 10% do sprint) para pagar débito técnico. |
| **Performance** | **Gargalos no banco de dados com o aumento do volume de empréstimos e pagamentos.** |          3          |       4       |     12      | Monitoramento proativo de queries lentas (APM). Estratégia de indexação de banco de dados. Caching em nível de aplicação (Redis) para dados frequentemente acessados e de leitura intensiva.                      |
| **Regulatório** | **Não conformidade com a LGPD ou futuras regulamentações financeiras.**             |          2          |       5       |     10      | Arquitetura projetada com LGPD em mente. Manter uma trilha de auditoria completa. Consultoria jurídica para revisar os fluxos de dados e políticas de retenção.                                                   |

---

**Diretrizes Essenciais:**

1. **Análise de Dependências com Decomposição Máxima:** A ordem de implementação deve ser determinada pelo princípio de **responsabilidade única por alvo**. Siga estas regras de decomposição:

   a. **Ordem de Módulos Transversais:** Os módulos que fornecem funcionalidades transversais **DEVEM** ser implementados primeiro. A ordem de implementação e validação entre eles deve seguir a lógica de dependência: **Autenticação > Gestão de Usuários e Autorização > Multi-Tenancy**.

   b. **Decomposição Obrigatória por Tipo (Backend):** Para cada módulo de negócio (ex: `iabank.users`, `iabank.loans`), você **DEVE** criar alvos de implementação separados e sequenciais para cada camada lógica, na seguinte ordem:

   1. **Modelos:** Apenas os arquivos `models.py`.
   2. **Repositórios/Infraestrutura:** Apenas a lógica de acesso a dados.
   3. **Serviços de Aplicação:** Apenas a lógica de negócio dos casos de uso.
   4. **Serializers:** Apenas os arquivos `serializers.py` da API.
   5. **Views/URLs:** Apenas os endpoints `views.py` e o roteamento `urls.py`.

   c. **Regra Especial para `users`:** O módulo de usuários **DEVE** ser decomposto em duas fases funcionais distintas, cada uma com sua própria parada de testes:

   1. **Fase 1: Autenticação JWT.** Implemente apenas os modelos, serializers e views necessários para os endpoints de obtenção e refresh de token (ex: `/token/`).
   2. **Fase 2: Gestão de Usuários e Autorização.** Após validar a autenticação, implemente os endpoints de CRUD de usuários (ex: `/users/`, `/users/me/`) e a lógica de permissões/perfis (RBAC).

2. **Criação do "Alvo 0":** Sua primeira tarefa é SEMPRE gerar um item inicial na ordem de implementação chamado **"Alvo 0: Setup do Projeto Profissional"**. Os detalhes do que este alvo implica estão definidos no prompt do Implementador (`F4`).

3. **Geração da Ordem Sequencial e Pontos de Teste:** Crie uma lista numerada de "Alvos de Implementação".

   - **Formato do Alvo:** Cada item da lista deve seguir o formato `**Alvo X:** <Módulo>: <Responsabilidade Única>` (ex: `**Alvo 2:** iabank.users: Modelos e Migrações`).
   - **Identificação de Paradas de Teste:** Insira um ponto de verificação após **um grupo de 2 a 4 alvos** que, juntos, completam uma funcionalidade vertical mínima (ex: após implementar modelos, serializers e views de um CRUD básico).
   - **Formato da Parada de Teste:** O ponto de verificação deve seguir o formato exato:
     `>>> **PARADA DE TESTES DE INTEGRAÇÃO T<Número>** (Nome da Funcionalidade Validada) <<<`
     O `<Número>` deve ser sequencial, começando em 1.

4. **Decomposição Granular Obrigatória da UI:** Ao definir os alvos para a Camada de Apresentação (UI), você **DEVE** criar alvos de implementação separados para cada camada lógica da arquitetura frontend, na seguinte ordem estrita:

   a. **Alvo UI-1:** Camada `shared/ui` (Biblioteca de componentes puros e reutilizáveis).
   b. **Alvo UI-2:** Camada `shared/api` e `shared/lib` (Configuração do cliente HTTP, utilitários e hooks genéricos).
   c. **Alvo UI-3:** Camada `entities` (Componentes, tipos e hooks relacionados a entidades de negócio).
   d. **Alvo UI-4:** Camada `features` (Implementação das lógicas de interação do usuário).
   e. **Alvo UI-5:** Camada `app` e `pages` (Configuração global, roteamento e composição final das telas).

   **Crie paradas de teste intermediárias para validar a UI, por exemplo, uma após a implementação das camadas `shared` e `entities` (para testar os componentes), e outra no final (para testar o fluxo completo).**

5. **Geração de Cenários de Teste de Integração:**

   - Para cada `>>> PARADA ... <<<` criada, você **DEVE** gerar uma seção detalhada logo abaixo dela.
   - Esta seção deve conter:
     - **Módulos no Grupo:** Liste os módulos principais implementados desde a última parada.
     - **Objetivo do Teste:** Descreva em uma frase clara o que se espera validar com a integração deste grupo, baseando-se nas responsabilidades combinadas dos módulos conforme o Blueprint.
     - **Cenários Chave:** Liste de 2 a 4 cenários de teste específicos e acionáveis que verifiquem as interações mais críticas. Para paradas que dependem de etapas anteriores (ex: testar uma funcionalidade que requer autenticação), os cenários devem mencionar o uso de simulação de pré-condições (ex: "Usando um usuário autenticado simulado...") em vez de repetir o fluxo completo.

6. **Simplicidade do Output:** O resultado final deve ser um documento Markdown contendo apenas a lista numerada da "Ordem de Implementação" com os "Alvos" e as "Paradas de Teste" detalhadas. **Não inclua justificativas ou descrições adicionais; foque apenas no plano de ação.**

**Resultado Esperado:**

Um documento Markdown (`Output_Ordem_e_Testes.md`) contendo a ordem de implementação e, para cada ponto de TI, os detalhes (Módulos, Objetivo, Cenários) para guiar a próxima fase de testes.
