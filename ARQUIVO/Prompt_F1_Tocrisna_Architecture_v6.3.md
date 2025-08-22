# AGV Prompt Template: Tocrisna v6.3 - Definição da Arquitetura Técnica e de Produto

## Tarefa Principal

Definir e documentar uma proposta de arquitetura de alto nível, cobrindo tanto os **aspectos técnicos (software)** quanto os de **produto (experiência do usuário)**. O resultado deve ser um Blueprint que sirva como a fonte única da verdade para a estrutura, componentes, contratos de serviço e, crucialmente, os contratos de apresentação de dados da UI. O foco é na modularidade, clareza, manutenibilidade e na criação de um "produto de engenharia" completo e profissional.

## Contexto e Definições Iniciais do Projeto: (Fornecido pelo usuário)

- **Nome do Projeto:** `[NOME_DO_PROJETO]`

- **Visão Geral / Objetivo Principal:**
  [DESCRIÇÃO CLARA DO PROPÓSITO GERAL DO SOFTWARE, O PROBLEMA QUE RESOLVE E SEU OBJETIVO FINAL.]

- **Funcionalidades Chave (Alto Nível):**
  [LISTA (BULLET POINTS) DAS PRINCIPAIS CAPACIDADES OU FEATURES QUE O SOFTWARE DEVE TER.]

- **Público Alvo / Ambiente de Uso:** `[QUEM USARÁ O SOFTWARE E EM QUE CONTEXTO? ISSO AJUDA A INFERIR REQUISITOS NÃO FUNCIONAIS. Ex: Usuários finais em desktop, Aplicação web interna, Serviço de backend.]`

- **Stack Tecnológica Definida:**

  - Linguagem Principal: `[Ex: Python 3.10+]`
  - Framework Principal (se houver): `[Ex: FastAPI, Flask, Nenhum, PySide6]`
  - Bibliotecas Essenciais Pré-definidas: `[Ex: Pillow, numpy, LangChain, BLAKE3, send2trash, stream-unzip]`
  - Banco de Dados (se aplicável): `[Ex: PostgreSQL com pgvector, SQLite, Nenhum]`
  - Outras Tecnologias Chave: `[Ex: Docker, LangFuse]`

- **Requisitos Não Funcionais Iniciais (se houver):**

  - Performance Esperada: `[Ex: Processar X itens por segundo, Tempo de resposta < Y ms, Foco em alta performance]`
  - Escalabilidade: `[Ex: Deve suportar Z usuários concorrentes, Volume de dados esperado]`
  - Segurança: `[Ex: Nível básico de segurança para dados de usuário, Autenticação necessária]`
  - Multi-tenancy (se SaaS): `[Ex: Isolamento por tenant, Dados compartilhados vs isolados]`
  - Compliance (se aplicável): `[Ex: PCI DSS, LGPD, SOX, HIPAA]`
  - Auditoria (se aplicável): `[Ex: Log de transações, Trilha de auditoria completa]`

- **Principais Restrições (se houver):** `[Ex: Orçamento limitado, Prazo curto, Deve integrar com API X existente]`
- **Definição de Escopo (Opcional - Recomendado para projetos complexos):**
  - **Dentro do Escopo:** `[Lista explícita do que SERÁ implementado. Ex: Módulo X, Feature Y, Integração Z]`
  - **Fora do Escopo:** `[Lista explícita do que NÃO será implementado para evitar scope creep. Ex: App móvel nativo, Integração com sistema legado ABC]`

## Diretrizes e Princípios Arquiteturais (Filosofia AGV)

1. **Modularidade e Separação de Responsabilidades (SRP):** Proponha uma divisão clara em módulos/componentes lógicos, cada um com uma responsabilidade bem definida. Minimize o acoplamento entre eles e maximize a coesão interna.
2. **Clareza e Manutenibilidade:** A arquitetura deve ser fácil de entender, manter e evoluir. Prefira soluções mais simples (KISS) quando apropriado.
3. **Definição Explícita de Interfaces e Construção de Componentes:** **CRUCIAL:**
   - **Interfaces de Serviço (Contratos Funcionais):** Para os principais pontos de interação entre os módulos identificados, defina claramente as interfaces (contratos) que eles expõem ou consomem.
     - **Abstração da Infraestrutura:** Isto inclui, obrigatoriamente, abstrair interações com a infraestrutura. Prefira definir componentes wrapper (ex: `FileSystemService`, `ConcurrencyService`, `BackupService`) na camada de infraestrutura com interfaces claras, em vez de usar bibliotecas de baixo nível (como `pathlib`, `shutil`, `concurrent.futures`) diretamente nas camadas superiores (Core, Application) onde possível.
     - A definição da interface de serviço deve incluir:
       - Assinaturas de funções/métodos públicos chave (com tipos de parâmetros e retorno).
       - Estruturas de dados (Dataclasses, Pydantic Models) usadas para troca de informações através desses métodos.
       - Uma breve descrição do propósito de cada método exposto.
   - **Configuração e Construção de Componentes:** Para cada componente/serviço principal proposto (especialmente aqueles que não são puramente modelos de dados):
     - Se o componente depender de valores de configuração externos essenciais para seu funcionamento (ex: caminhos de arquivo padrão, URLs de API, chaves secretas, níveis de log, etc.), **indique explicitamente como esses valores de configuração seriam fornecidos ao componente em sua inicialização.**
     - **Priorize a passagem de parâmetros de configuração através do construtor (`__init__`) do componente.** Detalhe os parâmetros de configuração chave que o construtor deve aceitar.
     - Se, alternativamente, a configuração for obtida de um serviço de configuração centralizado ou por um método de configuração dedicado, mencione essa abordagem e a interface relevante.
     - O objetivo é garantir que o blueprint deixe claro como os componentes são instanciados com suas configurações necessárias, promovendo desacoplamento e testabilidade.
4. **Listagem Explícita de Dependências Diretas:** **IMPORTANTE:** Para cada componente/módulo principal descrito, liste explicitamente os **outros arquivos `.py` ou módulos específicos** dos quais ele depende diretamente para importar e usar funcionalidades. Use caminhos relativos à raiz do projeto (ex: `fotix.domain.models`, `utils.helpers`).
5. **Testabilidade:** A arquitetura deve facilitar a escrita de testes unitários e de integração (ex: permitir injeção de dependência onde fizer sentido).
6. **Segurança Fundamental:** Incorpore princípios básicos de segurança desde o design (ex: onde a validação de input deve ocorrer, como dados sensíveis podem ser tratados – sugerir hashing/criptografia, necessidade de autenticação/autorização).
7. **Aderência à Stack:** Utilize primariamente as tecnologias definidas na Stack Tecnológica. Se sugerir uma tecnologia _adicional_, justifique claramente a necessidade.
8. **Padrões de Design:** Sugira e aplique padrões de design relevantes (ex: Repository, Service Layer, Observer, Strategy, etc.) onde eles agregarem valor à estrutura e manutenibilidade. Justifique brevemente a escolha.
9. **Escalabilidade (Básica):** Considere como a arquitetura pode suportar um crescimento moderado no futuro (ex: design sem estado para serviços, possibilidade de paralelizar tarefas usando `concurrent.futures`).
10. **Especificação de Tecnologias para Tipos de Componentes:** Para garantir consistência e aderência à stack definida, ao descrever os componentes/módulos, você DEVE especificar a tecnologia ou biblioteca principal a ser utilizada para certos tipos de artefatos, quando aplicável e relevante para a arquitetura. Por exemplo:
    - **Modelos de Dados (DTOs, entidades de domínio, configurações):** Especificar o uso de **Pydantic `BaseModel`** como a tecnologia padrão para sua definição, visando validação de dados e facilidades de serialização.
    - **Camada de Acesso a Dados (se houver BD):** Especificar o ORM (ex: SQLAlchemy) ou a biblioteca de acesso.
    - **APIs Web (se houver):** Especificar o framework (ex: FastAPI, Flask).
    - **Interface de Usuário (se houver):** Especificar o framework de UI (ex: PySide6). \* (Adicionar outros tipos de componentes/tecnologias conforme a necessidade do projeto).
      Estas especificações devem constar na descrição de cada componente relevante no Blueprint Arquitetural.

## Resultado Esperado (Blueprint Arquitetural)

Um documento (preferencialmente em Markdown) descrevendo a arquitetura proposta, incluindo:

1. **Visão Geral da Arquitetura:** Um breve resumo da abordagem arquitetural escolhida (ex: Arquitetura em Camadas, Microsserviços simples, Baseada em Eventos, etc.) e uma justificativa. Esta seção também deve definir a estratégia de organização do código-fonte, esclarecendo se será utilizado um monorepo (com backend e frontend no mesmo repositório) ou múltiplos repositórios, e justificar a escolha.
2. **Diagramas da Arquitetura (Modelo C4):** Gere os diagramas utilizando a sintaxe do Mermaid.js, seguindo os 3 níveis principais do Modelo C4 para uma visualização clara e em camadas.

   - **2.1. Nível 1: Diagrama de Contexto do Sistema (C1)**

     - **Objetivo:** Mostrar como o sistema se encaixa no mundo, interagindo com usuários e sistemas externos. É a visão mais macro, mostrando o sistema como uma "caixa preta" e suas interações externas.
     - **Elementos a incluir:** Sistema principal (como um único bloco), tipos de usuários, sistemas externos que interagem.
     - **Exemplo de estrutura Mermaid:**

       ```mermaid
       graph TD
           subgraph "Sistema [NOME_DO_PROJETO]"
               A[Sistema Principal]
           end
           U1[Tipo Usuário 1] -->|interage via| A
           U2[Tipo Usuário 2] -->|interage via| A
           A -->|conecta com| SE1[Sistema Externo 1]
       ```

   - **2.2. Nível 2: Diagrama de Containers (C2)**

     - **Objetivo:** Dar um "zoom" no Sistema, mostrando as principais "caixas" tecnológicas (containers) que o compõem e como elas se comunicam. Um container é uma unidade executável/implantável (ex: aplicação web, banco de dados, API).
     - **Elementos a incluir:** Frontend, Backend API, Banco de Dados, Cache, Filas, etc.
     - **Exemplo de estrutura Mermaid:**

       ```mermaid
       graph TD
           U[Usuários] -->|HTTPS| F[Frontend SPA]
           F -->|API REST| B[Backend API]
           B -->|SQL| DB[(Banco de Dados)]
           B -->|Pub/Sub| Q[Fila de Mensagens]
       ```

   - **2.3. Nível 3: Diagrama de Componentes (C3) - Exemplo para o Container Principal**

     - **Objetivo:** Dar um "zoom" em um container específico (geralmente o Backend API) para mostrar seus principais componentes/módulos internos e suas responsabilidades.
     - **Elementos a incluir:** Camadas internas (Apresentação, Aplicação, Domínio, Infraestrutura) ou componentes principais do container escolhido.
     - **Nota:** Este nível é opcional mas recomendado para o container mais complexo do sistema.
     - **Exemplo de estrutura Mermaid:**

       ```mermaid
       graph TD
           subgraph "Container: Backend API"
               C1[Camada de Apresentação/API]
               C2[Camada de Aplicação/Serviços]
               C3[Camada de Domínio/Negócio]
               C4[Camada de Infraestrutura/Dados]
           end
           C1 --> C2
           C2 --> C3
           C2 --> C4
       ```

3. **Descrição dos Componentes, Interfaces e Modelos de Domínio:**

   - Para cada componente principal:

     - Nome claro (ex: `fotix.core.duplicate_finder`).
     - Responsabilidade principal.
     - **Tecnologias Chave da Stack que Serão Usadas Nele:** Conforme a Diretriz 10 ("Especificação de Tecnologias para Tipos de Componentes"), indique a biblioteca ou framework principal para este componente (ex: "Pydantic `BaseModel`" para módulos de modelos de dados; "PySide6" para componentes de UI; "FastAPI" para um serviço de API; `logging` stdlib para um serviço de logging, etc.). Se for apenas lógica Python pura sem uma biblioteca externa dominante, indique "Python (Lógica Pura)".
     - **Dependências Diretas (Lista explícita - Diretriz 4).**

   - **3.1. Consistência dos Modelos de Dados (SSOT do Domínio):**

     - Defina todos os seus modelos de dados principais (DTOs, entidades de domínio, etc.) em uma única seção dedicada (ex: "Camada de Domínio/Core - Models"). **Esta seção é a Fonte Única da Verdade (SSOT) para todas as estruturas de dados do projeto.**
     - Ao definir as interfaces na Seção 4, os tipos de retorno e os parâmetros que forem objetos complexos **DEVEM OBRIGATORIAMENTE** referenciar os modelos definidos nesta seção "Models" (a SSOT do Domínio).
     - Se um componente (como um serviço de infraestrutura) lida com uma fonte de dados externa (ex: uma API, metadados de um arquivo ZIP) que não corresponde exatamente ao modelo de domínio canônico, a **"Responsabilidade Principal"** desse componente deve incluir explicitamente a tarefa de **"mapear" ou "traduzir" os dados da fonte para o modelo de domínio oficial**. O Blueprint não deve criar um modelo de dados duplicado ou divergente para acomodar a fonte externa.

   - **Para a Camada de Apresentação (UI) (ex: `fotix.ui`):**

     - Além da descrição geral da UI, **proponha uma decomposição em principais Telas/Views ou Componentes de UI reutilizáveis significativos.**
     - Para cada Tela/View/Componente de UI proposto:

       - Descreva brevemente seu propósito principal.
       - Liste os principais serviços da Camada de Aplicação com os quais ele provavelmente interagirá.
       - Sugira se sua implementação pode ser considerada uma unidade de trabalho relativamente independente.
       - **Contrato de Dados da View (ViewModel):**

         - Para componentes que exibem dados complexos (tabelas, listas, árvores), defina a estrutura de dados explícita que a View deve consumir. Esta definição serve como um "ViewModel" ou "Presentation Model" e é um contrato formal.
         - **Estrutura de Dados da View:** Defina a estrutura usando sintaxe de `dataclass` ou `Pydantic Model` para clareza. Esta estrutura deve representar uma única unidade de exibição (ex: uma linha na tabela).
         - **Mapeamento de Origem:** Explique claramente como essa estrutura de dados da view é derivada dos Modelos de Domínio canônicos (definidos na seção "SSOT do Domínio").
         - **Exemplo de como isso deve ser formatado no Blueprint de saída:**

         ```python
         - Módulo: `fotix.ui.results_view`
           - ... (outras descrições)
           - Contrato de Dados da View (ViewModel):
             - `ResultsViewRow(ViewModel)`: Representa uma única linha na tabela de resultados, correspondendo a um `DuplicateSet` completo.
               - `keeper_name: str`
               - `keeper_path: str`
               - `duplicates_summary: str` (Ex: "duplicate1.jpg (1.2 MB), duplicate2.png (2.3 MB)")
               - `space_saved_mb: float`
             - Mapeamento de Origem: A camada de orquestração (ex: `MainWindow` ou um `Controller`) será responsável por iterar sobre a lista de `DuplicateSet` do `ScanResult` e, para cada um, criar uma instância de `ResultsViewRow`. Os campos são preenchidos a partir das propriedades do `DuplicateSet` e seus `MediaFile` associados.
         ```

4. **Descrição Detalhada da Arquitetura Frontend:** Descreva a arquitetura e a organização de diretórios propostas para a aplicação cliente (SPA). O objetivo é garantir modularidade, escalabilidade e uma clara separação de responsabilidades, independentemente do framework de UI escolhido. A descrição deve incluir:

   - **Padrão Arquitetural:** Adote e explique um padrão de design ou filosofia para a organização do código. Justifique como o padrão escolhido ajuda a separar as responsabilidades. Exemplos de conceitos a serem abordados:

     - **Separação por Funcionalidade (Feature-based):** Organizar o código em torno de funcionalidades de negócio em vez de tipos de arquivo (ex: uma pasta `novo-emprestimo/` contendo seus componentes, estado e lógica de API, em vez de pastas separadas `components/`, `hooks/`, `api/`).
     - **Componentes de UI vs. Componentes de Lógica (Presentational vs. Container):** Como a arquitetura distingue componentes "burros" que apenas exibem dados de componentes "inteligentes" que gerenciam estado e lógica.

   - **Estrutura de Diretórios Proposta:** Proponha uma estrutura de diretórios `src` que reflita o padrão arquitetural. Detalhe o propósito de cada camada ou pasta principal de forma conceitual, por exemplo:

     - **Camada de Aplicação (`app/` ou `core/`):** Configuração global (roteamento, injeção de dependência, provedores de estado, estilos globais).
     - **Camada de Roteamento/Páginas (`pages/`, `views/` ou `routes/`):** Os pontos de entrada para as diferentes telas do sistema.
     - **Camada de Funcionalidades (`features/`):** Módulos que encapsulam uma funcionalidade de negócio completa, orquestrando a lógica e a UI.
     - **Camada de Entidades (`entities/`):** Lógica de negócio e componentes relacionados a entidades de domínio do cliente (ex: um card de `Cliente`, um modelo de `Empréstimo`).
     - **Camada Compartilhada (`shared/` ou `lib/`):** Código totalmente reutilizável e agnóstico de negócio:
       - `ui/`: A biblioteca de componentes de UI puros (Botão, Input, Tabela, etc.).
       - `api/`: Configuração do cliente HTTP e definições de contrato com o backend.
       - `lib/`: Funções utilitárias, helpers, hooks genéricos, etc.

   - **Estratégia de Gerenciamento de Estado:** Especifique claramente a abordagem para os diferentes tipos de estado:

     - **Estado do Servidor (Server State):** Como os dados vindos da API serão buscados, cacheados e sincronizados. Mencione o uso de bibliotecas especializadas (como TanStack Query, SWR, Apollo Client) como a fonte da verdade para esses dados.
     - **Estado Global do Cliente (Global Client State):** Se e como o estado síncrono compartilhado entre diferentes partes da UI será gerenciado (ex: informações do usuário logado, tema da UI). Sugira ferramentas apropriadas para o ecossistema do framework (ex: Zustand, Jotai para React; Pinia para Vue; Stores para Svelte).
     - **Estado Local do Componente (Local Component State):** Confirme que o estado efêmero e não compartilhado deve ser mantido localmente nos componentes usando os mecanismos nativos do framework.

   - **Fluxo de Dados:** Descreva brevemente o fluxo de dados típico na aplicação, desde a interação do usuário, passando pela camada de funcionalidades, a chamada à API, a atualização do estado do servidor, até a renderização final nos componentes de UI.

5. **Definição das Interfaces Principais:** Detalhamento dos contratos de comunicação entre os componentes chave (conforme Diretriz 3), incluindo como os componentes recebem suas configurações iniciais (priorizando `__init__`).
6. **Gerenciamento de Dados (se aplicável):** Como os dados serão persistidos e acessados (ex: Módulo data_access usando SQLAlchemy com padrão Repository, ou especificando Pydantic `BaseModel` para modelos de dados se não houver persistência complexa). Além da persistência, a seção deve descrever a estratégia para: Gerenciamento de Schema (confirmando o uso de migrações automáticas como as do Django) e Seed de Dados (como popular o banco de dados de desenvolvimento com dados iniciais/fictícios, ex: usando scripts customizados, fixtures ou bibliotecas como factory-boy).
7. **Estrutura de Diretórios Proposta:** Uma sugestão inicial, **preferencialmente utilizando o layout `src` moderno** (com o código principal do pacote dentro de uma pasta `src/nome_do_pacote/`) para melhor organização e empacotamento, mostrando a organização das pastas e arquivos principais.
8. **Arquivo `.gitignore` Proposto:** Um conteúdo sugerido, **completo e pronto para uso**, para o arquivo `.gitignore` na raiz do projeto, apropriado para a "Stack Tecnológica Definida". Ele deve ser abrangente, cobrindo caches, ambientes virtuais, arquivos de IDEs comuns (VS Code, PyCharm), e arquivos específicos do SO.
9. **Arquivo `README.md` Proposto:** A geração do **conteúdo completo** para um arquivo `README.md` inicial e profissional. O README deve seguir uma estrutura padrão, contendo, no mínimo:
   - O nome do projeto e uma descrição concisa.
   - Badges de status (pode usar placeholders).
   - Seção "Sobre o Projeto".
   - Seção "Stack Tecnológica".
   - Seção "Como Começar" (com instruções para instalar dependências e rodar o projeto).
   - Seção "Como Executar os Testes".
   - Seção "Estrutura do Projeto" (uma breve explicação das pastas principais).
10. **Arquivo `LICENSE` Proposto:** Uma sugestão de licença de software (ex: MIT, Apache 2.0) e a geração do **texto completo** correspondente para o arquivo `LICENSE` na raiz do projeto. Se nenhuma for especificada, sugira a MIT como um padrão seguro.
11. **Arquivo `CONTRIBUTING.md` Proposto:** A geração de um **template de conteúdo** para o `CONTRIBUTING.md`, descrevendo como contribuir para um projeto que segue o Método AGV (ex: seguir o blueprint, garantir testes, etc.). O documento deve também mencionar as políticas de qualidade de código, como o uso de linters (ex: Ruff, ESLint) e formatadores (ex: Black, Prettier), e sugerir a automação dessas checagens através de ganchos de pre-commit (mencionando o arquivo .pre-commit-config.yaml). Adicionalmente, o documento deve estabelecer um padrão mínimo para a documentação de código (ex: estilo de docstrings para funções públicas e classes) para garantir a manutenibilidade do projeto a longo prazo.
12. **Estrutura do `CHANGELOG.md`:** A geração de um arquivo `CHANGELOG.md` inicial, contendo apenas a estrutura padrão (ex: `## [Unreleased]`, `## [0.1.0] - YYYY-MM-DD`) para ser preenchido futuramente.
13. **Estratégia de Configuração e Ambientes:** Descreva como as configurações da aplicação (segredos, conexões de banco de dados, etc.) serão gerenciadas em diferentes ambientes (desenvolvimento, homologação, produção). Sugira o uso de variáveis de ambiente e arquivos de configuração específicos por ambiente (ex: usando python-decouple ou django-environ).
14. **Estratégia de Observabilidade Completa:** Detalhe uma abordagem abrangente para observabilidade do sistema em produção. A descrição deve incluir:

    - **Logging Estruturado:** Defina a abordagem para logging de eventos e erros. Sugira o uso de logs estruturados (JSON) para facilitar a análise por ferramentas externas (ex: Sentry, Datadog, ELK Stack). Defina diferentes níveis de log para produção e desenvolvimento.

    - **Métricas de Negócio:** Defina métricas específicas do domínio que devem ser coletadas e como elas serão expostas e visualizadas. Especifique métricas que permitam monitorar a saúde do negócio, não apenas da infraestrutura.

    - **Distributed Tracing:** Para arquiteturas com múltiplos serviços, defina a estratégia de rastreamento distribuído para debugar problemas de performance e identificar gargalos entre componentes.

    - **Health Checks e SLIs/SLOs:** Defina indicadores de saúde do sistema (Service Level Indicators) e objetivos de nível de serviço (Service Level Objectives) mensuráveis. Especifique endpoints de health check e critérios de disponibilidade.

    - **Alerting Inteligente:** Defina estratégia de alertas baseada em anomalias e tendências, não apenas limites fixos, para reduzir ruído e focar em problemas reais que impactem usuários ou negócio.

15. **Estratégia de Testes Detalhada:** Elabore sobre a seção "Como Executar os Testes". Detalhe os diferentes tipos de testes a serem implementados (Unitários, Integração, End-to-End/API), em quais camadas da arquitetura cada um se aplica e as ferramentas recomendadas (pytest, APIClient do DRF, etc.). **Esta seção deve também incluir:**

    - **Estrutura e Convenção de Nomenclatura de Testes:** Defina a estrutura de diretórios para os testes (ex: `tests/unit`, `tests/integration`). Para evitar conflitos de nomes de módulos, estabeleça uma convenção de nomenclatura explícita para os arquivos de teste, como `test_<nome_do_app>_<nome_do_modulo>.py` (ex: `test_users_models.py`, `test_loans_services.py`).
    - **Padrões de Teste de Integração:** Defina as convenções para escrever testes de integração robustos e de fácil manutenção:
      - **Uso de Factories:** Recomende o uso de uma biblioteca de "factories" (ex: `factory-boy` para Python, `Faker.js` para Node) para a criação de dados de teste complexos e consistentes, evitando a configuração manual de objetos em cada teste.
      - **Simulação de Autenticação:** Para testes que requerem um usuário autenticado, especifique o uso de métodos de simulação fornecidos pelo framework (ex: `force_authenticate` no DRF, `TestSecurityContextHolder` no Spring Security) em vez de simular o fluxo de login completo em cada teste. Isso isola o teste da lógica de autenticação.
      - **Escopo de Teste:** Enfatize que os testes de integração de uma funcionalidade (ex: CRUD de Empréstimos) devem focar em validar **essa** funcionalidade, tratando dependências já testadas (como autenticação e multi-tenancy) como "caixas-pretas" que podem ser simuladas ou pré-configuradas.

16. **Estratégia de CI/CD (Integração e Implantação Contínuas):** Descreva uma estratégia de CI/CD de alto nível para automatizar a construção, teste e implantação da aplicação. A descrição deve incluir:

    - **Ferramenta Sugerida:** Recomende uma ferramenta de CI/CD (ex: GitHub Actions, GitLab CI, Jenkins) e a criação de um arquivo de configuração de pipeline na raiz do projeto (ex: `.github/workflows/main.yml`).

    - **Gatilhos do Pipeline:** Defina quando o pipeline deve ser executado (ex: em cada push para o branch `main` e em cada abertura de Pull Request).

    - **Estágios do Pipeline:** Defina uma estratégia de CI/CD que cubra os aspectos essenciais do ciclo de vida do software:
      - **Integração Contínua:** Como o código será validado automaticamente (build, qualidade, testes)
      - **Entrega Contínua:** Como os artefatos serão empacotados e versionados
      - **Implantação:** Estratégia conceitual para deploy em diferentes ambientes
      - **Rollback:** Mecanismo de reversão em caso de problemas

17. **Estratégia de Versionamento da API:** Proponha uma estratégia para versionar a API (ex: via URL, como /api/v1/...) para permitir futuras evoluções sem quebrar os clientes existentes (como o frontend ou apps móveis).
18. **Padrão de Resposta da API e Tratamento de Erros:** Defina um formato de resposta JSON padrão e consistente para todos os endpoints da API, tanto para sucesso quanto para erros. Descreva como as exceções (ex: validação, não encontrado, erro de servidor) serão capturadas e mapeadas para respostas de erro padronizadas.
19. **Estratégia de Segurança Abrangente:** Detalhe uma abordagem estruturada para segurança que vai além dos princípios básicos. A descrição deve incluir:

    - **Threat Modeling Básico:** Identifique e documente as principais ameaças ao sistema baseadas no modelo de negócio e arquitetura proposta. Para cada ameaça identificada, sugira controles de mitigação específicos que devem ser implementados na arquitetura.

    - **Estratégia de Secrets Management:** Defina como dados sensíveis (chaves de API, senhas de banco, certificados) serão armazenados, rotacionados e acessados em diferentes ambientes. Especifique se será usado um serviço dedicado (ex: HashiCorp Vault, AWS Secrets Manager) ou variáveis de ambiente criptografadas.

    - **Compliance Framework (se aplicável):** Se o projeto está sujeito a regulamentações específicas (LGPD, PCI DSS, SOX, HIPAA), detalhe os controles arquiteturais necessários para conformidade, incluindo:

      - Estratégia de auditoria e logs de compliance
      - Controles de acesso baseados em papéis (RBAC) granulares
      - Criptografia de dados em repouso e em trânsito
      - Políticas de retenção e purga de dados

    - **Security by Design:** Descreva como os princípios de segurança serão incorporados desde o design inicial, incluindo validação de entrada, sanitização de dados, princípio do menor privilégio e defesa em profundidade.

20. **Justificativas e Trade-offs:** Breve explicação das principais decisões arquiteturais e por que alternativas foram descartadas (se relevante).
21. **Exemplo de Bootstrapping/Inicialização (se aplicável e útil para clareza):** Um pequeno trecho de código exemplo (conceitual, como um `main.py` simplificado) demonstrando como os principais serviços seriam instanciados e configurados, especialmente focando em como as configurações são injetadas (via `__init__` ou métodos `configure()`).
22. **Estratégia de Evolução do Blueprint:** Para projetos de longo prazo, defina como o próprio blueprint arquitetural será versionado e evoluído. A descrição deve incluir:

    - **Versionamento Semântico do Blueprint:** Estabeleça uma convenção para versionar o blueprint (ex: v1.0.0 para a arquitetura inicial, v1.1.0 para adições de componentes, v2.0.0 para mudanças breaking na arquitetura).

    - **Processo de Evolução Arquitetural:** Defina o processo para propor, avaliar e implementar mudanças arquiteturais significativas, incluindo:

      - Critérios para determinar quando uma mudança requer nova versão do blueprint
      - Processo de validação de impacto em componentes existentes
      - Estratégia de migração para mudanças breaking

    - **Documentação de Decisões Arquiteturais (ADRs):** Estabeleça o formato e processo para documentar decisões arquiteturais importantes, suas justificativas e trade-offs, criando um histórico de evolução do sistema.

    - **Compatibilidade e Deprecação:** Defina políticas para manter compatibilidade entre versões e processo de deprecação de componentes ou interfaces obsoletas.

23. **Métricas de Qualidade e Quality Gates:** Defina métricas objetivas de qualidade e os gates de qualidade que devem ser aplicados para garantir consistência e excelência técnica. A descrição deve incluir:

    - **Métricas de Cobertura de Código:** Estabeleça metas específicas de cobertura (ex: mínimo 80% para lógica de negócio, 95% para componentes críticos de segurança). Defina quais tipos de código podem ser excluídos da cobertura (ex: código gerado, interfaces de terceiros).

    - **Métricas de Complexidade:** Defina limites para complexidade ciclomática (ex: máximo 10 por função), profundidade de aninhamento (ex: máximo 4 níveis) e tamanho de funções/classes. Especifique as ferramentas que serão usadas para medir essas métricas.

    - **Quality Gates Automatizados:** Defina os critérios objetivos que devem ser atendidos para que código seja aceito em produção:

      - Cobertura de testes acima do limite definido
      - Zero vulnerabilidades de segurança de alta severidade
      - Complexidade dentro dos limites estabelecidos
      - Todos os testes passando
      - Conformidade com padrões de código (linting)

    - **Métricas de Performance:** Para componentes críticos, defina benchmarks de performance que devem ser mantidos (ex: tempo de resposta de APIs, throughput de processamento, uso de memória).

24. **Análise de Riscos e Plano de Mitigação (Opcional - Recomendado para projetos críticos):** Para projetos de alta criticidade, compliance regulatório ou sistemas financeiros, forneça uma análise estruturada dos principais riscos técnicos e de negócio que podem impactar o projeto. Use uma matriz de riscos para priorização.

    **Formato sugerido:**

    | Categoria   | Risco Identificado                      | Probabilidade (1-5) | Impacto (1-5) | Score (P×I) | Estratégia de Mitigação    |
    | ----------- | --------------------------------------- | :-----------------: | :-----------: | :---------: | -------------------------- |
    | Técnico     | [Descrever risco técnico principal]     |        [1-5]        |     [1-5]     |    [P×I]    | [Plano de ação preventivo] |
    | Negócio     | [Descrever risco de negócio]            |        [1-5]        |     [1-5]     |    [P×I]    | [Plano de ação preventivo] |
    | Segurança   | [Descrever risco de segurança]          |        [1-5]        |     [1-5]     |    [P×I]    | [Plano de ação preventivo] |
    | Performance | [Descrever risco de performance/escala] |        [1-5]        |     [1-5]     |    [P×I]    | [Plano de ação preventivo] |

    **Legendas:**

    - **Probabilidade:** 1=Muito Baixa, 2=Baixa, 3=Média, 4=Alta, 5=Muito Alta
    - **Impacto:** 1=Insignificante, 2=Menor, 3=Moderado, 4=Maior, 5=Catastrófico
    - **Score:** Multiplicação para priorização (scores ≥12 são críticos)

    **Nota:** Foque nos 3-5 riscos mais relevantes. Esta análise deve ser revisada e atualizada periodicamente durante o projeto.
