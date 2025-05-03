# AGV Prompt Template: ValidadorCruzado v1.0 - Validação de Preenchimento de Prompt

**Tarefa Principal:** Validar a precisão e completude do prompt AGV preenchido (`Prompt_Severino_Preenchido.md`) em relação aos seus documentos fonte originais (`Output_Tocrisna_Architecture_v1.0.md` e `Prompt_Tocrisna_Architecture_v1.0.md`).

**Contexto:** Uma IA ("Preenchedor") foi usada para preencher um template de prompt AGV (`Prompt_Severino_EspeciFi_v1.1.md`) usando os documentos fonte listados. Sua tarefa é atuar como um revisor independente para garantir que o preenchimento foi feito corretamente, sem omissões, alucinações ou interpretações errôneas.

**Arquivos para Análise:**

1.  **Prompt Preenchido (a ser validado):**
    ```markdown
    # --- Conteúdo de [Prompt_Severino_Preenchido.md] ---
    # --- Conteúdo de [Prompt_Severino_EspeciFi_v1.1.md] ---
---

# AGV Prompt Template: Severino v1.1 - Especificação Funcional Detalhada

**Tarefa Principal:** Detalhar a especificação técnica para a funcionalidade/módulo descrito na seção **"Descrição de Alto Nível da Funcionalidade (Fornecida por Você)"** abaixo, baseando-se estritamente no contexto arquitetural fornecido. O resultado deve ser formatado de forma clara e precisa, pronto para ser usado na seção "Especificação da Funcionalidade/Módulo a ser Implementada" do prompt do agente Tocle.

**Contexto do Projeto e Arquitetura (Definido por Fases Anteriores):**

*   **Nome do Projeto:** `Fotix`
*   **Objetivo Geral do Projeto:** Aplicativo desktop para localizar e remover arquivos duplicados (imagens/vídeos) em diretórios e ZIPs, selecionando automaticamente qual manter com base em critérios (resolução, data, nome), com backup e restauração, otimizado para grandes volumes.
*   **Blueprint Arquitetural Relevante (Extraído do Output da Tocrisna):**
    *   **Módulo/Arquivo Alvo desta Especificação:** `fotix/src/fotix/core/decision_logic.py`
    *   **Principais Responsabilidades deste Módulo/Arquivo (Conforme Arquitetura):** Implementar o algoritmo de decisão para escolher qual arquivo manter dentro de um grupo de duplicatas, baseado em regras de negócio (resolução, data, nome, etc.).
    *   **Dependências Diretas deste Módulo (Conforme Arquitetura):**
        *   `fotix.domain.models` (para as estruturas de dados `FileMetadata`, `DuplicateGroup`)
    *   **Interfaces de Dependências (Contratos a serem Usados por este Módulo):**
        *   `[Nenhuma interface de serviço externo explicitamente chamada por este módulo, conforme a arquitetura.]` (O módulo opera sobre os dados recebidos como parâmetros).
    *   **Interfaces Expostas (Contratos Fornecidos por este Módulo):**
        *   `decide_file_to_keep(group: DuplicateGroup) -> FileMetadata`: Aplica as regras de negócio (resolução, data, nome) para selecionar o melhor arquivo dentro de um grupo de duplicatas.
    *   **Estruturas de Dados Relevantes (Definidas pela Arquitetura):**
        ```python
        from dataclasses import dataclass, field
        from pathlib import Path
        from typing import List, Dict, Optional, Iterator

        @dataclass(frozen=True)
        class FileMetadata:
            path: Path
            size: int
            creation_time: float # Timestamp UTC
            # Potencialmente outros metadados úteis para decisão (resolução, etc. - a serem extraídos seletivamente)
            # hash: Optional[str] = None # Preenchido durante o processamento

        @dataclass
        class DuplicateGroup:
            files: List[FileMetadata] # Lista de arquivos idênticos
            file_to_keep: Optional[FileMetadata] = None # Decidido pelo Core
            hash_value: str # Hash que identifica o grupo
        ```

**Descrição de Alto Nível da Funcionalidade (Fornecida por Você):** **<<< INPUT HUMANO ESSENCIAL >>>**

[COLE AQUI SUA DESCRIÇÃO EM LINGUAGEM NATURAL E CLARA DO QUE ESTA FUNCIONALIDADE ESPECÍFICA DEVE FAZER. SEJA O MAIS CLARO POSSÍVEL SOBRE O OBJETIVO.
Exemplo: "Preciso que o DecisionEngine (implementado em decision_logic.py), ao receber um DuplicateGroup, escolha qual FileMetadata manter. O critério principal é a maior resolução (largura * altura). Se houver empate na resolução, o critério secundário é a data de modificação mais recente. Se ainda houver empate, o critério terciário é o nome de arquivo mais curto. Retornar o FileMetadata escolhido."]

**Diretrizes para Geração da Especificação:**

1.  **Base na Descrição de Alto Nível:** A especificação deve implementar fielmente a funcionalidade descrita por você acima.
2.  **Clareza e Precisão:** A especificação deve ser inequívoca e fácil de entender por um desenvolvedor (ou pelo agente Tocle).
3.  **Detalhamento:** Descreva os passos lógicos necessários para implementar a funcionalidade.
4.  **Referência às Interfaces:** Quando o processamento envolver a interação com outros módulos, refira-se explicitamente às interfaces listadas no "Contexto Arquitetural". (Neste caso, focar na interface exposta e nas estruturas de dados).
5.  **Inputs e Outputs:** Detalhe claramente os inputs esperados (parâmetros: `DuplicateGroup`, tipos de dados: definidos em `fotix.domain.models`) e os outputs (valor de retorno: `FileMetadata`).
6.  **Regras de Negócio:** Incorpore todas as regras de negócio mencionadas na descrição de alto nível (ex: critérios de resolução, data, nome).
7.  **Tratamento de Erros:** Especifique os principais cenários de erro razoáveis para a funcionalidade descrita e como devem ser tratados (ex: o que fazer se o `DuplicateGroup` estiver vazio ou contiver menos de dois arquivos? O que fazer se os metadados necessários para a decisão estiverem faltando em alguns arquivos?). Sugira exceções apropriadas (ex: `ValueError`).
8.  **Casos de Borda:** Mencione casos de borda óbvios (ex: grupo com apenas dois arquivos, todos os arquivos com metadados idênticos segundo os critérios, arquivos sem metadados de resolução/data).
9.  **Formato Adequado:** Use linguagem clara, listas ou passos numerados. A saída deve ser adequada para colar diretamente na seção "Especificação..." do `Prompt_Tocle`.

**Resultado Esperado:**

Um bloco de texto contendo a **Especificação Técnica Detalhada** da funcionalidade, pronta para ser usada no prompt do Tocle, detalhando inputs, passos lógicos (referenciando interfaces), outputs, regras de negócio, tratamento de erro e casos de borda, **baseado na descrição de alto nível fornecida**.

---

Pronto! Este é o `Prompt_Severino_EspeciFi_v1.1.md`. Ele atua como a ponte entre sua visão funcional de alto nível e as instruções técnicas detalhadas que o Tocle precisa, sempre respeitando a arquitetura definida pela Tocrisna.

Este prompt é crucial para traduzir seus requisitos de alto nível em especificações técnicas acionáveis para o Tocle, usando o contexto da arquitetura definida pela Tocrisna.
    ```

2.  **Template Original (para referência da estrutura):**
    ```markdown
    # --- Conteúdo de [Prompt_Severino_EspeciFi_v1.1.md] ---
---

# AGV Prompt Template: Severino v1.1 - Especificação Funcional Detalhada

**Tarefa Principal:** Detalhar a especificação técnica para a funcionalidade/módulo descrito na seção **"Descrição de Alto Nível da Funcionalidade (Fornecida por Você)"** abaixo, baseando-se estritamente no contexto arquitetural fornecido. O resultado deve ser formatado de forma clara e precisa, pronto para ser usado na seção "Especificação da Funcionalidade/Módulo a ser Implementada" do prompt do agente Tocle.

**Contexto do Projeto e Arquitetura (Definido por Fases Anteriores):**

*   **Nome do Projeto:** `[NOME_DO_PROJETO]`
*   **Objetivo Geral do Projeto:** `[BREVE DESCRIÇÃO DO PROPÓSITO GERAL DO PROJETO]`
*   **Blueprint Arquitetural Relevante (Extraído do Output da Tocrisna):**
    *   **Módulo/Arquivo Alvo desta Especificação:** `[CAMINHO/COMPLETO/DO/ARQUIVO_ALVO.py]`
    *   **Principais Responsabilidades deste Módulo/Arquivo (Conforme Arquitetura):** `[COPIAR DESCRIÇÃO DA RESPONSABILIDADE DO BLUEPRINT]`
    *   **Dependências Diretas deste Módulo (Conforme Arquitetura):**
        *   `[COPIAR A LISTA EXPLÍCITA DE DEPENDÊNCIAS DIRETAS DO BLUEPRINT. Ex:]`
        *   `fotix.domain.models`
        *   `utils.helpers`
    *   **Interfaces de Dependências (Contratos a serem Usados por este Módulo):**
        *   `[COPIAR AS INTERFACES RELEVANTES DO BLUEPRINT - Assinaturas e descrições das funções/métodos de outros módulos que este precisa chamar. Ex:]`
        *   `utils.helpers.calcular_hash(file_path: Path) -> str`
        *   `core.database.UserRepository.get_user_by_id(user_id: int) -> Optional[User]`
    *   **Interfaces Expostas (Contratos Fornecidos por este Módulo):**
        *   `[COPIAR AS INTERFACES RELEVANTES DO BLUEPRINT - Assinaturas e descrições das funções/métodos públicos que este módulo deve expor. Ex:]`
        *   `Classe 'DuplicateDetector' com método público 'find_duplicates(directory_path: Path) -> Dict[str, List[Path]]'`
    *   **Estruturas de Dados Relevantes (Definidas pela Arquitetura):** `[COPIAR DEFINIÇÕES DE DATACLASSES/NAMEDTUPLES RELEVANTES DO BLUEPRINT]`

**Descrição de Alto Nível da Funcionalidade (Fornecida por Você):** **<<< INPUT HUMANO ESSENCIAL >>>**

[COLE AQUI SUA DESCRIÇÃO EM LINGUAGEM NATURAL E CLARA DO QUE ESTA FUNCIONALIDADE ESPECÍFICA DEVE FAZER. SEJA O MAIS CLARO POSSÍVEL SOBRE O OBJETIVO.
Exemplo: "Preciso que o DecisionEngine, ao receber um DuplicateGroup, escolha qual FileMetadata manter. O critério principal é a maior resolução (largura * altura). Se houver empate na resolução, o critério secundário é a data de modificação mais recente. Retornar o FileMetadata escolhido."]

**Diretrizes para Geração da Especificação:**

1.  **Base na Descrição de Alto Nível:** A especificação deve implementar fielmente a funcionalidade descrita por você acima.
2.  **Clareza e Precisão:** A especificação deve ser inequívoca e fácil de entender por um desenvolvedor (ou pelo agente Tocle).
3.  **Detalhamento:** Descreva os passos lógicos necessários para implementar a funcionalidade.
4.  **Referência às Interfaces:** Quando o processamento envolver a interação com outros módulos, refira-se explicitamente às interfaces listadas no "Contexto Arquitetural".
5.  **Inputs e Outputs:** Detalhe claramente os inputs esperados (parâmetros, tipos de dados, baseados nas interfaces expostas/consumidas) e os outputs (valores de retorno, tipos, efeitos colaterais).
6.  **Regras de Negócio:** Incorpore todas as regras de negócio mencionadas na descrição de alto nível (ex: "ignorar arquivos < 1KB").
7.  **Tratamento de Erros:** Especifique os principais cenários de erro razoáveis para a funcionalidade descrita e como devem ser tratados (ex: o que fazer se o grupo de duplicatas estiver vazio ou contiver dados inválidos?). Sugira exceções apropriadas.
8.  **Casos de Borda:** Mencione casos de borda óbvios (ex: grupo com um só arquivo? grupo com arquivos sem metadados de resolução?).
9.  **Formato Adequado:** Use linguagem clara, listas ou passos numerados. A saída deve ser adequada para colar diretamente na seção "Especificação..." do `Prompt_Tocle`.

**Resultado Esperado:**

Um bloco de texto contendo a **Especificação Técnica Detalhada** da funcionalidade, pronta para ser usada no prompt do Tocle, detalhando inputs, passos lógicos (referenciando interfaces), outputs, regras de negócio, tratamento de erro e casos de borda, **baseado na descrição de alto nível fornecida**.

---

Pronto! Este é o `Prompt_Severino_EspeciFi_v1.0.md`. Ele atua como a ponte entre sua visão funcional de alto nível e as instruções técnicas detalhadas que o Tocle precisa, sempre respeitando a arquitetura definida pela Tocrisna.

Este prompt é crucial para traduzir seus requisitos de alto nível em especificações técnicas acionáveis para o Tocle, usando o contexto da arquitetura definida pela Tocrisna.
    ```

3.  **Documentos Fonte (usados para preencher):**
    ```markdown
    # --- Conteúdo de [Output_Tocrisna_Architecture_v1.0.md] ---
    # Proposta de Arquitetura Técnica: Fotix v1.0

**Documento Preparado Por:** Tocrisna (Agente Arquiteta de Software)
**Versão:** 1.0
**Data:** 2024-08-28

## 1. Visão Geral da Arquitetura

A arquitetura proposta para o `Fotix` é uma **Arquitetura em Camadas (Layered Architecture)** com forte separação de responsabilidades. Esta abordagem foi escolhida por sua clareza, manutenibilidade e testabilidade, adequadas para uma aplicação desktop com funcionalidades bem definidas.

As camadas principais são:

1.  **Camada de Apresentação (GUI):** Responsável pela interface com o usuário.
2.  **Camada de Aplicação (Serviços):** Orquestra os casos de uso, atuando como fachada para o núcleo.
3.  **Camada de Núcleo (Core/Domain):** Contém a lógica de negócio principal (identificação de duplicatas, regras de decisão).
4.  **Camada de Infraestrutura:** Lida com preocupações transversais como acesso ao sistema de arquivos, paralelismo, logging e persistência de backups.

**Justificativa:**
*   **Modularidade:** Separa claramente a interface do usuário, a lógica de negócio e o acesso a recursos externos (sistema de arquivos, etc.).
*   **Manutenibilidade:** Alterações na GUI não devem impactar o Core, e vice-versa. Novas fontes de arquivos (ex: outros formatos compactados no futuro) podem ser adicionadas na Infraestrutura sem afetar o Core.
*   **Testabilidade:** Cada camada pode ser testada isoladamente. O Core, sendo independente de UI e I/O direto, é altamente testável unitariamente. A Camada de Aplicação pode ser testada com mocks da Infraestrutura e do Core.
*   **Clareza:** Facilita o entendimento do fluxo de dados e responsabilidades.
*   **GUI Responsiva:** Permite que as operações intensivas (Core e Infraestrutura) rodem em threads/processos separados, mantendo a GUI (Apresentação) responsiva.

## 2. Diagrama de Componentes (Simplificado - Descrição Textual)

```
+-----------------------+      +--------------------------+      +---------------------+      +------------------------+
|   Apresentação (GUI)  |<---->|  Aplicação (Serviços)    |<---->|   Núcleo (Core)     |<---->| Infraestrutura         |
|-----------------------|      |--------------------------|      |---------------------|      |------------------------|
| - PySide6 (Views)     |      | - Orquestração Casos Uso |      | - Lógica Duplicatas |      | - FileSystemService    |
| - ViewModels (Qt)     |      | - Gerencia Estado Scan   |      | - Algoritmo Decisão |      | - ZipHandlingService   |
| - Interação Usuário   |      | - Fachada p/ GUI         |      | - Hashing (BLAKE3)  |      | - ConcurrencyManager   |
| - Signals/Slots       |----->| - Comunicação Async GUI <------| - Estruturas Dados  |      | - BackupRestoreService |
+-----------------------+      +--------------------------+      +---------------------+      | - LoggingService       |
                                                                                            | - (pathlib, shutil,    |
                                                                                            |  send2trash,           |
                                                                                            |  stream-unzip,         |
                                                                                            |  concurrent.futures)   |
                                                                                            +------------------------+
        ^                                                                                            ^
        |                                                                                            |
        +----------------------------------------- Utilidades (`utils`) -----------------------------+
                                             (Funções Comuns, Constantes, etc.)
```

**Fluxo Principal (Exemplo: Scan):**
GUI -> Aplicação (inicia scan) -> Infraestrutura (lista arquivos) -> Core (pré-filtra, hash) -> Infraestrutura (lê arquivos p/ hash) -> Core (compara hashes, agrupa) -> Aplicação (recebe resultados) -> GUI (exibe resultados)

## 3. Descrição dos Componentes/Módulos

1.  **`fotix.gui` (Apresentação)**
    *   **Responsabilidade:** Renderizar a interface gráfica, capturar entradas do usuário (seleção de diretórios, configurações), exibir o progresso e os resultados do escaneamento, permitir ações sobre os resultados (exclusão, restauração).
    *   **Tecnologias:** PySide6 (Qt for Python).
    *   **Interação:** Comunica-se *exclusivamente* com a camada `fotix.application` através de chamadas de método e recebe atualizações via Signals/Slots do Qt (ou um mecanismo similar de callback/fila) para manter a responsividade.

2.  **`fotix.application` (Aplicação/Serviços)**
    *   **Responsabilidade:** Orquestrar os fluxos de trabalho (casos de uso). Atua como uma fachada entre a GUI e o Core/Infraestrutura. Gerencia o estado geral da aplicação (ex: scan em andamento, resultados carregados). Inicia tarefas em background (usando `ConcurrencyManager` da Infraestrutura) e coordena a comunicação assíncrona de volta para a GUI (progresso, resultados, erros).
    *   **Tecnologias:** Python puro, `dataclasses`/`pydantic`.
    *   **Interação:** Chamado pela `gui`. Chama métodos do `core` para lógica de negócio e da `infrastructure` para operações de I/O, paralelismo e outras preocupações externas.

3.  **`fotix.core` (Núcleo/Domain)**
    *   **Responsabilidade:** Implementar a lógica central de identificação de duplicatas. Contém o algoritmo de hashing (usando BLAKE3), a lógica de comparação, a estratégia de pré-filtragem por tamanho, e o algoritmo de decisão para escolher qual arquivo manter. Define as estruturas de dados canônicas para representar arquivos, duplicatas e resultados. **Deve ser independente de UI e I/O direto.**
    *   **Tecnologias:** Python puro, BLAKE3 (via biblioteca), `dataclasses`/`pydantic`.
    *   **Interação:** Chamado pela `application`. Pode solicitar dados de arquivos (ex: stream de bytes para hashing) através de interfaces implementadas pela `infrastructure`, mas não acessa o sistema de arquivos diretamente.

4.  **`fotix.infrastructure` (Infraestrutura)**
    *   **Responsabilidade:** Lidar com todas as interações com o mundo exterior e preocupações transversais. Isso inclui:
        *   Acesso ao sistema de arquivos (listar diretórios, obter metadados, ler, mover, deletar arquivos).
        *   Manipulação de arquivos ZIP (leitura e extração otimizada).
        *   Gerenciamento de concorrência/paralelismo (pools de threads/processos).
        *   Operações de backup e restauração.
        *   Logging.
        *   (Opcional) Persistência de configuração.
    *   **Tecnologias:** `pathlib`, `shutil`, `os.path`, `send2trash`, `stream-unzip`, `concurrent.futures`, `logging`, Python puro.
    *   **Interação:** Chamado pela `application` para executar tarefas de I/O ou gerenciar concorrência. Implementa interfaces que podem ser usadas pelo `core` (ex: para obter dados de arquivos de forma abstrata).

5.  **`fotix.utils` (Utilidades)**
    *   **Responsabilidade:** Fornecer funções auxiliares, constantes, e talvez classes base ou decoradores usados por múltiplos módulos/camadas. Ex: formatação de tamanho de arquivo, setup inicial de logging.
    *   **Tecnologias:** Python puro.
    *   **Interação:** Usado por qualquer outra camada conforme necessário.

## 4. Definição das Interfaces Principais (Contratos entre Camadas)

Usaremos `dataclasses` ou `pydantic` para definir estruturas de dados claras.

**Estruturas de Dados Chave:**

```python
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Iterator

@dataclass(frozen=True)
class FileMetadata:
    path: Path
    size: int
    creation_time: float # Timestamp UTC
    # Potencialmente outros metadados úteis para decisão (resolução, etc. - a serem extraídos seletivamente)
    # hash: Optional[str] = None # Preenchido durante o processamento

@dataclass
class ScanConfig:
    directories_to_scan: List[Path]
    include_zip_files: bool
    # Outras configurações (ex: filtros de extensão, tamanho mínimo/máximo)

@dataclass
class DuplicateGroup:
    files: List[FileMetadata] # Lista de arquivos idênticos
    file_to_keep: Optional[FileMetadata] = None # Decidido pelo Core
    hash_value: str # Hash que identifica o grupo

@dataclass
class ScanProgress:
    files_scanned: int
    duplicates_found: int
    current_phase: str # Ex: "Listing files", "Hashing", "Comparing"
    error_message: Optional[str] = None

@dataclass
class BackupInfo:
    original_path: Path
    backup_path: Path
    timestamp: float
```

**Interfaces (Assinaturas de Métodos Chave):**

*   **`fotix.application.ScanService` (Interface exposta para a `gui`)**
    *   `start_scan(config: ScanConfig) -> None`: Inicia um novo processo de scan em background. Dispara sinais/callbacks para progresso.
    *   `get_current_results() -> List[DuplicateGroup]`: Retorna os grupos de duplicatas encontrados até o momento (ou ao final).
    *   `process_deletions(groups: List[DuplicateGroup]) -> None`: Inicia o processo de backup e remoção dos arquivos marcados para exclusão (não os `file_to_keep`). Dispara sinais/callbacks para progresso/conclusão.
    *   `restore_from_backup(backup_info: BackupInfo) -> None`: Inicia a restauração de um arquivo.
    *   `get_backup_list() -> List[BackupInfo]`: Retorna a lista de backups disponíveis.
    *   *Sinais/Callbacks para GUI (Conceitual):* `progress_updated(progress: ScanProgress)`, `scan_completed(results: List[DuplicateGroup])`, `deletion_completed()`, `error_occurred(message: str)`

*   **`fotix.core.DuplicateFinder` (Interface usada pela `application`)**
    *   `find_duplicates(file_iterator: Iterator[FileMetadata], hash_function: callable) -> List[DuplicateGroup]`: Recebe um iterador de metadados de arquivos e uma função para obter o hash (fornecida via `infrastructure`), retorna os grupos de duplicatas. O processo interno envolve:
        1. Pré-filtragem por tamanho.
        2. Agrupamento por tamanho.
        3. Hashing (usando `hash_function`) apenas para grupos com mais de um arquivo.
        4. Comparação final por hash.
    *   `decide_file_to_keep(group: DuplicateGroup) -> FileMetadata`: Aplica as regras de negócio (resolução, data, nome) para selecionar o melhor arquivo dentro de um grupo de duplicatas.

*   **`fotix.infrastructure.FileSystemService` (Interface usada pela `application` e potencialmente pelo `core` via `application`)**
    *   `scan_directory_recursively(path: Path, include_zip: bool) -> Iterator[FileMetadata]`: Itera sobre arquivos em diretórios, retornando `FileMetadata` básico (sem hash). Delega a extração de ZIPs ao `ZipHandlingService`.
    *   `get_file_stream(path: Path) -> Iterator[bytes]`: Retorna um iterador/stream de bytes para um arquivo (usado para hashing pelo `core`).
    *   `move_file_to_trash(path: Path) -> None`: Move um arquivo para a lixeira do sistema de forma segura (usando `send2trash`).
    *   `get_file_metadata(path: Path) -> FileMetadata`: Obtém metadados detalhados de um arquivo (pode incluir extração de metadados de mídia se necessário para a decisão do `core`).

*   **`fotix.infrastructure.ZipHandlingService` (Interface usada pelo `FileSystemService`)**
    *   `stream_files_from_zip(zip_path: Path) -> Iterator[Tuple[str, Iterator[bytes], int]]`: Usa `stream-unzip` para iterar sobre os arquivos dentro de um ZIP, retornando o nome do arquivo interno, um iterador para seus bytes e seu tamanho, sem extrair tudo para o disco.

*   **`fotix.infrastructure.ConcurrencyManager` (Interface usada pela `application`)**
    *   `submit_cpu_bound_task(func: callable, *args, **kwargs) -> Future`: Submete uma tarefa intensiva em CPU (ex: hashing de múltiplos arquivos) para execução em um pool de processos (`ProcessPoolExecutor`).
    *   `submit_io_bound_task(func: callable, *args, **kwargs) -> Future`: Submete uma tarefa intensiva em I/O (ex: listar muitos arquivos, ler muitos arquivos pequenos) para execução em um pool de threads (`ThreadPoolExecutor`).

*   **`fotix.infrastructure.BackupRestoreService` (Interface usada pela `application`)**
    *   `backup_file(source_path: Path) -> BackupInfo`: Move o arquivo para um local de backup seguro e retorna informações sobre o backup.
    *   `restore_file(backup_info: BackupInfo) -> None`: Restaura um arquivo do backup para seu local original.
    *   `list_backups() -> List[BackupInfo]`: Lista os backups existentes.
    *   `purge_old_backups(days_threshold: int) -> None`: (Opcional) Remove backups antigos.

## 5. Gerenciamento de Dados

*   **Dados de Scan:** Mantidos em memória durante o processamento pela `application` e `core`, usando as `dataclasses` definidas. Os resultados finais são passados para a `gui`. Não há persistência dos resultados do scan entre sessões do aplicativo na v1.0.
*   **Backups:** Gerenciados pela `BackupRestoreService` na camada de `infrastructure`. Os arquivos removidos são movidos para um diretório de backup dedicado (configurável, ex: `AppData/Local/Fotix/Backup` ou similar), possivelmente com metadados adicionais (um pequeno arquivo de índice ou nomeando os backups de forma informativa).
*   **Logs:** Gerenciados pela `LoggingService` na `infrastructure`. Logs detalhados são escritos em arquivos (`AppData/Local/Fotix/Logs`), e relatórios resumidos podem ser gerados ao final do processo.
*   **Configuração:** Configurações simples (últimos diretórios usados, etc.) podem ser salvas em um arquivo de configuração (ex: INI, JSON) gerenciado pela `infrastructure`.

## 6. Estrutura de Diretórios Proposta

```
fotix/
├── src/
│   └── fotix/
│       ├── __init__.py
│       ├── main.py           # Ponto de entrada da aplicação
│       ├── gui/              # Camada de Apresentação (PySide6 Widgets, Views, ViewModels)
│       │   ├── __init__.py
│       │   ├── main_window.py
│       │   └── widgets/
│       ├── application/      # Camada de Aplicação (Serviços/Orquestração)
│       │   ├── __init__.py
│       │   └── scan_service.py
│       ├── core/             # Camada de Núcleo (Lógica de Negócio)
│       │   ├── __init__.py
│       │   ├── duplicate_finder.py
│       │   └── decision_logic.py
│       ├── infrastructure/   # Camada de Infraestrutura
│       │   ├── __init__.py
│       │   ├── file_system.py
│       │   ├── zip_handler.py
│       │   ├── concurrency.py
│       │   ├── backup.py
│       │   └── logging_setup.py
│       ├── domain/           # Estruturas de dados compartilhadas (Dataclasses/Pydantic) - Alternativa a colocá-las em 'core'
│       │   ├── __init__.py
│       │   └── models.py
│       └── utils/            # Utilidades
│           ├── __init__.py
│           └── helpers.py
├── tests/                  # Testes unitários e de integração
│   ├── __init__.py
│   ├── gui/
│   ├── application/
│   ├── core/
│   └── infrastructure/
├── data/                   # (Opcional) Dados de exemplo, recursos
├── docs/                   # Documentação
├── scripts/                # Scripts auxiliares (build, etc.)
├── requirements.txt        # Dependências
└── README.md
```

## 7. Considerações de Segurança

*   **Validação de Input:** A camada `gui` e `application` devem validar as entradas do usuário (ex: caminhos de diretório existem e são acessíveis).
*   **Operações de Arquivo Seguras:** Usar `send2trash` para exclusão minimiza o risco de perda acidental de dados. O sistema de backup é a principal salvaguarda.
*   **Tratamento de Erros:** Capturar exceções específicas de I/O (`FileNotFoundError`, `PermissionError`) na camada de `infrastructure` e reportá-las adequadamente para a `application` e `gui` para informar o usuário. Evitar falhas silenciosas em operações críticas (backup, delete).
*   **Permissões:** A aplicação rodará com as permissões do usuário logado. Garantir que o acesso a arquivos e diretórios respeite as permissões do sistema operacional.
*   **Hashing Seguro:** BLAKE3 é um algoritmo de hash criptográfico moderno e rápido, adequado para identificação de arquivos idênticos e resistente a colisões acidentais.
*   **Dados Sensíveis:** O aplicativo lida com caminhos de arquivo do usuário. Não há dados sensíveis adicionais (senhas, etc.) previstos. Logs devem evitar informações excessivamente detalhadas que possam ser sensíveis, se aplicável.

## 8. Justificativas e Trade-offs

*   **Arquitetura em Camadas vs. Outras:** Escolhida pela simplicidade e clareza para uma aplicação desktop. Microsserviços seriam excessivos. Uma arquitetura puramente baseada em eventos poderia adicionar complexidade na comunicação entre componentes para este escopo.
*   **`concurrent.futures`:** Oferece uma abstração de alto nível para paralelismo (threads para I/O, processos para CPU-bound como hashing BLAKE3), simplificando o gerenciamento em comparação com `threading` ou `multiprocessing` puros.
*   **`stream-unzip`:** Essencial para o requisito de lidar com grandes ZIPs com baixo uso de memória, processando arquivos um a um em vez de extrair tudo de uma vez.
*   **PySide6 (Qt):** Framework robusto e maduro para GUIs desktop, com bom suporte a multithreading (via `QThread` e signals/slots) que se integra bem com a necessidade de tarefas em background.
*   **BLAKE3:** Oferece excelente desempenho para hashing, crucial para a velocidade de identificação de duplicatas em grandes volumes.
*   **Separação `core` vs. `infrastructure`:** Garante que a lógica de negócio principal seja pura e testável, isolada dos detalhes de implementação de I/O, que podem mudar (ex: suportar outros formatos compactados no futuro).
*   **Interfaces Explícitas:** A definição clara das interfaces e estruturas de dados é crucial para o baixo acoplamento e facilita a evolução e os testes (mocking).
*   **Trade-off:** A comunicação assíncrona entre a camada de Aplicação/Infraestrutura (background threads/processes) e a GUI adiciona alguma complexidade (gerenciamento de signals/slots ou filas), mas é necessária para a responsividade da UI.

---

Esta proposta fornece um blueprint sólido para o desenvolvimento do `Fotix`, priorizando os requisitos funcionais e não funcionais definidos, com foco em uma estrutura manutenível e robusta.

    # --- Conteúdo de [Prompt_Tocrisna_Architecture_v1.0.md] ---
    
---

# AGV Prompt Template: Tocrisna v1.0 - Definição da Arquitetura Técnica

**Tarefa Principal:** Definir e documentar uma proposta de arquitetura técnica de alto nível para o projeto descrito abaixo. O foco deve ser na modularidade, clareza, manutenibilidade, e na definição clara dos principais componentes e suas interfaces de comunicação.

## Contexto e Definições Iniciais do Projeto

- **Nome do Projeto:** `Fotix`

- **Visão Geral / Objetivo Principal:**

    Aplicativo desktop desenvolvido em Python, com backend robusto e interface gráfica (GUI) completa, projetado para localizar e remover arquivos duplicados (idênticos) de imagens e vídeos em múltiplos diretórios e arquivos ZIP.
    O sistema analisa arquivos de mídia e, **somente ao identificar dois ou mais arquivos idênticos**, utiliza um algoritmo inteligente para decidir qual arquivo manter e qual remover, com base em critérios como maior resolução da imagem, data de criação mais antiga e estrutura do nome do arquivo (evitando cópias como "(1)", "cópia", etc.).
    A arquitetura é otimizada para grandes volumes de dados, utilizando processamento assíncrono, batching progressivo e execução paralela.
    O aplicativo também oferece sistema de backup e restauração para recuperação segura dos arquivos removidos.

- **Funcionalidades Chave (Alto Nível):**

    - Análise de arquivos de mídia (imagens e vídeos) em diretórios e arquivos ZIP.
    - Identificação precisa de arquivos duplicados (idênticos) utilizando hashing.
    - Seleção automática do arquivo a ser mantido entre duplicatas com base em critérios objetivos.
    - Remoção segura de duplicatas com backup automático.
    - Recuperação fácil de arquivos removidos através do sistema de restauração.
    - Processamento otimizado para grandes volumes de dados com execução assíncrona, paralela e em lotes.
    - Interface gráfica intuitiva para configuração e acompanhamento.
    - Geração de logs detalhados e relatórios resumidos com estatísticas pós-processamento.

- **Público Alvo / Ambiente de Uso:** `Usuários finais em desktop (Windows)`

- **Stack Tecnológica Definida:**

  - **Linguagem Principal:** Python 3.10+
  - **GUI (Interface Gráfica):** PySide6 (Qt for Python) — framework moderno para criação de interfaces desktop nativas.
  - **Motor de Escaneamento de Duplicatas:** BLAKE3 + pré-filtragem por tamanho com `os.path.getsize` para otimização inicial.
  - **Manipulação de Arquivos e Sistema de Arquivos:** pathlib + shutil + send2trash (remoção segura) + concurrent.futures (execução paralela).
  - **Descompactação Otimizada:** stream-unzip para leitura e extração progressiva de arquivos ZIP.

- **Requisitos Não Funcionais Iniciais:**

  - Capacidade de processar grandes volumes (100.000+ arquivos) sem travamentos.
  - Identificação rápida de duplicatas com uso eficiente de CPU, RAM e disco.
  - Backups automáticos para garantir segurança de dados.
  - GUI responsiva mesmo sob alta carga de processamento.
  - Compatibilidade garantida com Windows 10 ou superior.
  - Descompactação eficiente e rápida de grandes arquivos ZIP com baixo uso de memória.
  - Tratamento de erros em operações críticas de escrita e remoção.

- **Principais Restrições:**

    - Suporte exclusivo para Windows na primeira versão.
    - Sem integração com bancos de dados externos.
    - Análise limitada a arquivos idêticos (sem similaridade perceptual).
    - Suporte apenas ao formato ZIP para arquivos compactados.
    - Sem sistema de atualização automática previsto na primeira versão.
    - Desempenho condicionado à capacidade de hardware local do usuário.

## Diretrizes e Princípios Arquiteturais (Filosofia AGV)

1. **Modularidade e Separação de Responsabilidades (SRP):** Proponha uma divisão clara em módulos/componentes lógicos, cada um com uma responsabilidade bem definida. Minimize o acoplamento entre eles e maximize a coesão interna.
2. **Clareza e Manutenibilidade:** A arquitetura deve ser fácil de entender, manter e evoluir. Prefira soluções mais simples (KISS) quando apropriado.
3. **Definição Explícita de Interfaces:** **CRUCIAL:** Para os principais pontos de interação entre os módulos identificados, defina claramente as interfaces (contratos). Isso inclui:
   - Assinaturas de funções/métodos públicos chave.
   - Estruturas de dados (Dataclasses, NamedTuples, Pydantic Models) usadas para troca de informações.
   - Descreva brevemente o propósito de cada interface exposta.
4. **Testabilidade:** A arquitetura deve facilitar a escrita de testes unitários e de integração (ex: permitir injeção de dependência onde fizer sentido).
5. **Segurança Fundamental:** Incorpore princípios básicos de segurança desde o design (ex: onde a validação de input deve ocorrer, como dados sensíveis podem ser tratados – sugerir hashing/criptografia, necessidade de autenticação/autorização).
6. **Aderência à Stack:** Utilize primariamente as tecnologias definidas na Stack Tecnológica. Se sugerir uma tecnologia *adicional*, justifique claramente a necessidade.
7. **Padrões de Design:** Sugira e aplique padrões de design relevantes (ex: Repository, Service Layer, Observer, Strategy, etc.) onde eles agregarem valor à estrutura e manutenibilidade. Justifique brevemente a escolha.
8. **Escalabilidade (Básica):** Considere como a arquitetura pode suportar um crescimento moderado no futuro (ex: design sem estado para serviços, possibilidade de paralelizar tarefas).

## Resultado Esperado (Blueprint Arquitetural)

Um documento (preferencialmente em Markdown) descrevendo a arquitetura proposta, incluindo:

1. **Visão Geral da Arquitetura:** Um breve resumo da abordagem arquitetural escolhida (ex: Arquitetura em Camadas, Microsserviços simples, Baseada em Eventos, etc.) e uma justificativa.
2. **Diagrama de Componentes (Simplificado):** Um diagrama de blocos (pode ser textual/ASCII ou uma descrição clara) mostrando os principais módulos/componentes e suas interconexões de alto nível.
3. **Descrição dos Componentes/Módulos:** Para cada componente principal identificado:
   - Nome claro (ex: `core`, `api`, `data_access`, `utils`).
   - Responsabilidade principal.
   - Tecnologias chave da stack que serão usadas nele.
4. **Definição das Interfaces Principais:** Detalhamento dos contratos de comunicação entre os componentes chave (conforme Diretriz 3).
5. **Gerenciamento de Dados (se aplicável):** Como os dados serão persistidos e acessados (ex: Módulo `data_access` usando SQLAlchemy com padrão Repository).
6. **Estrutura de Diretórios Proposta:** Uma sugestão inicial para a organização das pastas e arquivos principais do projeto.
7. **Considerações de Segurança:** Resumo dos princípios de segurança aplicados no design.
8. **Justificativas e Trade-offs:** Breve explicação das principais decisões arquiteturais e por que alternativas foram descartadas (se relevante).
    

**Instruções Detalhadas para Validação:**

1.  **Comparação Seção por Seção:** Para cada seção preenchida no `Prompt Preenchido`, compare seu conteúdo com as informações correspondentes nos `Documentos Fonte`.
2.  **Identificar Discrepâncias:** Aponte *qualquer* diferença, incluindo:
    *   **Informação Incorreta:** Dados no prompt preenchido que contradizem a fonte.
    *   **Informação Omitida:** Dados relevantes da fonte que *deveriam* estar no prompt preenchido, mas não estão.
    *   **Alucinação/Invenção:** Informações presentes no prompt preenchido que *não* têm base nos documentos fonte.
    *   **Interpretação Errada:** Informação da fonte que foi distorcida ou mal aplicada no prompt preenchido.
3.  **Verificar Completude:** Certifique-se de que *todos* os placeholders relevantes do `Template Original` foram adequadamente preenchidos no `Prompt Preenchido`.
4.  **Validação Estrutural (Mapeamento Fonte -> Destino):** Para cada seção principal preenchida no `Prompt Preenchido`, tente identificar e declarar *qual documento fonte* (e, se possível, qual parte dele) foi usado para preencher aquela seção específica. Isso ajuda a verificar se o Preenchedor usou as fontes corretas para cada parte.
5.  **Consistência Geral:** Avalie se o prompt preenchido como um todo faz sentido lógico e está internamente consistente.

**Resultado Esperado:**

Um **Relatório de Validação Detalhado** em Markdown, contendo:

1.  **Resumo Geral:** Uma avaliação sucinta (ex: "Preenchimento correto", "Preenchimento com pequenas inconsistências", "Preenchimento com erros significativos").
2.  **Lista de Achados (Discrepâncias e Confirmações):**
    *   Para cada discrepância encontrada (incorreção, omissão, alucinação, interpretação errada):
        *   Indique a seção do `Prompt Preenchido` afetada.
        *   Descreva o problema específico.
        *   Referencie a informação correta/faltante no `Documento Fonte`.
    *   Mencione seções importantes que foram preenchidas *corretamente*.
3.  **Relatório de Validação Estrutural (Mapeamento):**
    *   Liste as seções principais do `Prompt Preenchido` e indique a fonte provável para cada uma. (Ex: "Seção 'Dependências Diretas' preenchida com base na Seção 3.X do `Output_Tocrisna_Blueprint.md`").
4.  **Recomendação:** Indique se o `Prompt Preenchido` está pronto para ser usado na próxima fase do AGV ou se precisa de correções (e quais).