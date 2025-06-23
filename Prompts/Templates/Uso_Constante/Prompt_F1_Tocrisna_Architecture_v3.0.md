# AGV Prompt Template: Tocrisna v3.0 - Definição da Arquitetura Técnica

## Tarefa Principal:
Definir e documentar uma proposta de arquitetura técnica de alto nível para o projeto descrito abaixo. O foco deve ser na modularidade, clareza, manutenibilidade, e na definição clara dos principais componentes, suas interfaces de comunicação e suas dependências diretas.

## Contexto e Definições Iniciais do Projeto:

-   **Nome do Projeto:** `Fotix`

-   **Visão Geral / Objetivo Principal:**

    Aplicativo desktop desenvolvido em Python, com backend robusto e interface gráfica (GUI) completa, projetado para localizar e remover arquivos duplicados (idênticos) de imagens e vídeos em múltiplos diretórios e arquivos ZIP.
    O sistema analisa arquivos de mídia e, **somente ao identificar dois ou mais arquivos idênticos**, utiliza um algoritmo inteligente para decidir qual arquivo manter e qual remover, com base em critérios como maior resolução da imagem, data de criação mais antiga e estrutura do nome do arquivo (evitando cópias como "(1)", "cópia", etc.).
    A arquitetura é otimizada para grandes volumes de dados, utilizando processamento assíncrono, batching progressivo e execução paralela.
    O aplicativo também oferece sistema de backup e restauração para recuperação segura dos arquivos removidos.
    
-   **Funcionalidades Chave (Alto Nível):**
    - Análise de arquivos de mídia (imagens e vídeos) em diretórios e arquivos ZIP.
    - Identificação precisa de arquivos duplicados (idênticos) utilizando hashing.
    - Seleção automática do arquivo a ser mantido entre duplicatas com base em critérios objetivos.
    - Remoção segura de duplicatas com backup automático.
    - Recuperação fácil de arquivos removidos através do sistema de restauração.
    - Processamento otimizado para grandes volumes de dados com execução assíncrona, paralela e em lotes.
    - Interface gráfica intuitiva para configuração e acompanhamento.
    - Geração de logs detalhados e relatórios resumidos com estatísticas pós-processamento.

-   **Público Alvo / Ambiente de Uso:** `Usuários finais em desktop (Windows)`

-   **Stack Tecnológica Definida:**
    - **Linguagem Principal:** Python 3.10+
    - **GUI (Interface Gráfica):** PySide6 (Qt for Python) — framework moderno para criação de interfaces desktop nativas.
    - **Motor de Escaneamento de Duplicatas:** BLAKE3 + pré-filtragem por tamanho com `os.path.getsize` para otimização inicial.
    - **Manipulação de Arquivos e Sistema de Arquivos:** pathlib + shutil + send2trash (remoção segura) + concurrent.futures (execução paralela).
    - **Descompactação Otimizada:** stream-unzip para leitura e extração progressiva de arquivos ZIP.
    
-   **Requisitos Não Funcionais Iniciais:**
    - Capacidade de processar grandes volumes (100.000+ arquivos) sem travamentos.
    - Identificação rápida de duplicatas com uso eficiente de CPU, RAM e disco.
    - Backups automáticos para garantir segurança de dados.
    - GUI responsiva mesmo sob alta carga de processamento.
    - Compatibilidade garantida com Windows 10 ou superior.
    - Descompactação eficiente e rápida de grandes arquivos ZIP com baixo uso de memória.
    - Tratamento de erros em operações críticas de escrita e remoção.

-   **Principais Restrições:**
    - Suporte exclusivo para Windows na primeira versão.
    - Sem integração com bancos de dados externos.
    - Análise limitada a arquivos idêticos (sem similaridade perceptual).
    - Suporte apenas ao formato ZIP para arquivos compactados.
    - Sem sistema de atualização automática previsto na primeira versão.
    - Desempenho condicionado à capacidade de hardware local do usuário.

## Diretrizes e Princípios Arquiteturais (Filosofia AGV):
1.  **Modularidade e Separação de Responsabilidades (SRP):** Proponha uma divisão clara em módulos/componentes lógicos, cada um com uma responsabilidade bem definida. Minimize o acoplamento entre eles e maximize a coesão interna.
2.  **Clareza e Manutenibilidade:** A arquitetura deve ser fácil de entender, manter e evoluir. Prefira soluções mais simples (KISS) quando apropriado.
3.  **Definição Explícita de Interfaces e Construção de Componentes:** **CRUCIAL:**
    *   **Interfaces de Serviço (Contratos Funcionais):** Para os principais pontos de interação entre os módulos identificados, defina claramente as interfaces (contratos) que eles expõem ou consomem.
        *   **Abstração da Infraestrutura:** Isto inclui, obrigatoriamente, abstrair interações com a infraestrutura. Prefira definir componentes wrapper (ex: `FileSystemService`, `ConcurrencyService`, `BackupService`) na camada de infraestrutura com interfaces claras, em vez de usar bibliotecas de baixo nível (como `pathlib`, `shutil`, `concurrent.futures`) diretamente nas camadas superiores (Core, Application) onde possível.
        *   A definição da interface de serviço deve incluir:
            *   Assinaturas de funções/métodos públicos chave (com tipos de parâmetros e retorno).
            *   Estruturas de dados (Dataclasses, Pydantic Models) usadas para troca de informações através desses métodos.
            *   Uma breve descrição do propósito de cada método exposto.
    *   **Configuração e Construção de Componentes:** Para cada componente/serviço principal proposto (especialmente aqueles que não são puramente modelos de dados):
        *   Se o componente depender de valores de configuração externos essenciais para seu funcionamento (ex: caminhos de arquivo padrão, URLs de API, chaves secretas, níveis de log, etc.), **indique explicitamente como esses valores de configuração seriam fornecidos ao componente em sua inicialização.**
        *   **Priorize a passagem de parâmetros de configuração através do construtor (`__init__`) do componente.** Detalhe os parâmetros de configuração chave que o construtor deve aceitar.
        *   Se, alternativamente, a configuração for obtida de um serviço de configuração centralizado ou por um método de configuração dedicado, mencione essa abordagem e a interface relevante.
        *   O objetivo é garantir que o blueprint deixe claro como os componentes são instanciados com suas configurações necessárias, promovendo desacoplamento e testabilidade.
4.  **Listagem Explícita de Dependências Diretas:** **IMPORTANTE:** Para cada componente/módulo principal descrito, liste explicitamente os **outros arquivos `.py` ou módulos específicos** dos quais ele depende diretamente para importar e usar funcionalidades. Use caminhos relativos à raiz do projeto (ex: `fotix.domain.models`, `utils.helpers`).
5.  **Testabilidade:** A arquitetura deve facilitar a escrita de testes unitários e de integração (ex: permitir injeção de dependência onde fizer sentido).
6.  **Segurança Fundamental:** Incorpore princípios básicos de segurança desde o design (ex: onde a validação de input deve ocorrer, como dados sensíveis podem ser tratados – sugerir hashing/criptografia, necessidade de autenticação/autorização).
7.  **Aderência à Stack:** Utilize primariamente as tecnologias definidas na Stack Tecnológica. Se sugerir uma tecnologia *adicional*, justifique claramente a necessidade.
8.  **Padrões de Design:** Sugira e aplique padrões de design relevantes (ex: Repository, Service Layer, Observer, Strategy, etc.) onde eles agregarem valor à estrutura e manutenibilidade. Justifique brevemente a escolha.
9.  **Escalabilidade (Básica):** Considere como a arquitetura pode suportar um crescimento moderado no futuro (ex: design sem estado para serviços, possibilidade de paralelizar tarefas usando `concurrent.futures`).
10. **Especificação de Tecnologias para Tipos de Componentes:** Para garantir consistência e aderência à stack definida, ao descrever os componentes/módulos, você DEVE especificar a tecnologia ou biblioteca principal a ser utilizada para certos tipos de artefatos, quando aplicável e relevante para a arquitetura. Por exemplo:
    *   **Modelos de Dados (DTOs, entidades de domínio, configurações):** Especificar o uso de **Pydantic `BaseModel`** como a tecnologia padrão para sua definição, visando validação de dados e facilidades de serialização.
    *   **Camada de Acesso a Dados (se houver BD):** Especificar o ORM (ex: SQLAlchemy) ou a biblioteca de acesso.
    *   **APIs Web (se houver):** Especificar o framework (ex: FastAPI, Flask).
    *   **Interface de Usuário (se houver):** Especificar o framework de UI (ex: PySide6).
    *   (Adicionar outros tipos de componentes/tecnologias conforme a necessidade do projeto).
Estas especificações devem constar na descrição de cada componente relevante no Blueprint Arquitetural.

## Resultado Esperado (Blueprint Arquitetural):
Um documento (preferencialmente em Markdown) descrevendo a arquitetura proposta, incluindo:

1.  **Visão Geral da Arquitetura:** Um breve resumo da abordagem arquitetural escolhida (ex: Arquitetura em Camadas, Microsserviços simples, Baseada em Eventos, etc.) e uma justificativa.
2.  **Diagrama de Componentes (Simplificado):** Um diagrama de blocos mostrando os principais módulos/componentes e suas interconexões.
3.  **Descrição dos Componentes, Interfaces e Modelos de Domínio:** 
    -   Para cada componente principal:
        -   Nome claro (ex: `fotix.core.duplicate_finder`).
        -   Responsabilidade principal.
        -   **Tecnologias Chave da Stack que Serão Usadas Nele:** Conforme a Diretriz 10 ("Especificação de Tecnologias para Tipos de Componentes"), indique a biblioteca ou framework principal para este componente (ex: "Pydantic `BaseModel`" para módulos de modelos de dados; "PySide6" para componentes de UI; "FastAPI" para um serviço de API; `logging` stdlib para um serviço de logging, etc.). Se for apenas lógica Python pura sem uma biblioteca externa dominante, indique "Python (Lógica Pura)".
        -   **Dependências Diretas (Lista explícita - Diretriz 4).**

    -   **3.1. Consistência dos Modelos de Dados (SSOT do Domínio):**
        -   Defina todos os seus modelos de dados principais (DTOs, entidades de domínio, etc.) em uma única seção dedicada (ex: "Camada de Domínio/Core - Models"). **Esta seção é a Fonte Única da Verdade (SSOT) para todas as estruturas de dados do projeto.**
        -   Ao definir as interfaces na Seção 4, os tipos de retorno e os parâmetros que forem objetos complexos **DEVEM OBRIGATORIAMENTE** referenciar os modelos definidos nesta seção "Models" (a SSOT do Domínio).
        -   Se um componente (como um serviço de infraestrutura) lida com uma fonte de dados externa (ex: uma API, metadados de um arquivo ZIP) que não corresponde exatamente ao modelo de domínio canônico, a **"Responsabilidade Principal"** desse componente deve incluir explicitamente a tarefa de **"mapear" ou "traduzir" os dados da fonte para o modelo de domínio oficial**. O Blueprint não deve criar um modelo de dados duplicado ou divergente para acomodar a fonte externa.

    -   Para a Camada de Apresentação (UI) (ex: `fotix.ui`):**
        -   Além da descrição geral da UI, **proponha uma decomposição em principais Telas/Views ou Componentes de UI reutilizáveis significativos.**
        -   Para cada Tela/View/Componente de UI proposto:
            -   Descreva brevemente seu propósito principal.
            -   Liste os principais serviços da Camada de Aplicação com os quais ele provavelmente interagirá.
            -   Sugira se sua implementação pode ser considerada uma unidade de trabalho relativamente independente.
4.  **Definição das Interfaces Principais:** Detalhamento dos contratos de comunicação entre os componentes chave (conforme Diretriz 3), incluindo como os componentes recebem suas configurações iniciais (priorizando `__init__`).
5.  **Gerenciamento de Dados (se aplicável):** Como os dados serão persistidos e acessados (ex: Módulo data_access usando SQLAlchemy com padrão Repository, ou especificando Pydantic `BaseModel` para modelos de dados se não houver persistência complexa).
6.  **Estrutura de Diretórios Proposta:** Uma sugestão inicial, **preferencialmente utilizando o layout `src` moderno** (com o código principal do pacote dentro de uma pasta `src/nome_do_pacote/`) para melhor organização e empacotamento, mostrando a organização das pastas e arquivos principais.
7.  **Arquivo `.gitignore` Proposto:** Um conteúdo sugerido, **completo e pronto para uso**, para o arquivo `.gitignore` na raiz do projeto, apropriado para a "Stack Tecnológica Definida". Ele deve ser abrangente, cobrindo caches, ambientes virtuais, arquivos de IDEs comuns (VS Code, PyCharm), e arquivos específicos do SO.
8.  **Arquivo `README.md` Proposto:** A geração do **conteúdo completo** para um arquivo `README.md` inicial e profissional. O README deve seguir uma estrutura padrão, contendo, no mínimo:
    *   O nome do projeto e uma descrição concisa.
    *   Badges de status (pode usar placeholders).
    *   Seção "Sobre o Projeto".
    *   Seção "Stack Tecnológica".
    *   Seção "Como Começar" (com instruções para instalar dependências e rodar o projeto).
    *   Seção "Como Executar os Testes".
    *   Seção "Estrutura do Projeto" (uma breve explicação das pastas principais).
9.  **Arquivo `LICENSE` Proposto:** Uma sugestão de licença de software (ex: MIT, Apache 2.0) e a geração do **texto completo** correspondente para o arquivo `LICENSE` na raiz do projeto. Se nenhuma for especificada, sugira a MIT como um padrão seguro.
10. **Arquivo `CONTRIBUTING.md` Proposto:** A geração de um **template de conteúdo** para o `CONTRIBUTING.md`, descrevendo como contribuir para um projeto que segue o Método AGV (ex: seguir o blueprint, garantir testes, etc.).
11. **Estrutura do `CHANGELOG.md`:** A geração de um arquivo `CHANGELOG.md` inicial, contendo apenas a estrutura padrão (ex: `## [Unreleased]`, `## [0.1.0] - YYYY-MM-DD`) para ser preenchido futuramente.
12.  **Considerações de Segurança:** Resumo dos princípios de segurança aplicados.
13.  **Justificativas e Trade-offs:** Breve explicação das principais decisões arquiteturais e por que alternativas foram descartadas (se relevante).
14. **Exemplo de Bootstrapping/Inicialização (se aplicável e útil para clareza):** Um pequeno trecho de código exemplo (conceitual, como um `main.py` simplificado) demonstrando como os principais serviços seriam instanciados e configurados, especialmente focando em como as configurações são injetadas (via `__init__` ou métodos `configure()`).