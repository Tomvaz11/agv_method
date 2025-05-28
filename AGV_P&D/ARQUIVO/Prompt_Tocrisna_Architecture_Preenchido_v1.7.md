# AGV Prompt Template: Tocrisna v1.7 - Definição da Arquitetura Técnica

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

## Resultado Esperado (Blueprint Arquitetural):
Um documento (preferencialmente em Markdown) descrevendo a arquitetura proposta, incluindo:

1.  **Visão Geral da Arquitetura:** Um breve resumo da abordagem arquitetural escolhida (ex: Arquitetura em Camadas, Microsserviços simples, Baseada em Eventos, etc.)  e uma justificativa.
2.  **Diagrama de Componentes (Simplificado):** Um diagrama de blocos mostrando os principais módulos/componentes e suas interconexões.
3.  **Descrição dos Componentes/Módulos:** 
    -   Para cada componente principal:
        -   Nome claro (ex: `fotix.core.duplicate_finder`).
        -   Responsabilidade principal.
        -   Tecnologias chave da stack que serão usadas nele.
        -   **Dependências Diretas (Lista explícita - Diretriz 4).**
    -   Para a Camada de Apresentação (UI) (ex: `fotix.ui`):**
        -   Além da descrição geral da UI, **proponha uma decomposição em principais Telas/Views ou Componentes de UI reutilizáveis significativos.**
        -   Para cada Tela/View/Componente de UI proposto:
            -   Descreva brevemente seu propósito principal.
            -   Liste os principais serviços da Camada de Aplicação com os quais ele provavelmente interagirá.
            -   Sugira se sua implementação pode ser considerada uma unidade de trabalho relativamente independente.
4.  **Definição das Interfaces Principais:** Detalhamento dos contratos de comunicação entre os componentes chave (conforme Diretriz 3).
5.  **Gerenciamento de Dados (se aplicável):** Como os dados serão persistidos e acessados (ex: Módulo data_access usando SQLAlchemy com padrão Repository).
6.  **Estrutura de Diretórios Proposta:** Uma sugestão inicial, **preferencialmente utilizando o layout `src` moderno** (com o código principal do pacote dentro de uma pasta `src/nome_do_pacote/`) para melhor organização e empacotamento, mostrando a organização das pastas e arquivos principais.
7.  **Considerações de Segurança:** Resumo dos princípios de segurança aplicados.
8.  **Justificativas e Trade-offs:** Breve explicação das principais decisões arquiteturais e por que alternativas foram descartadas (se relevante).