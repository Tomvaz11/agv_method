## Blueprint Arquitetural: Fotix v5.0

### 1. Visão Geral da Arquitetura

A arquitetura proposta para o `Fotix` será uma **Arquitetura em Camadas (Layered Architecture)**. Esta abordagem promove uma clara separação de responsabilidades, modularidade e facilita a manutenibilidade e testabilidade do sistema. As camadas principais serão:

1.  **Camada de Apresentação (UI):** Responsável pela interação com o usuário, utilizando PySide6.
2.  **Camada de Aplicação:** Orquestra os casos de uso, coordenando as interações entre a UI e o Core/Domínio, e utilizando os serviços de infraestrutura.
3.  **Camada de Domínio/Core:** Contém a lógica de negócio principal, modelos de dados e as regras para identificação e seleção de duplicatas. É independente de frameworks de UI ou detalhes de infraestrutura.
4.  **Camada de Infraestrutura:** Fornece implementações concretas para acesso ao sistema de arquivos, concorrência, backup, descompactação e logging, abstraindo as bibliotecas de baixo nível.

**Justificativa:**
*   **Modularidade:** Cada camada tem responsabilidades distintas, facilitando o desenvolvimento e a manutenção.
*   **Testabilidade:** As camadas de Aplicação e Domínio podem ser testadas independentemente da UI e da infraestrutura real (usando mocks/stubs para as interfaces de infraestrutura).
*   **Manutenibilidade:** Mudanças na UI ou em uma biblioteca de infraestrutura específica (ex: um novo método de hashing) têm menor probabilidade de impactar outras camadas, desde que as interfaces sejam respeitadas.
*   **Clareza:** A estrutura é bem compreendida e promove um fluxo de dependências unidirecional (Apresentação -> Aplicação -> Domínio; Aplicação/Domínio -> Interfaces de Infraestrutura <- Implementações de Infraestrutura).

### 2. Diagrama de Componentes (Simplificado)

```mermaid
graph TD
    subgraph Camada de Apresentação (UI)
        UI_MainWindow["FotixMainWindow (PySide6)"]
        UI_Views["Views/Dialogs (PySide6) \n (Config, Progresso, Resultados, Restauração)"]
    end

    subgraph Camada de Aplicação
        App_ScanService["ScanService"]
        App_DuplicateMgtService["DuplicateManagementService"]
        App_RestoreService["RestoreService"]
        App_ReportingService["ReportingService"]
        App_ConfigService["ConfigurationService"]
    end

    subgraph Camada de Domínio/Core
        Domain_Models["Models (Pydantic) \n (FileEntry, DuplicateSet, ScanConfig, BackupRecord)"]
        Domain_DuplicateFinder["DuplicateFinderEngine"]
        Domain_SelectionStrategy["SelectionStrategy"]
    end

    subgraph Camada de Infraestrutura
        Infra_FileSystem["FileSystemService \n (pathlib, shutil, send2trash, os.path)"]
        Infra_Concurrency["ConcurrencyService \n (concurrent.futures)"]
        Infra_Backup["BackupService"]
        Infra_Zip["ZipService \n (stream-unzip)"]
        Infra_Hashing["HashingService \n (blake3)"]
        Infra_Logging["LoggingService \n (logging stdlib)"]
    end

    %% Interfaces (Abstrações)
    Abs_IFileSystem["IFileSystemService (ABC)"]
    Abs_IConcurrency["IConcurrencyService (ABC)"]
    Abs_IBackup["IBackupService (ABC)"]
    Abs_IZip["IZipService (ABC)"]
    Abs_IHashing["IHashingService (ABC)"]
    Abs_ILogging["ILoggingService (ABC)"]


    %% Conexões UI -> Aplicação
    UI_MainWindow --> App_ScanService
    UI_MainWindow --> App_DuplicateMgtService
    UI_MainWindow --> App_RestoreService
    UI_MainWindow --> App_ConfigService
    UI_Views --> App_ScanService
    UI_Views --> App_DuplicateMgtService
    UI_Views --> App_RestoreService
    UI_Views --> App_ConfigService

    %% Conexões Aplicação -> Domínio
    App_ScanService --> Domain_DuplicateFinder
    App_ScanService --> Domain_Models
    App_DuplicateMgtService --> Domain_SelectionStrategy
    App_DuplicateMgtService --> Domain_Models
    App_RestoreService --> Domain_Models

    %% Conexões Aplicação -> Interfaces de Infraestrutura
    App_ScanService --> Abs_IFileSystem
    App_ScanService --> Abs_IConcurrency
    App_ScanService --> Abs_IZip
    App_ScanService --> Abs_IHashing
    App_ScanService --> Abs_ILogging
    App_DuplicateMgtService --> Abs_IFileSystem
    App_DuplicateMgtService --> Abs_IBackup
    App_DuplicateMgtService --> Abs_ILogging
    App_RestoreService --> Abs_IFileSystem
    App_RestoreService --> Abs_IBackup
    App_RestoreService --> Abs_ILogging
    App_ReportingService --> Abs_ILogging
    App_ConfigService --> Abs_IFileSystem %% Para ler/salvar config

    %% Conexões Domínio -> Interfaces de Infraestrutura (Mínimas, se necessário. Idealmente Domínio não conhece infra)
    Domain_DuplicateFinder --> Abs_IHashing %% Para lógica de hash
    Domain_DuplicateFinder --> Abs_IFileSystem %% Para obter tamanho do arquivo (pré-filtragem)

    %% Implementações de Infraestrutura -> Interfaces
    Infra_FileSystem -.-> Abs_IFileSystem
    Infra_Concurrency -.-> Abs_IConcurrency
    Infra_Backup -.-> Abs_IBackup
    Infra_Zip -.-> Abs_IZip
    Infra_Hashing -.-> Abs_IHashing
    Infra_Logging -.-> Abs_ILogging

    style Abs_IFileSystem fill:#E6E6FA,stroke:#333,stroke-width:2px
    style Abs_IConcurrency fill:#E6E6FA,stroke:#333,stroke-width:2px
    style Abs_IBackup fill:#E6E6FA,stroke:#333,stroke-width:2px
    style Abs_IZip fill:#E6E6FA,stroke:#333,stroke-width:2px
    style Abs_IHashing fill:#E6E6FA,stroke:#333,stroke-width:2px
    style Abs_ILogging fill:#E6E6FA,stroke:#333,stroke-width:2px
```

### 3. Descrição dos Componentes/Módulos

#### 3.1. Camada de Apresentação (`fotix.ui`)
Responsável pela interface com o usuário.

*   **Tecnologias Chave:** PySide6
*   **Dependências Diretas Principais:** `fotix.application.services`, `fotix.domain.models` (para exibir dados)

*   **`MainWindow (main_window.py)`**
    *   **Propósito:** Janela principal da aplicação, contendo menus, barra de status e área central para exibir diferentes views. Orquestra a navegação entre as views.
    *   **Interage com:** `ScanService`, `DuplicateManagementService`, `RestoreService`, `ConfigurationService`.
    *   **Unidade Independente:** Sim, principal ponto de entrada da UI.

*   **`DirectorySelectionView (directory_selection_view.py)`**
    *   **Propósito:** Permite ao usuário selecionar diretórios e arquivos ZIP para escanear, configurar opções de escaneamento (ex: tipos de arquivo).
    *   **Interage com:** `ScanService` (para iniciar escaneamento), `ConfigurationService` (para carregar/salvar padrões).
    *   **Unidade Independente:** Sim.

*   **`ScanProgressView (scan_progress_view.py)`**
    *   **Propósito:** Exibe o progresso do escaneamento em tempo real (arquivos processados, duplicatas encontradas), permite cancelar a operação.
    *   **Interage com:** `ScanService` (para receber atualizações de progresso e enviar comando de cancelamento).
    *   **Unidade Independente:** Sim.

*   **`ResultsView (results_view.py)`**
    *   **Propósito:** Apresenta os conjuntos de arquivos duplicados encontrados, permitindo ao usuário revisar as seleções automáticas e, opcionalmente, alterá-las antes de confirmar a remoção.
    *   **Interage com:** `DuplicateManagementService` (para obter resultados e confirmar ações).
    *   **Unidade Independente:** Sim.

*   **`BackupRestoreView (backup_restore_view.py)`**
    *   **Propósito:** Lista os backups disponíveis e permite ao usuário selecionar arquivos/conjuntos para restauração.
    *   **Interage com:** `RestoreService` (para listar backups e iniciar restauração).
    *   **Unidade Independente:** Sim.

*   **`SettingsDialog (settings_dialog.py)`**
    *   **Propósito:** Permite ao usuário configurar preferências da aplicação (ex: caminho do backup, nível de log, critérios de seleção padrão).
    *   **Interage com:** `ConfigurationService`.
    *   **Unidade Independente:** Sim.

*   **`LogView (log_view.py)`**
    *   **Propósito:** Exibe os logs da aplicação de forma amigável.
    *   **Interage com:** `ReportingService` (para obter logs).
    *   **Unidade Independente:** Sim.

#### 3.2. Camada de Aplicação (`fotix.application`)
Orquestra os casos de uso e serve como intermediário entre a UI e o Domínio/Infraestrutura.

*   **`ScanService (scan_service.py)`**
    *   **Responsabilidade:** Orquestra o processo de escaneamento de arquivos. Utiliza `FileSystemService` para listar arquivos, `ZipService` para arquivos ZIP, `ConcurrencyService` para processamento paralelo, `HashingService` para gerar hashes, e `DuplicateFinderEngine` para identificar duplicatas. Emite eventos de progresso para a UI.
    *   **Tecnologias Chave:** Python (Lógica Pura).
    *   **Dependências Diretas:** `fotix.application.interfaces.IFileSystemService`, `fotix.application.interfaces.IZipService`, `fotix.application.interfaces.IConcurrencyService`, `fotix.application.interfaces.IHashingService`, `fotix.application.interfaces.ILoggingService`, `fotix.domain.core.DuplicateFinderEngine`, `fotix.domain.models`.

*   **`DuplicateManagementService (duplicate_management_service.py)`**
    *   **Responsabilidade:** Gerencia a lógica de seleção de arquivos a serem mantidos/removidos (usando `SelectionStrategy`), coordena o processo de backup (via `BackupService`) e remoção segura de arquivos (via `FileSystemService`).
    *   **Tecnologias Chave:** Python (Lógica Pura).
    *   **Dependências Diretas:** `fotix.application.interfaces.IFileSystemService`, `fotix.application.interfaces.IBackupService`, `fotix.application.interfaces.ILoggingService`, `fotix.domain.core.SelectionStrategy`, `fotix.domain.models`.

*   **`RestoreService (restore_service.py)`**
    *   **Responsabilidade:** Gerencia o processo de restauração de arquivos a partir dos backups. Utiliza `BackupService` para identificar e recuperar arquivos e `FileSystemService` para colocá-los de volta.
    *   **Tecnologias Chave:** Python (Lógica Pura).
    *   **Dependências Diretas:** `fotix.application.interfaces.IFileSystemService`, `fotix.application.interfaces.IBackupService`, `fotix.application.interfaces.ILoggingService`, `fotix.domain.models`.

*   **`ReportingService (reporting_service.py)`**
    *   **Responsabilidade:** Coleta informações e estatísticas do processamento para gerar relatórios resumidos e fornecer acesso aos logs detalhados para a UI. Interage com `LoggingService`.
    *   **Tecnologias Chave:** Python (Lógica Pura).
    *   **Dependências Diretas:** `fotix.application.interfaces.ILoggingService`.

*   **`ConfigurationService (configuration_service.py)`**
    *   **Responsabilidade:** Gerencia as configurações da aplicação (ex: caminhos padrão, preferências do usuário). Lê e salva configurações, possivelmente em um arquivo JSON ou INI, usando `FileSystemService`. Fornece configurações para outros serviços.
    *   **Tecnologias Chave:** Python (Lógica Pura), Pydantic `BaseModel` para estrutura de configuração.
    *   **Dependências Diretas:** `fotix.application.interfaces.IFileSystemService`, `fotix.domain.models` (para o modelo de configuração).

#### 3.3. Camada de Domínio/Core (`fotix.domain`)
Contém a lógica de negócio pura e os modelos de dados.

*   **`Models (models.py)`**
    *   **Responsabilidade:** Define as estruturas de dados centrais da aplicação (DTOs, entidades).
        *   `FileEntry`: Representa um arquivo com seus metadados (caminho, tamanho, hash, data de criação, resolução, etc.).
        *   `DuplicateSet`: Um conjunto de `FileEntry` que são idênticos.
        *   `ScanConfig`: Configurações para uma operação de escaneamento.
        *   `BackupRecord`: Metadados de um arquivo/conjunto que foi "removido" (backupeado).
        *   `AppConfig`: Modelo para as configurações globais da aplicação.
    *   **Tecnologias Chave:** Pydantic `BaseModel`.
    *   **Dependências Diretas:** Nenhuma (apenas Pydantic e tipos Python padrão).

*   **`DuplicateFinderEngine (duplicate_finder.py)`**
    *   **Responsabilidade:** Implementa a lógica central de identificação de duplicatas. Recebe uma lista de `FileEntry`, aplica pré-filtragem por tamanho, depois utiliza `HashingService` para calcular hashes e agrupa arquivos idênticos.
    *   **Tecnologias Chave:** Python (Lógica Pura).
    *   **Dependências Diretas:** `fotix.domain.models`, `fotix.application.interfaces.IHashingService`, `fotix.application.interfaces.IFileSystemService` (apenas para `get_file_size` se não vier no `FileEntry`).

*   **`SelectionStrategy (selection_strategy.py)`**
    *   **Responsabilidade:** Implementa o algoritmo inteligente para decidir qual arquivo manter de um `DuplicateSet` com base nos critérios definidos (resolução, data, nome do arquivo). Pode ser implementado usando o padrão Strategy se múltiplos algoritmos forem previstos no futuro.
    *   **Tecnologias Chave:** Python (Lógica Pura).
    *   **Dependências Diretas:** `fotix.domain.models`.

#### 3.4. Camada de Infraestrutura (`fotix.infrastructure`)
Implementações concretas das interfaces de serviços externos.

*   **`FileSystemService (file_system_service.py)`**
    *   **Responsabilidade:** Implementa `IFileSystemService`. Abstrai as operações de sistema de arquivos (`pathlib`, `shutil`, `os.path.getsize`, `send2trash`).
    *   **Tecnologias Chave:** `pathlib`, `shutil`, `os`, `send2trash`.
    *   **Dependências Diretas:** Nenhuma (apenas bibliotecas padrão/stack definida).

*   **`ConcurrencyService (concurrency_service.py)`**
    *   **Responsabilidade:** Implementa `IConcurrencyService`. Abstrai o uso de `concurrent.futures` para execução paralela e assíncrona de tarefas (ex: hashing de múltiplos arquivos).
    *   **Tecnologias Chave:** `concurrent.futures`.
    *   **Dependências Diretas:** Nenhuma (apenas bibliotecas padrão).

*   **`BackupService (backup_service.py)`**
    *   **Responsabilidade:** Implementa `IBackupService`. Gerencia a criação de backups (copiando arquivos para um local seguro) e a restauração. Mantém metadados dos backups (ex: em um arquivo JSON).
    *   **Tecnologias Chave:** `pathlib`, `shutil`, `json` (para metadados), Pydantic `BaseModel` (para metadados).
    *   **Dependências Diretas:** `fotix.domain.models` (para `BackupRecord`).

*   **`ZipService (zip_service.py)`**
    *   **Responsabilidade:** Implementa `IZipService`. Abstrai a leitura e extração progressiva de arquivos ZIP usando `stream-unzip`.
    *   **Tecnologias Chave:** `stream-unzip`.
    *   **Dependências Diretas:** Nenhuma (apenas biblioteca da stack).

*   **`HashingService (hashing_service.py)`**
    *   **Responsabilidade:** Implementa `IHashingService`. Abstrai o cálculo de hash de arquivos usando BLAKE3.
    *   **Tecnologias Chave:** `blake3`.
    *   **Dependências Diretas:** Nenhuma (apenas biblioteca da stack).

*   **`LoggingService (logging_service.py)`**
    *   **Responsabilidade:** Implementa `ILoggingService`. Configura e fornece uma interface para o sistema de logging padrão do Python (`logging`). Pode incluir formatação customizada, múltiplos handlers (console, arquivo).
    *   **Tecnologias Chave:** `logging` (stdlib).
    *   **Dependências Diretas:** Nenhuma (apenas biblioteca padrão).

### 4. Definição das Interfaces Principais (`fotix.application.interfaces` e `fotix.infrastructure.interfaces`)

Interfaces serão definidas usando `abc.ABC` e `abc.abstractmethod`.
Os modelos de dados (Pydantic) de `fotix.domain.models` serão usados para tipos de parâmetros e retorno.

#### 4.1. `IFileSystemService (fotix.application.interfaces.file_system.py)`
```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Iterator, Tuple

class IFileSystemService(ABC):
    @abstractmethod
    def __init__(self, logger: 'ILoggingService'): # Exemplo de dependência básica
        pass

    @abstractmethod
    def get_file_size(self, file_path: Path) -> int:
        """Retorna o tamanho do arquivo em bytes."""
        pass

    @abstractmethod
    def list_files_recursive(self, dir_path: Path, extensions: Tuple[str, ...]) -> Iterator[Path]:
        """Lista arquivos recursivamente em um diretório, filtrando por extensões."""
        pass

    @abstractmethod
    def path_exists(self, path: Path) -> bool:
        """Verifica se um caminho existe."""
        pass

    @abstractmethod
    def is_file(self, path: Path) -> bool:
        """Verifica se um caminho é um arquivo."""
        pass

    @abstractmethod
    def is_dir(self, path: Path) -> bool:
        """Verifica se um caminho é um diretório."""
        pass

    @abstractmethod
    def move_to_trash(self, file_path: Path) -> None:
        """Move o arquivo para a lixeira do sistema."""
        pass

    @abstractmethod
    def copy_file(self, source_path: Path, destination_path: Path) -> None:
        """Copia um arquivo."""
        pass

    @abstractmethod
    def create_directory(self, dir_path: Path, parents: bool = True, exist_ok: bool = True) -> None:
        """Cria um diretório."""
        pass

    @abstractmethod
    def read_file_chunks(self, file_path: Path, chunk_size: int = 8192) -> Iterator[bytes]:
        """Lê um arquivo em pedaços (chunks)."""
        pass

    @abstractmethod
    def get_creation_time(self, file_path: Path) -> float:
        """Retorna o timestamp de criação do arquivo."""
        pass

    @abstractmethod
    def get_modification_time(self, file_path: Path) -> float:
        """Retorna o timestamp da última modificação do arquivo."""
        pass
```

#### 4.2. `IHashingService (fotix.application.interfaces.hashing.py)`
```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable # Para callbacks de progresso

class IHashingService(ABC):
    @abstractmethod
    def __init__(self, logger: 'ILoggingService'):
        pass

    @abstractmethod
    def calculate_hash(self, file_path: Path, progress_callback: Callable[[int, int], None] = None) -> str:
        """Calcula o hash BLAKE3 de um arquivo.
        progress_callback(bytes_processed, total_bytes) opcional.
        """
        pass
```

#### 4.3. `IZipService (fotix.application.interfaces.zip.py)`
```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator, Tuple, Callable
from fotix.domain.models import FileEntry # Usando um modelo de domínio como exemplo

class IZipService(ABC):
    @abstractmethod
    def __init__(self, logger: 'ILoggingService'):
        pass

    @abstractmethod
    def stream_extract_paths_and_hashes(
        self,
        zip_file_path: Path,
        target_extensions: Tuple[str, ...],
        hashing_service: 'IHashingService', # Dependência para hashear os arquivos dentro do ZIP
        progress_callback: Callable[[str, int, int], None] = None # file_in_zip, bytes_processed, total_bytes
    ) -> Iterator[FileEntry]: # FileEntry com dados do arquivo dentro do ZIP
        """
        Extrai arquivos de um ZIP progressivamente, calcula hashes e retorna FileEntry.
        Não armazena os arquivos extraídos em disco permanentemente, apenas em memória/temp para hashing.
        """
        pass
```

#### 4.4. `IConcurrencyService (fotix.application.interfaces.concurrency.py)`
```python
from abc import ABC, abstractmethod
from typing import Callable, Iterable, Any, Iterator, Optional
from concurrent.futures import Future

class IConcurrencyService(ABC):
    @abstractmethod
    def __init__(self, max_workers: Optional[int] = None, logger: 'ILoggingService'):
        """max_workers: Número máximo de threads/processos. None para padrão do executor."""
        pass

    @abstractmethod
    def run_parallel(self, func: Callable[..., Any], tasks: Iterable[Any]) -> Iterator[Any]:
        """Executa uma função em paralelo para uma lista de tarefas/argumentos."""
        pass

    @abstractmethod
    def submit_task(self, func: Callable[..., Any], *args, **kwargs) -> Future:
        """Submete uma única tarefa para execução assíncrona."""
        pass
```

#### 4.5. `IBackupService (fotix.application.interfaces.backup.py)`
```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from fotix.domain.models import FileEntry, BackupRecord # Exemplo de modelos

class IBackupService(ABC):
    @abstractmethod
    def __init__(self, backup_root_path: Path, logger: 'ILoggingService'):
        """backup_root_path: Diretório raiz onde os backups serão armazenados."""
        self.backup_root_path = backup_root_path
        self.logger = logger
        # self.metadata_file = backup_root_path / "fotix_backup_metadata.json" # Exemplo

    @abstractmethod
    def backup_file(self, file_to_backup: FileEntry) -> BackupRecord:
        """Cria um backup do arquivo e retorna metadados do backup."""
        pass

    @abstractmethod
    def restore_file(self, backup_record: BackupRecord, restore_path: Path) -> bool:
        """Restaura um arquivo do backup para o caminho especificado."""
        pass

    @abstractmethod
    def list_backups(self) -> List[BackupRecord]:
        """Lista todos os backups disponíveis."""
        pass

    @abstractmethod
    def remove_backup(self, backup_record: BackupRecord) -> bool:
        """Remove um backup específico (arquivo e metadados)."""
        pass
```

#### 4.6. `ILoggingService (fotix.application.interfaces.logging.py)`
```python
from abc import ABC, abstractmethod
from typing import Optional

class ILoggingService(ABC):
    @abstractmethod
    def __init__(self, log_file_path: Optional[Path] = None, level: str = "INFO", app_name: str = "Fotix"):
        """
        log_file_path: Caminho para o arquivo de log. Se None, pode logar apenas no console.
        level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        """
        pass

    @abstractmethod
    def debug(self, message: str, exc_info: bool = False) -> None:
        pass

    @abstractmethod
    def info(self, message: str, exc_info: bool = False) -> None:
        pass

    @abstractmethod
    def warning(self, message: str, exc_info: bool = False) -> None:
        pass

    @abstractmethod
    def error(self, message: str, exc_info: bool = False) -> None:
        pass

    @abstractmethod
    def critical(self, message: str, exc_info: bool = False) -> None:
        pass

    @abstractmethod
    def get_logs(self, count: Optional[int] = None) -> List[str]:
        """Retorna as últimas 'count' entradas de log (se o handler de arquivo estiver configurado e for acessível)."""
        pass
```

**Configuração dos Componentes:**
A configuração dos componentes de serviço (especialmente os da camada de Aplicação e Infraestrutura) será feita majoritariamente via seus construtores (`__init__`). Parâmetros de configuração essenciais (como `backup_root_path` para `BackupService` ou `max_workers` para `ConcurrencyService`) e dependências de outros serviços (abstraídos por suas interfaces) serão passados na instanciação.

O `ConfigurationService` será responsável por carregar configurações globais de um arquivo (ex: `config.json`) e fornecê-las durante a inicialização da aplicação.

### 5. Gerenciamento de Dados

*   **Dados de Configuração da Aplicação:**
    *   Um arquivo JSON (ex: `~/.fotix/config.json` ou `%APPDATA%/Fotix/config.json`) gerenciado pelo `ConfigurationService`.
    *   A estrutura deste JSON será definida por um Pydantic `BaseModel` (ex: `AppConfig` em `fotix.domain.models`).
*   **Metadados de Backup:**
    *   Um arquivo JSON (ex: `BACKUP_ROOT_PATH/fotix_backup_metadata.json`) gerenciado pelo `BackupService`.
    *   A estrutura de cada registro de backup será definida por um Pydantic `BaseModel` (`BackupRecord` em `fotix.domain.models`).
*   **Dados Temporários (durante o escaneamento):**
    *   Listas de `FileEntry` e `DuplicateSet` serão mantidas em memória. Dado o volume potencial, estratégias de batching e processamento progressivo são cruciais.
    *   O `stream-unzip` ajuda a evitar o armazenamento de todo o conteúdo do ZIP em disco/memória de uma vez.
*   **Logs:**
    *   Gerenciados pelo `LoggingService`, podendo ser direcionados para console e/ou arquivo de log (ex: `~/.fotix/logs/fotix.log`).

Não haverá banco de dados externo na primeira versão.

### 6. Estrutura de Diretórios Proposta (Layout `src`)

```
fotix_project/
├── src/
│   └── fotix/
│       ├── __init__.py
│       ├── main.py                   # Ponto de entrada da aplicação, bootstrapping
│       ├── app_config.py             # Lógica para carregar e prover AppConfig
│       │
│       ├── ui/                       # Camada de Apresentação (PySide6)
│       │   ├── __init__.py
│       │   ├── main_window.py
│       │   ├── views/
│       │   │   ├── __init__.py
│       │   │   ├── directory_selection_view.py
│       │   │   ├── scan_progress_view.py
│       │   │   ├── results_view.py
│       │   │   ├── backup_restore_view.py
│       │   │   └── log_view.py
│       │   ├── dialogs/
│       │   │   └── settings_dialog.py
│       │   └── widgets/              # Componentes de UI reutilizáveis
│       │       └── __init__.py
│       │
│       ├── application/              # Camada de Aplicação
│       │   ├── __init__.py
│       │   ├── services/             # Implementações dos serviços de aplicação
│       │   │   ├── __init__.py
│       │   │   ├── scan_service.py
│       │   │   ├── duplicate_management_service.py
│       │   │   ├── restore_service.py
│       │   │   ├── reporting_service.py
│       │   │   └── configuration_service.py
│       │   └── interfaces/           # Contratos/ABCs para serviços (opcional aqui, se forem mais para infra)
│       │       └── __init__.py
│       │
│       ├── domain/                   # Camada de Domínio/Core
│       │   ├── __init__.py
│       │   ├── models.py             # Pydantic models (FileEntry, DuplicateSet, etc.)
│       │   └── core/                 # Lógica de negócio principal
│       │       ├── __init__.py
│       │       ├── duplicate_finder.py # DuplicateFinderEngine
│       │       └── selection_strategy.py
│       │
│       ├── infrastructure/           # Camada de Infraestrutura
│       │   ├── __init__.py
│       │   ├── implementations/      # Implementações concretas dos serviços de infra
│       │   │   ├── __init__.py
│       │   │   ├── file_system_service.py
│       │   │   ├── concurrency_service.py
│       │   │   ├── backup_service.py
│       │   │   ├── zip_service.py
│       │   │   ├── hashing_service.py
│       │   │   └── logging_service.py
│       │   └── interfaces/           # Contratos/ABCs para serviços de infraestrutura
│       │       ├── __init__.py
│       │       ├── file_system.py    # IFileSystemService
│       │       ├── hashing.py        # IHashingService
│       │       ├── zip.py            # IZipService
│       │       ├── concurrency.py    # IConcurrencyService
│       │       ├── backup.py         # IBackupService
│       │       └── logging.py        # ILoggingService
│       │
│       └── utils/                    # Utilitários diversos
│           ├── __init__.py
│           └── helpers.py            # Funções auxiliares genéricas
│
├── tests/                            # Testes unitários e de integração
│   ├── __init__.py
│   ├── unit/
│   │   ├── application/
│   │   ├── domain/
│   │   └── infrastructure/
│   └── integration/
│
├── .gitignore
├── pyproject.toml                    # Para gerenciamento de dependências e build (ex: com Poetry ou Hatch)
├── README.md
└── LICENSE
```

### 7. Arquivo `.gitignore` Proposto

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib60/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a parent folder of Double Commander
#  paths. Therefore, make sure you still get paths of Double Commander.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# poetry
poetry.lock
# poetry-dotenv
.env

# PEP 582; __pypackages__
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype
.pytype/

# Cython debug symbols
cython_debug/

# VS Code
.vscode/

# PyCharm
.idea/
*.iml
*.iws

# Sublime Text
*.sublime-project
*.sublime-workspace

# Atom
.atom/

# Eclipse
.project
.pydevproject
.settings/

# Logs and databases
*.log
*.sqlite
*.db
*.rdb
*.pid
*.pid.lock

# Temporary files
*.swp
*~
*.tmp
*.bak

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Fotix specific
backup_data/ # Se o diretório de backup padrão for local ao projeto (não recomendado para produção)
*.zip # Evitar adicionar acidentalmente arquivos ZIP de teste ao repo
fotix_config.json # Se o arquivo de configuração padrão for local ao projeto
```

### 8. Considerações de Segurança

1.  **Remoção Segura:** Utilizar `send2trash` garante que os arquivos sejam movidos para a lixeira do sistema em vez de serem permanentemente deletados, permitindo recuperação caso o backup falhe ou seja indesejado.
2.  **Validação de Input:**
    *   Caminhos de diretório fornecidos pelo usuário devem ser validados para existência e permissões adequadas antes do processamento.
    *   Pydantic `BaseModel` será usado para validar estruturas de dados lidas de arquivos de configuração ou metadados.
3.  **Tratamento de Erros:** Operações críticas de I/O (leitura, escrita, remoção, backup) devem ter tratamento de erro robusto (try-except blocos) com logging apropriado. A UI deve informar o usuário sobre falhas de forma clara.
4.  **Backup:** O sistema de backup automático antes da remoção é uma medida de segurança fundamental. O local do backup deve ser configurável e, idealmente, em um disco/partição diferente.
5.  **Permissões de Arquivo:** A aplicação deve rodar com os privilégios mínimos necessários. Cuidado ao criar diretórios de backup/log para não expor dados sensíveis com permissões muito abertas.
6.  **Hashing:** O uso de BLAKE3, um algoritmo de hashing criptograficamente seguro, garante a integridade da identificação de duplicatas, sendo resistente a colisões acidentais.
7.  **Sem execução arbitrária:** Evitar construir caminhos de execução ou comandos de sistema diretamente a partir de input do usuário não validado.

### 9. Justificativas e Trade-offs

*   **Arquitetura em Camadas:**
    *   **Prós:** Boa separação de responsabilidades, testabilidade, manutenibilidade. Padrão bem conhecido.
    *   **Contras:** Pode introduzir alguma verbosidade com a definição de interfaces e a passagem de dependências. Para aplicações muito pequenas, pode ser um overhead, mas para `Fotix` com sua complexidade, é justificado.
*   **Abstração da Infraestrutura:**
    *   **Prós:** Desacopla a lógica de negócio das bibliotecas específicas, facilitando a substituição de uma biblioteca (ex: trocar `send2trash` por outra coisa) ou o mocking em testes.
    *   **Contras:** Adiciona uma camada de indireção e a necessidade de manter as interfaces.
*   **Pydantic para Modelos:**
    *   **Prós:** Validação de dados em tempo de execução, ótima integração com type hints, serialização/desserialização fácil para JSON, auto-documentação.
    *   **Contras:** Adiciona uma dependência externa; performance marginalmente menor que `dataclasses` puras para cenários sem validação. Benefícios superam os contras aqui.
*   **Configuração via `__init__` (Injeção de Dependência):**
    *   **Prós:** Torna as dependências explícitas, melhora a testabilidade (fácil de injetar mocks), promove componentes mais coesos e desacoplados.
    *   **Contras:** Construtores podem ficar longos para componentes com muitas dependências (mas isso pode indicar que o componente tem responsabilidades demais).
*   **`src` layout:**
    *   **Prós:** Melhora a organização, evita problemas comuns de importação, padrão moderno para empacotamento.
    *   **Contras:** Ligeiramente diferente de layouts mais antigos, pode exigir pequeno ajuste para quem não está familiarizado.
*   **Limitado a Windows e ZIP na v1:**
    *   Simplifica o escopo inicial, permitindo focar na qualidade das funcionalidades chave. A arquitetura modular permite adicionar suporte a outros OS ou formatos de arquivo compactado no futuro com menor impacto.

### 10. Exemplo de Bootstrapping/Inicialização (Conceitual `src/fotix/main.py`)

```python
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from fotix.app_config import load_app_config, AppConfig
from fotix.ui.main_window import FotixMainWindow

# Importações de interfaces e implementações de serviços
from fotix.infrastructure.interfaces.logging import ILoggingService
from fotix.infrastructure.implementations.logging_service import LoggingService
from fotix.infrastructure.interfaces.file_system import IFileSystemService
from fotix.infrastructure.implementations.file_system_service import FileSystemService
from fotix.infrastructure.interfaces.hashing import IHashingService
from fotix.infrastructure.implementations.hashing_service import HashingService
from fotix.infrastructure.interfaces.zip import IZipService
from fotix.infrastructure.implementations.zip_service import ZipService
from fotix.infrastructure.interfaces.concurrency import IConcurrencyService
from fotix.infrastructure.implementations.concurrency_service import ConcurrencyService
from fotix.infrastructure.interfaces.backup import IBackupService
from fotix.infrastructure.implementations.backup_service import BackupService

from fotix.application.services.configuration_service import ConfigurationService
from fotix.application.services.scan_service import ScanService
from fotix.application.services.duplicate_management_service import DuplicateManagementService
from fotix.application.services.restore_service import RestoreService
from fotix.application.services.reporting_service import ReportingService

from fotix.domain.core.duplicate_finder import DuplicateFinderEngine
from fotix.domain.core.selection_strategy import DefaultSelectionStrategy # Exemplo de estratégia

def bootstrap_application():
    # 1. Carregar Configurações da Aplicação
    # (Pode envolver ler um arquivo de config, variáveis de ambiente, etc.)
    # Aqui, vamos assumir um AppConfig padrão ou carregado de um local fixo.
    app_config: AppConfig = load_app_config() # app_config.py define essa função

    # 2. Inicializar Serviços de Infraestrutura com suas configurações
    # O logger é fundamental e geralmente o primeiro a ser configurado
    logging_service: ILoggingService = LoggingService(
        log_file_path=app_config.log_settings.log_file_path,
        level=app_config.log_settings.log_level
    )
    logging_service.info("Fotix Application starting...")

    file_system_service: IFileSystemService = FileSystemService(logger=logging_service)
    hashing_service: IHashingService = HashingService(logger=logging_service)
    zip_service: IZipService = ZipService(logger=logging_service)
    concurrency_service: IConcurrencyService = ConcurrencyService(
        max_workers=app_config.performance_settings.max_workers,
        logger=logging_service
    )
    backup_service: IBackupService = BackupService(
        backup_root_path=app_config.backup_settings.backup_directory,
        logger=logging_service
    )

    # 3. Inicializar Componentes de Domínio (se precisarem de config ou dependências injetáveis)
    # Geralmente são mais "puros", mas podem precisar de serviços de infra via interface
    duplicate_finder_engine = DuplicateFinderEngine(
        hashing_service=hashing_service,
        file_system_service=file_system_service # Para get_file_size
    )
    selection_strategy = DefaultSelectionStrategy() # Pode ter suas próprias configs no futuro

    # 4. Inicializar Serviços de Aplicação, injetando dependências
    # O ConfigurationService pode ser o primeiro dos serviços de aplicação
    # para que outros possam usá-lo se necessário, embora aqui AppConfig já foi carregado.
    configuration_service = ConfigurationService(
        app_config=app_config, # Passa a configuração carregada
        file_system_service=file_system_service, # Para salvar config, se necessário
        logger=logging_service
    )

    scan_service = ScanService(
        file_system_service=file_system_service,
        zip_service=zip_service,
        concurrency_service=concurrency_service,
        duplicate_finder_engine=duplicate_finder_engine,
        logger=logging_service
    )

    duplicate_management_service = DuplicateManagementService(
        file_system_service=file_system_service,
        backup_service=backup_service,
        selection_strategy=selection_strategy,
        logger=logging_service
    )

    restore_service = RestoreService(
        file_system_service=file_system_service,
        backup_service=backup_service,
        logger=logging_service
    )

    reporting_service = ReportingService(
        logging_service=logging_service # Para buscar logs para a UI
    )

    # 5. Inicializar UI e injetar serviços da camada de aplicação
    app = QApplication(sys.argv)
    main_window = FotixMainWindow(
        scan_service=scan_service,
        duplicate_management_service=duplicate_management_service,
        restore_service=restore_service,
        reporting_service=reporting_service,
        configuration_service=configuration_service, # Para a UI acessar/modificar configurações
        logger=logging_service
    )
    main_window.show()

    logging_service.info("Fotix Application bootstrapped and UI shown.")
    sys.exit(app.exec())

if __name__ == "__main__":
    # Basic error handling for bootstrap phase
    try:
        bootstrap_application()
    except Exception as e:
        # Se o logger ainda não estiver configurado, printar para stderr
        # Idealmente, o logger é configurado o mais cedo possível
        # Em um app real, pode-se ter um logger muito básico para bootstrap errors.
        print(f"CRITICAL BOOTSTRAP ERROR: {e}", file=sys.stderr)
        # Tentar logar se o logger foi inicializado
        # (um logger global pode ser uma alternativa para esta fase)
        # if 'logging_service' in locals() and logging_service:
        # logging_service.critical(f"Application failed to bootstrap: {e}", exc_info=True)
        sys.exit(1)
```