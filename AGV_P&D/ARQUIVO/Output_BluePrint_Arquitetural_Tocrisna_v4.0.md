## AGV Prompt Template: Tocrisna v1.7 - Definição da Arquitetura Técnica - Fotix

## 1. Visão Geral da Arquitetura

A arquitetura proposta para o `Fotix` é uma **Arquitetura em Camadas (Layered Architecture)**. Esta abordagem foi escolhida por sua clareza, modularidade, facilidade de manutenção e testabilidade. Ela promove uma forte separação de responsabilidades, onde cada camada tem um papel distinto e se comunica com as camadas adjacentes através de interfaces bem definidas.

As camadas principais serão:

1.  **Camada de Apresentação (UI - User Interface):** Responsável pela interação com o usuário, construída com PySide6.
2.  **Camada de Aplicação (Application):** Orquestra os casos de uso, atuando como um intermediário entre a UI e o Core/Domínio. Contém os serviços de aplicação.
3.  **Camada de Domínio/Core (Core):** Contém a lógica de negócios principal, as regras de identificação de duplicatas e seleção de arquivos. Inclui os modelos de domínio.
4.  **Camada de Infraestrutura (Infrastructure):** Lida com preocupações transversais e interações com o sistema operacional, como acesso a arquivos, concorrência, logging, e manipulação de ZIP. Abstrai as bibliotecas de baixo nível.

Esta estrutura facilita a substituição de componentes (ex: a UI ou um mecanismo de persistência específico, se necessário no futuro) com impacto mínimo nas outras camadas.

## 2. Diagrama de Componentes (Simplificado)

```mermaid
graph TD
    subgraph Camada de Apresentação (UI)
        UI_MainWindow["FotixMainWindow (PySide6)"]
        UI_SettingsView["SettingsView"]
        UI_ScanProgressView["ScanProgressView"]
        UI_ResultsView["ResultsView"]
        UI_BackupRestoreView["BackupRestoreView"]
    end

    subgraph Camada de Aplicação
        App_ScanService["ScanOrchestrationService"]
        App_BackupRestoreService["BackupRestoreService"]
        App_ReportingService["ReportingService"]
        App_ConfigurationService["ConfigurationService (leitura)"]
    end

    subgraph Camada de Domínio/Core
        Core_DuplicateFinder["DuplicateFinderAlgorithm"]
        Core_FileAnalyzer["FileAnalyzer"]
        Core_DecisionEngine["DecisionEngine"]
        Domain_Models["DomainModels (FileInfo, DuplicateGroup, ScanSettings, etc.)"]
    end

    subgraph Camada de Infraestrutura
        Infra_FileSystem["FileSystemService"]
        Infra_ZipHandler["ZipHandlerService"]
        Infra_Hashing["HashingService"]
        Infra_Concurrency["ConcurrencyService"]
        Infra_Backup["BackupManagerService"]
        Infra_Logging["LoggingService"]
        Infra_ConfigLoader["ConfigLoader"]
    end

    %% UI Dependencies
    UI_MainWindow --> App_ScanService
    UI_MainWindow --> App_BackupRestoreService
    UI_MainWindow --> App_ReportingService
    UI_MainWindow --> App_ConfigurationService

    %% Application Layer Dependencies
    App_ScanService --> Core_FileAnalyzer
    App_ScanService --> Core_DuplicateFinder
    App_ScanService --> Core_DecisionEngine
    App_ScanService --> Domain_Models
    App_ScanService --> Infra_FileSystem
    App_ScanService --> Infra_ZipHandler
    App_ScanService --> Infra_Hashing
    App_ScanService --> Infra_Concurrency
    App_ScanService --> Infra_Backup
    App_ScanService --> Infra_Logging

    App_BackupRestoreService --> Infra_Backup
    App_BackupRestoreService --> Infra_Logging

    App_ReportingService --> Infra_Logging

    App_ConfigurationService --> Infra_ConfigLoader

    %% Core Layer Dependencies
    Core_FileAnalyzer --> Infra_Hashing
    Core_FileAnalyzer --> Infra_FileSystem  %% Para get_size
    Core_FileAnalyzer --> Infra_ZipHandler  %% Para ler conteúdo de arquivos dentro de ZIPs
    Core_FileAnalyzer --> Domain_Models

    Core_DuplicateFinder --> Domain_Models

    Core_DecisionEngine --> Domain_Models

    %% Infrastructure Layer Dependencies
    Infra_FileSystem --> Python_Libs_FS["(pathlib, shutil, send2trash)"]
    Infra_ZipHandler --> Python_Libs_ZIP["(stream-unzip)"]
    Infra_Hashing --> Python_Libs_Hash["(blake3)"]
    Infra_Concurrency --> Python_Libs_Conc["(concurrent.futures)"]
    Infra_Backup --> Infra_FileSystem

    %% Styling
    classDef ui fill:#D6EAF8,stroke:#333,stroke-width:2px;
    classDef app fill:#D1F2EB,stroke:#333,stroke-width:2px;
    classDef core fill:#FCF3CF,stroke:#333,stroke-width:2px;
    classDef infra fill:#FDEDEC,stroke:#333,stroke-width:2px;
    classDef ext fill:# мнение,stroke:#333,stroke-width:2px;

    class UI_MainWindow,UI_SettingsView,UI_ScanProgressView,UI_ResultsView,UI_BackupRestoreView ui;
    class App_ScanService,App_BackupRestoreService,App_ReportingService,App_ConfigurationService app;
    class Core_DuplicateFinder,Core_FileAnalyzer,Core_DecisionEngine,Domain_Models core;
    class Infra_FileSystem,Infra_ZipHandler,Infra_Hashing,Infra_Concurrency,Infra_Backup,Infra_Logging,Infra_ConfigLoader infra;
    class Python_Libs_FS,Python_Libs_ZIP,Python_Libs_Hash,Python_Libs_Conc ext;
```

## 3. Descrição dos Componentes/Módulos

### 3.1. Camada de Apresentação (UI) - `fotix.ui`

Responsável por toda a interação com o usuário. Construída com PySide6.

*   **`fotix.ui.main_window.FotixMainWindow`**
    *   **Responsabilidade:** Janela principal da aplicação, orquestra as diferentes views e interações com os serviços da camada de aplicação.
    *   **Tecnologias:** PySide6.
    *   **Dependências Diretas:**
        *   `fotix.ui.views.settings_view.SettingsView`
        *   `fotix.ui.views.scan_progress_view.ScanProgressView`
        *   `fotix.ui.views.results_view.ResultsView`
        *   `fotix.ui.views.backup_restore_view.BackupRestoreView`
        *   `fotix.application.services.scan_orchestration_service.ScanOrchestrationService`
        *   `fotix.application.services.backup_restore_service.BackupRestoreService`
        *   `fotix.application.services.reporting_service.ReportingService`
        *   `fotix.application.services.configuration_service.ConfigurationService`
        *   `fotix.ui.models` (View models, se necessário)

*   **`fotix.ui.views.settings_view.SettingsView`** (Componente de UI)
    *   **Propósito:** Permitir ao usuário configurar os diretórios a serem escaneados, arquivos ZIP, e potencialmente critérios de decisão.
    *   **Interage com:** `ConfigurationService` (para carregar/salvar configurações), `ScanOrchestrationService` (para iniciar uma varredura com as configurações fornecidas).
    *   **Unidade de Trabalho:** Relativamente independente, focada na coleta de input do usuário para a varredura.

*   **`fotix.ui.views.scan_progress_view.ScanProgressView`** (Componente de UI)
    *   **Propósito:** Exibir o progresso da varredura (arquivos processados, duplicatas encontradas), permitir cancelamento.
    *   **Interage com:** `ScanOrchestrationService` (para receber atualizações de progresso e enviar comandos de cancelamento).
    *   **Unidade de Trabalho:** Dependente de um processo de varredura ativo.

*   **`fotix.ui.views.results_view.ResultsView`** (Componente de UI)
    *   **Propósito:** Apresentar os grupos de arquivos duplicados encontrados, mostrando qual será mantido e quais serão removidos. Permitir ao usuário inspecionar (e opcionalmente, no futuro, sobrescrever decisões).
    *   **Interage com:** `ScanOrchestrationService` (para obter os resultados), `ReportingService` (para gerar relatórios).
    *   **Unidade de Trabalho:** Focada na apresentação dos resultados pós-varredura.

*   **`fotix.ui.views.backup_restore_view.BackupRestoreView`** (Componente de UI)
    *   **Propósito:** Listar os backups disponíveis e permitir ao usuário selecionar arquivos/pastas para restauração.
    *   **Interage com:** `BackupRestoreService`.
    *   **Unidade de Trabalho:** Relativamente independente, focada na gestão de backups.

*   **`fotix.ui.models` (Opcional, ex: `fotix.ui.view_models`)**
    *   **Responsabilidade:** Conter classes de dados específicas para a UI, adaptando modelos de domínio para exibição ou coletando dados de formulários.
    *   **Tecnologias:** Dataclasses, Pydantic (se validação for útil aqui).
    *   **Dependências Diretas:** `fotix.domain.models` (potencialmente).

### 3.2. Camada de Aplicação - `fotix.application`

Orquestra os casos de uso e coordena os componentes do Core e da Infraestrutura.

*   **`fotix.application.services.scan_orchestration_service.ScanOrchestrationService`**
    *   **Responsabilidade:** Gerenciar todo o fluxo de varredura: receber configurações da UI, coordenar a análise de arquivos, detecção de duplicatas, decisão de qual manter/remover, execução da remoção com backup, e notificar a UI sobre o progresso e resultados.
    *   **Tecnologias:** Python.
    *   **Dependências Diretas:**
        *   `fotix.core.file_analyzer.FileAnalyzer`
        *   `fotix.core.duplicate_finder.DuplicateFinderAlgorithm`
        *   `fotix.core.decision_engine.DecisionEngine`
        *   `fotix.domain.models`
        *   `fotix.infrastructure.file_system.FileSystemService`
        *   `fotix.infrastructure.zip_handler.ZipHandlerService`
        *   `fotix.infrastructure.hashing.HashingService`
        *   `fotix.infrastructure.concurrency.ConcurrencyService`
        *   `fotix.infrastructure.backup_manager.BackupManagerService`
        *   `fotix.infrastructure.logging.LoggingService`

*   **`fotix.application.services.backup_restore_service.BackupRestoreService`**
    *   **Responsabilidade:** Lidar com as operações de listagem de backups e restauração de arquivos a partir dos backups.
    *   **Tecnologias:** Python.
    *   **Dependências Diretas:**
        *   `fotix.infrastructure.backup_manager.BackupManagerService`
        *   `fotix.infrastructure.logging.LoggingService`
        *   `fotix.domain.models` (para estruturas de dados de backup/restauração, se necessário)

*   **`fotix.application.services.reporting_service.ReportingService`**
    *   **Responsabilidade:** Gerar relatórios resumidos e estatísticas pós-processamento com base nos resultados da varredura.
    *   **Tecnologias:** Python.
    *   **Dependências Diretas:**
        *   `fotix.domain.models` (para consumir `ScanResult`)
        *   `fotix.infrastructure.logging.LoggingService`
        *   `fotix.infrastructure.file_system.FileSystemService` (para salvar relatórios)

*   **`fotix.application.services.configuration_service.ConfigurationService`**
    *   **Responsabilidade:** Fornecer uma interface para a UI (e outros serviços, se necessário) acessarem as configurações da aplicação (ex: último diretório escaneado, preferências de decisão, caminho do backup). Não lida com a persistência, apenas com o acesso.
    *   **Tecnologias:** Python.
    *   **Dependências Diretas:**
        *   `fotix.infrastructure.config_loader.ConfigLoader`
        *   `fotix.domain.models` (para `AppConfig` dataclass)

### 3.3. Camada de Domínio/Core - `fotix.core` e `fotix.domain`

Contém a lógica de negócios pura e os modelos de dados centrais.

*   **`fotix.core.file_analyzer.FileAnalyzer`**
    *   **Responsabilidade:** Analisar arquivos individuais para extrair metadados relevantes (tamanho, data de criação, resolução - se imagem/vídeo) e calcular seu hash. Lida com a leitura de arquivos normais e arquivos dentro de ZIPs (usando `ZipHandlerService`).
    *   **Tecnologias:** Python.
    *   **Dependências Diretas:**
        *   `fotix.infrastructure.hashing.HashingService`
        *   `fotix.infrastructure.file_system.FileSystemService` (para `get_size`, etc.)
        *   `fotix.infrastructure.zip_handler.ZipHandlerService`
        *   `fotix.domain.models.FileInfo`
        *   `fotix.utils.media_parser` (um novo utilitário para metadados de imagem/vídeo, ex: usando `Pillow`, `opencv-python-headless` ou `hachoir`)

*   **`fotix.core.duplicate_finder.DuplicateFinderAlgorithm`**
    *   **Responsabilidade:** Receber uma lista de `FileInfo` (com hashes e tamanhos), identificar e agrupar arquivos idênticos (duplicatas). Implementa a pré-filtragem por tamanho.
    *   **Tecnologias:** Python.
    *   **Dependências Diretas:**
        *   `fotix.domain.models.FileInfo`
        *   `fotix.domain.models.DuplicateGroup`

*   **`fotix.core.decision_engine.DecisionEngine`**
    *   **Responsabilidade:** Aplicar a lógica inteligente para decidir qual arquivo manter de um `DuplicateGroup`, com base nos critérios definidos (resolução, data, nome do arquivo).
    *   **Tecnologias:** Python.
    *   **Dependências Diretas:**
        *   `fotix.domain.models.FileInfo`
        *   `fotix.domain.models.DuplicateGroup`

*   **`fotix.domain.models`** (Módulo contendo dataclasses/Pydantic models)
    *   **Responsabilidade:** Definir as estruturas de dados centrais usadas em toda a aplicação.
        *   `FileInfo(path: Path, size: int, creation_date: datetime, modification_date: datetime, file_hash: str, resolution: Optional[Tuple[int, int]], is_in_zip: bool, zip_path: Optional[Path])`
        *   `DuplicateGroup(files: List[FileInfo], file_to_keep: Optional[FileInfo], files_to_remove: List[FileInfo])`
        *   `ScanSettings(paths_to_scan: List[Path], zip_files_to_scan: List[Path], decision_criteria_weights: Dict[str, float])`
        *   `ScanResult(processed_files_count: int, duplicate_groups_found: List[DuplicateGroup], total_space_saved: int, errors: List[str])`
        *   `AppConfig(backup_directory: Path, log_level: str, ...)`
        *   `BackupLogEntry(original_path: Path, backup_path: Path, timestamp: datetime)`
    *   **Tecnologias:** Python Dataclasses (ou Pydantic para validação embutida).
    *   **Dependências Diretas:** `pathlib`, `datetime` (stdlib).

### 3.4. Camada de Infraestrutura - `fotix.infrastructure`

Abstrai as interações com o sistema operacional e bibliotecas de terceiros.

*   **`fotix.infrastructure.file_system.FileSystemService`**
    *   **Responsabilidade:** Abstrair operações de sistema de arquivos (listar arquivos, obter tamanho, ler, mover, deletar de forma segura).
    *   **Tecnologias:** `pathlib`, `shutil`, `send2trash`, `os`.
    *   **Dependências Diretas:** Nenhuma (usa bibliotecas padrão/terceiros diretamente).

*   **`fotix.infrastructure.zip_handler.ZipHandlerService`**
    *   **Responsabilidade:** Abstrair a leitura e extração progressiva de arquivos ZIP.
    *   **Tecnologias:** `stream-unzip`.
    *   **Dependências Diretas:** Nenhuma (usa `stream-unzip` diretamente).

*   **`fotix.infrastructure.hashing.HashingService`**
    *   **Responsabilidade:** Abstrair o cálculo de hash de arquivos.
    *   **Tecnologias:** `blake3`.
    *   **Dependências Diretas:** Nenhuma (usa `blake3` diretamente).

*   **`fotix.infrastructure.concurrency.ConcurrencyService`**
    *   **Responsabilidade:** Abstrair a execução paralela de tarefas.
    *   **Tecnologias:** `concurrent.futures`.
    *   **Dependências Diretas:** Nenhuma (usa `concurrent.futures` diretamente).

*   **`fotix.infrastructure.backup_manager.BackupManagerService`**
    *   **Responsabilidade:** Gerenciar o backup de arquivos antes da remoção e a restauração a partir desses backups. Mantém um log/índice dos arquivos em backup.
    *   **Tecnologias:** Python, `json` (para log/índice simples).
    *   **Dependências Diretas:**
        *   `fotix.infrastructure.file_system.FileSystemService`
        *   `fotix.domain.models.BackupLogEntry`

*   **`fotix.infrastructure.logging.LoggingService`**
    *   **Responsabilidade:** Configurar e fornecer uma interface para logging em toda a aplicação.
    *   **Tecnologias:** `logging` (stdlib).
    *   **Dependências Diretas:** Nenhuma (usa `logging` diretamente).

*   **`fotix.infrastructure.config_loader.ConfigLoader`**
    *   **Responsabilidade:** Carregar e persistir configurações da aplicação (ex: de um arquivo JSON ou INI).
    *   **Tecnologias:** Python, `json` ou `configparser`.
    *   **Dependências Diretas:**
        *   `fotix.domain.models.AppConfig`
        *   `fotix.infrastructure.file_system.FileSystemService` (para ler/escrever arquivo de config)

### 3.5. Utilitários - `fotix.utils`

*   **`fotix.utils.media_parser`**
    *   **Responsabilidade:** Extrair metadados específicos de mídia, como resolução de imagens e vídeos.
    *   **Tecnologias:** `Pillow` (para imagens), `opencv-python-headless` ou `hachoir` (para vídeos e outros formatos, se necessário).
    *   **Dependências Diretas:** Nenhuma (usa bibliotecas de terceiros diretamente).
    *   *Nota:* A escolha da biblioteca para análise de vídeo pode precisar de mais pesquisa para garantir leveza e compatibilidade com Windows sem dependências pesadas. `hachoir` é uma boa candidata por ser Python puro.

## 4. Definição das Interfaces Principais (Contratos Funcionais)

Exemplos chave, seguindo a Diretriz 3. Usaremos dataclasses para DTOs.

---

**`fotix.domain.models.py` (Exemplos de Estruturas de Dados)**

```python
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple, Dict
from datetime import datetime

@dataclass
class FileInfo:
    path: Path
    size: int
    creation_date: datetime
    modification_date: datetime
    file_hash: Optional[str] = None # Calculado posteriormente
    resolution: Optional[Tuple[int, int]] = None # (width, height)
    is_in_zip: bool = False
    zip_path: Optional[Path] = None
    entry_name_in_zip: Optional[str] = None # Nome do arquivo dentro do ZIP

@dataclass
class DuplicateGroup:
    key_hash: str # Hash comum ao grupo
    files: List[FileInfo]
    file_to_keep: Optional[FileInfo] = None
    files_to_remove: List[FileInfo] = field(default_factory=list)

@dataclass
class ScanSettings:
    paths_to_scan: List[Path]
    zip_files_to_scan: List[Path]
    # Exemplo: {'resolution': 0.5, 'creation_date': 0.3, 'name_pattern': 0.2}
    decision_criteria_weights: Dict[str, float]
    # Callback para progresso: (processed_count, total_count, current_file_path)
    progress_callback: Optional[callable] = None
    # Callback para quando um grupo de duplicatas é totalmente processado (identificado, decidido)
    # (DuplicateGroup)
    duplicate_group_processed_callback: Optional[callable] = None
    # Callback para erro durante processamento de arquivo
    # (file_path, error_message)
    file_error_callback: Optional[callable] = None


@dataclass
class ScanResult:
    processed_files_count: int
    identified_duplicate_groups: List[DuplicateGroup]
    total_space_to_be_saved: int = 0 # Calculado após decisão
    errors_log: List[str] = field(default_factory=list)

@dataclass
class AppConfig:
    backup_directory: Path = Path.home() / ".fotix" / "backups"
    log_level: str = "INFO"
    log_file_path: Path = Path.home() / ".fotix" / "fotix.log"
    max_concurrent_workers: Optional[int] = None # None para default de ThreadPoolExecutor

@dataclass
class BackupLogEntry:
    original_path: Path
    backup_path: Path
    timestamp: datetime
    metadata: Dict[str, any] # Para armazenar informações adicionais se necessário
```

---

**`fotix.infrastructure.file_system.FileSystemService` (Interface e Implementação)**

```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Iterator, Union, IO

class IFileSystemService(ABC):
    @abstractmethod
    def get_size(self, path: Path) -> int:
        """Retorna o tamanho de um arquivo em bytes."""
        pass

    @abstractmethod
    def file_exists(self, path: Path) -> bool:
        """Verifica se um arquivo ou diretório existe."""
        pass

    @abstractmethod
    def list_files_recursive(self, dir_path: Path, extensions: Optional[List[str]] = None) -> Iterator[Path]:
        """Lista todos os arquivos recursivamente em um diretório, opcionalmente filtrando por extensões."""
        pass

    @abstractmethod
    def read_file_chunks(self, path: Path, chunk_size: int = 8192) -> Iterator[bytes]:
        """Lê um arquivo em chunks."""
        pass

    @abstractmethod
    def move_file(self, source: Path, destination: Path) -> None:
        """Move um arquivo."""
        pass

    @abstractmethod
    def delete_file_safe(self, path: Path) -> None:
        """Remove um arquivo para a lixeira."""
        pass

    @abstractmethod
    def create_directory(self, path: Path, parents: bool = True, exist_ok: bool = True) -> None:
        """Cria um diretório."""
        pass

    @abstractmethod
    def write_text_file(self, path: Path, content: str) -> None:
        """Escreve conteúdo textual em um arquivo."""
        pass

    @abstractmethod
    def read_text_file(self, path: Path) -> str:
        """Lê conteúdo textual de um arquivo."""
        pass

# Implementação (em fotix/infrastructure/file_system_impl.py ou similar)
# import os, shutil, send2trash, pathlib
# class FileSystemService(IFileSystemService):
#     def __init__(self, logger: LoggingService): # Exemplo de injeção de config/dependência
#         self.logger = logger
#     # ... implementações usando pathlib, shutil, send2trash ...
```

---

**`fotix.infrastructure.zip_handler.ZipHandlerService` (Interface e Implementação)**

```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator, Tuple, IO, ContextManager

class IZipHandlerService(ABC):
    @abstractmethod
    def list_zip_contents_metadata(self, zip_path: Path, extensions: Optional[List[str]] = None) -> Iterator[Tuple[str, int, datetime]]:
        """
        Lista metadados de entradas (nome, tamanho, data modif.) em um arquivo ZIP,
        opcionalmente filtrando por extensões.
        Retorna iterador de (entry_name, size, modification_date).
        """
        pass

    @abstractmethod
    def stream_unzip_file_content(self, zip_path: Path, entry_name: str) -> ContextManager[IO[bytes]]:
        """
        Fornece um stream de leitura para o conteúdo de um arquivo específico dentro de um ZIP.
        Usa stream-unzip para eficiência de memória.
        """
        pass

# Implementação (em fotix/infrastructure/zip_handler_impl.py ou similar)
# import stream_unzip
# class ZipHandlerService(IZipHandlerService):
#    def __init__(self, logger: LoggingService):
#        self.logger = logger
#    # ... implementações usando stream-unzip ...
```

---

**`fotix.infrastructure.hashing.HashingService` (Interface e Implementação)**

```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import IO, Iterator

class IHashingService(ABC):
    @abstractmethod
    def calculate_hash_from_stream(self, stream: IO[bytes]) -> str:
        """Calcula o hash BLAKE3 de um stream de bytes."""
        pass

    @abstractmethod
    def calculate_hash_from_path(self, file_path: Path, file_system_service: IFileSystemService) -> str:
        """Calcula o hash BLAKE3 de um arquivo no disco (usando FileSystemService para ler em chunks)."""
        pass

# Implementação (em fotix/infrastructure/hashing_impl.py ou similar)
# import blake3
# class HashingService(IHashingService):
#    def __init__(self, logger: LoggingService):
#        self.logger = logger
#    # ... implementações usando blake3 ...
```
---
**`fotix.infrastructure.concurrency.ConcurrencyService` (Interface e Implementação)**
```python
from abc import ABC, abstractmethod
from typing import Callable, List, Any, Iterator, Optional
from concurrent.futures import Future

class IConcurrencyService(ABC):
    @abstractmethod
    def run_tasks_parallel(self, tasks_with_args: List[Tuple[Callable, List[Any]]]) -> List[Any]:
        """
        Executa uma lista de callables (com seus argumentos) em paralelo e retorna os resultados na ordem.
        """
        pass

    @abstractmethod
    def map_parallel(self, func: Callable, iterables: Iterator[Any]) -> Iterator[Any]:
        """
        Aplica uma função a cada item de um iterável em paralelo, similar ao map(), mas concorrente.
        """
        pass

# Implementação (em fotix/infrastructure/concurrency_impl.py ou similar)
# from concurrent.futures import ThreadPoolExecutor
# class ConcurrencyService(IConcurrencyService):
#    def __init__(self, max_workers: Optional[int] = None, logger: LoggingService):
#        self.max_workers = max_workers
#        self.logger = logger
#    # ... implementações usando ThreadPoolExecutor ...
```
---
**`fotix.infrastructure.backup_manager.BackupManagerService` (Interface e Implementação)**
```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

# from fotix.domain.models import FileInfo, BackupLogEntry (já definidos)

class IBackupManagerService(ABC):
    @abstractmethod
    def initialize_backup_location(self) -> None:
        """Garante que o local de backup exista."""
        pass

    @abstractmethod
    def backup_file(self, file_info: FileInfo) -> Path:
        """
        Cria um backup seguro do arquivo.
        Retorna o caminho para o arquivo no backup.
        Registra a operação de backup.
        """
        pass

    @abstractmethod
    def restore_file(self, backup_entry_id: str, target_path: Optional[Path] = None) -> Path:
        """
        Restaura um arquivo do backup para seu local original ou um novo local.
        Retorna o caminho do arquivo restaurado.
        """
        pass

    @abstractmethod
    def list_backups(self) -> List[BackupLogEntry]:
        """Lista os arquivos atualmente em backup."""
        pass

    @abstractmethod
    def get_backup_entry(self, original_path: Path) -> Optional[BackupLogEntry]:
        """Recupera um registro de backup pelo caminho original."""
        pass

# Implementação (em fotix/infrastructure/backup_manager_impl.py)
# import json
# class BackupManagerService(IBackupManagerService):
#    def __init__(self, backup_root_dir: Path, file_system_service: IFileSystemService, logger: LoggingService):
#        self.backup_root_dir = backup_root_dir
#        self.backup_log_file = backup_root_dir / "backup_log.json"
#        self.file_system_service = file_system_service
#        self.logger = logger
#        self.initialize_backup_location()
#    # ... implementações ...
```
---
**`fotix.core.file_analyzer.FileAnalyzer` (Classe, não interface pura, mas com contrato claro)**
```python
# from fotix.domain.models import FileInfo
# from fotix.infrastructure.hashing import IHashingService
# from fotix.infrastructure.file_system import IFileSystemService
# from fotix.infrastructure.zip_handler import IZipHandlerService
# from fotix.utils.media_parser import MediaMetadata # Supondo um dataclass para metadados

class FileAnalyzer:
    def __init__(self,
                 hashing_service: IHashingService,
                 file_system_service: IFileSystemService,
                 zip_handler_service: IZipHandlerService,
                 # media_parser_service: IMediaParserService, # Se abstraído
                 logger: LoggingService):
        self.hashing_service = hashing_service
        self.file_system_service = file_system_service
        self.zip_handler_service = zip_handler_service
        # self.media_parser_service = media_parser_service
        self.logger = logger


    def analyze_disk_file(self, file_path: Path) -> FileInfo:
        """Analisa um arquivo do disco, calcula hash e extrai metadados."""
        # ... lógica usando os serviços injetados ...
        # size = self.file_system_service.get_size(file_path)
        # file_hash = self.hashing_service.calculate_hash_from_path(file_path, self.file_system_service)
        # resolution = self._get_media_resolution(file_path) # Usaria media_parser
        # return FileInfo(...)
        pass

    def analyze_zip_entry_content(self, zip_path: Path, entry_name: str, entry_size: int, entry_mod_date: datetime) -> FileInfo:
        """
        Analisa o conteúdo de uma entrada de ZIP, calcula hash e extrai metadados.
        Usa zip_handler_service.stream_unzip_file_content e hashing_service.calculate_hash_from_stream.
        """
        # with self.zip_handler_service.stream_unzip_file_content(zip_path, entry_name) as stream:
        #     file_hash = self.hashing_service.calculate_hash_from_stream(stream)
        #     stream.seek(0) # Reset stream if media_parser needs to read it too (or pass bytes)
        #     # resolution = self._get_media_resolution_from_stream(stream, entry_name)
        # return FileInfo(path=zip_path, ..., is_in_zip=True, zip_path=zip_path, entry_name_in_zip=entry_name)
        pass
```
---
**`fotix.application.services.scan_orchestration_service.ScanOrchestrationService`**
```python
# from fotix.domain.models import ScanSettings, ScanResult, FileInfo, DuplicateGroup
# from fotix.core.file_analyzer import FileAnalyzer
# from fotix.core.duplicate_finder import DuplicateFinderAlgorithm
# from fotix.core.decision_engine import DecisionEngine
# from fotix.infrastructure.services import (
#    IFileSystemService, IZipHandlerService, IConcurrencyService,
#    IBackupManagerService, ILoggingService
# )

class ScanOrchestrationService:
    def __init__(self,
                 file_analyzer: FileAnalyzer,
                 duplicate_finder: DuplicateFinderAlgorithm,
                 decision_engine: DecisionEngine,
                 file_system_service: IFileSystemService,
                 zip_handler_service: IZipHandlerService,
                 concurrency_service: IConcurrencyService,
                 backup_manager_service: IBackupManagerService,
                 logging_service: ILoggingService):
        # ... atribuição das dependências ...
        self.file_analyzer = file_analyzer
        # ... etc ...

    def perform_scan(self, settings: ScanSettings) -> ScanResult:
        """
        Orquestra o processo completo de varredura.
        1. Lista arquivos de diretórios e ZIPs (usando FileSystemService, ZipHandlerService).
        2. Para cada arquivo/entrada de ZIP:
           a. Pré-filtra por tamanho (se já existe outro arquivo com mesmo tamanho).
           b. Analisa (calcula hash, metadados) usando FileAnalyzer (paralelizado por ConcurrencyService).
           c. Envia FileInfo para o DuplicateFinder.
        3. DuplicateFinder agrupa duplicatas.
        4. Para cada grupo de duplicatas:
           a. DecisionEngine escolhe qual manter.
           b. Envia para callbacks de progresso/resultados.
        5. Retorna ScanResult.
        """
        # ... implementação ...
        # Notificar UI via settings.progress_callback e settings.duplicate_group_processed_callback
        pass

    def process_duplicates_for_removal(self, duplicate_groups: List[DuplicateGroup]) -> Tuple[int, int]:
        """
        Processa os grupos de duplicatas marcados para remoção.
        Para cada arquivo a ser removido:
        1. Faz backup usando BackupManagerService.
        2. Remove usando FileSystemService.delete_file_safe().
        Retorna (total_files_removed, total_space_saved).
        """
        # ... implementação ...
        pass
```

**Configuração e Construção de Componentes:**
A configuração de cada serviço (ex: `backup_root_dir` para `BackupManagerService`, `max_workers` para `ConcurrencyService`) será passada através de seus construtores (`__init__`).
O `main.py` (ou um `bootstrap.py`) será responsável por:
1.  Carregar a configuração geral da aplicação usando `ConfigLoader` (ex: de `fotix_config.json`).
2.  Instanciar os serviços da camada de Infraestrutura, passando os parâmetros de configuração relevantes.
3.  Instanciar os componentes da camada Core, injetando os serviços de infraestrutura necessários.
4.  Instanciar os serviços da camada de Aplicação, injetando os componentes Core e serviços de infraestrutura.
5.  Instanciar a UI, injetando os serviços da camada de Aplicação.

Exemplo de inicialização (simplificado) no `main.py`:
```python
# main.py
from fotix.infrastructure.logging_impl import LoggingService
from fotix.infrastructure.config_loader_impl import ConfigLoader
from fotix.infrastructure.file_system_impl import FileSystemService
# ... outras importações de implementações ...
from fotix.application.services.scan_orchestration_service import ScanOrchestrationService
from fotix.ui.main_window import FotixMainWindow
# ...

def main():
    # 1. Configuração inicial
    base_config_path = Path.home() / ".fotix"
    
    # Logger primeiro
    # Idealmente, o path do log viria da config, mas para iniciar o logger, podemos ter um default
    initial_log_path = base_config_path / "fotix_init.log" 
    logging_service = LoggingService(log_file_path=initial_log_path, level="DEBUG") # Nível alto para bootstrap
    
    # Carregar configuração da aplicação
    config_loader = ConfigLoader(default_config_dir=base_config_path, logger=logging_service)
    app_config = config_loader.load_config(config_file_name="app_settings.json", default_config_model=AppConfig())
    
    # Reconfigurar logger com base na config carregada, se necessário
    logging_service.configure(log_file_path=app_config.log_file_path, level=app_config.log_level)
    
    # 2. Instanciar Serviços de Infraestrutura
    file_system_svc = FileSystemService(logger=logging_service)
    zip_handler_svc = ZipHandlerService(logger=logging_service)
    hashing_svc = HashingService(logger=logging_service)
    concurrency_svc = ConcurrencyService(max_workers=app_config.max_concurrent_workers, logger=logging_service)
    backup_manager_svc = BackupManagerService(
        backup_root_dir=app_config.backup_directory,
        file_system_service=file_system_svc,
        logger=logging_service
    )
    # ... outros serviços de infra ...

    # 3. Instanciar Componentes Core
    file_analyzer = FileAnalyzer(
        hashing_service=hashing_svc,
        file_system_service=file_system_svc,
        zip_handler_service=zip_handler_svc,
        logger=logging_service
    )
    duplicate_finder = DuplicateFinderAlgorithm(logger=logging_service) # Logger pode ser útil
    decision_engine = DecisionEngine(logger=logging_service)

    # 4. Instanciar Serviços de Aplicação
    scan_service = ScanOrchestrationService(
        file_analyzer=file_analyzer,
        duplicate_finder=duplicate_finder,
        decision_engine=decision_engine,
        file_system_service=file_system_svc,
        zip_handler_service=zip_handler_svc,
        concurrency_service=concurrency_svc,
        backup_manager_service=backup_manager_svc,
        logging_service=logging_service
    )
    backup_restore_service = BackupRestoreService(
        backup_manager_service=backup_manager_svc,
        logging_service=logging_service
    )
    # ... outros serviços de app ...
    app_configuration_service = ConfigurationService(config_loader=config_loader, current_config=app_config)


    # 5. Instanciar e Rodar UI
    app = QApplication(sys.argv)
    main_window = FotixMainWindow(
        scan_service=scan_service,
        backup_restore_service=backup_restore_service,
        # reporting_service=...
        configuration_service=app_configuration_service,
        logging_service=logging_service
    )
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

## 5. Gerenciamento de Dados

*   **Dados de Configuração da Aplicação:** Serão gerenciados pelo `ConfigLoader` e persistidos em um arquivo local (ex: `~/.fotix/app_settings.json`). O `ConfigurationService` provê acesso a essa configuração.
*   **Dados de Backup:** O `BackupManagerService` gerenciará os arquivos de backup em um diretório dedicado (configurável, ex: `~/.fotix/backups/`). Um arquivo de índice/log (ex: `backup_log.json`) dentro deste diretório manterá o mapeamento entre arquivos originais e seus backups, incluindo metadados como timestamp.
*   **Dados de Sessão de Varredura (Resultados):** Os resultados da varredura (`ScanResult`, contendo `DuplicateGroup`, `FileInfo`) são primariamente mantidos em memória durante a execução da UI para exibição e processamento.
*   **Logs:** Gerenciados pelo `LoggingService` e escritos em um arquivo de log (ex: `~/.fotix/fotix.log`).
*   **Relatórios:** Gerados pelo `ReportingService` e salvos como arquivos (ex: TXT, CSV, ou futuramente HTML) em um local escolhido pelo usuário ou um diretório padrão.

Não há necessidade de banco de dados externo, conforme as restrições.

## 6. Estrutura de Diretórios Proposta (Layout `src`)

```
fotix-project/
├── src/
│   └── fotix/
│       ├── __init__.py
│       ├── main.py                 # Ponto de entrada da aplicação, bootstrapping
│       │
│       ├── ui/                     # Camada de Apresentação (PySide6)
│       │   ├── __init__.py
│       │   ├── main_window.py
│       │   ├── views/
│       │   │   ├── __init__.py
│       │   │   ├── settings_view.py
│       │   │   ├── scan_progress_view.py
│       │   │   ├── results_view.py
│       │   │   └── backup_restore_view.py
│       │   ├── widgets/            # Componentes de UI reutilizáveis
│       │   │   └── __init__.py
│       │   └── models/             # ViewModels, se necessário
│       │       └── __init__.py
│       │
│       ├── application/            # Camada de Aplicação
│       │   ├── __init__.py
│       │   └── services/
│       │       ├── __init__.py
│       │       ├── scan_orchestration_service.py
│       │       ├── backup_restore_service.py
│       │       ├── reporting_service.py
│       │       └── configuration_service.py
│       │
│       ├── core/                   # Camada de Domínio/Core (lógica de negócio)
│       │   ├── __init__.py
│       │   ├── file_analyzer.py
│       │   ├── duplicate_finder.py # Contém DuplicateFinderAlgorithm
│       │   └── decision_engine.py
│       │
│       ├── domain/                 # Modelos de domínio (dataclasses/Pydantic)
│       │   ├── __init__.py
│       │   └── models.py           # Contém FileInfo, DuplicateGroup, ScanSettings, etc.
│       │
│       ├── infrastructure/         # Camada de Infraestrutura
│       │   ├── __init__.py
│       │   ├── file_system.py      # Interface IFileSystemService
│       │   ├── file_system_impl.py # Implementação FileSystemService
│       │   ├── zip_handler.py      # Interface IZipHandlerService
│       │   ├── zip_handler_impl.py # Implementação ZipHandlerService
│       │   ├── hashing.py          # Interface IHashingService
│       │   ├── hashing_impl.py     # Implementação HashingService
│       │   ├── concurrency.py      # Interface IConcurrencyService
│       │   ├── concurrency_impl.py # Implementação ConcurrencyService
│       │   ├── backup_manager.py   # Interface IBackupManagerService
│       │   ├── backup_manager_impl.py # Implementação BackupManagerService
│       │   ├── logging.py          # Interface ILoggingService
│       │   ├── logging_impl.py     # Implementação LoggingService
│       │   ├── config_loader.py    # Interface IConfigLoader
│       │   └── config_loader_impl.py # Implementação ConfigLoader
│       │
│       ├── utils/                  # Utilitários comuns
│       │   ├── __init__.py
│       │   └── media_parser.py     # Para extrair resolução de imagens/vídeos
│       │
│       └── config/                 # Arquivos de configuração padrão, se houver
│           └── default_app_settings.json
│
├── tests/                        # Testes unitários e de integração
│   ├── __init__.py
│   ├── unit/
│   │   ├── core/
│   │   └── infrastructure/
│   └── integration/
│
├── scripts/                      # Scripts auxiliares (build, release, etc.)
├── docs/                         # Documentação
├── README.md
├── pyproject.toml                # Para build e dependências (PEP 517/518)
└── LICENSE
```
*Nota sobre `infrastructure/*_impl.py`:* As interfaces (ABCs) podem estar em `fotix/infrastructure/interfaces/` ou diretamente nos arquivos de módulo (ex: `file_system.py` define `IFileSystemService` e `file_system_impl.py` define `FileSystemService` que a implementa). Optei por sugerir interfaces e implementações separadas para maior clareza, mas manter a interface no mesmo arquivo da sua principal implementação também é comum (`file_system.py` teria `IFileSystemService` e `FileSystemService`). Por simplicidade inicial, manter a interface e a implementação principal no mesmo arquivo de módulo pode ser mais prático, e o `_impl` pode ser omitido (ex: `fotix.infrastructure.file_system.py` conteria tanto `IFileSystemService` quanto `FileSystemService`). Para este blueprint, usei a abordagem de arquivos `_impl.py` para enfatizar a separação.

## 7. Considerações de Segurança

1.  **Remoção Segura de Arquivos:** Uso de `send2trash` (abstraído pelo `FileSystemService`) para mover arquivos para a lixeira em vez de exclusão permanente, permitindo recuperação pelo usuário fora do sistema de backup da aplicação, se necessário.
2.  **Backup Automático:** O `BackupManagerService` garante que os arquivos sejam copiados para uma área de backup antes da remoção. O acesso a esta área deve ser restrito ao usuário.
3.  **Validação de Input:**
    *   Caminhos de diretório/arquivo fornecidos pelo usuário na UI devem ser validados para evitar Path Traversal (embora `pathlib` ajude, verificar se os caminhos são "seguros" ou estão dentro de limites esperados é bom).
    *   Configurações lidas de arquivos devem ser validadas (Pydantic nos modelos de domínio/config pode ajudar).
4.  **Tratamento de Erros:** Operações críticas (leitura/escrita de arquivos, remoção) devem ter tratamento de erro robusto (try-except) e logar falhas detalhadamente. A UI deve informar o usuário sobre erros críticos de forma clara.
5.  **Permissões de Arquivo:** A aplicação rodará com as permissões do usuário. Nenhuma elevação de privilégio é esperada ou necessária.
6.  **Dependências:** Manter as dependências atualizadas para mitigar vulnerabilidades conhecidas.
7.  **Sem Dados Sensíveis:** A aplicação lida primariamente com metadados de arquivos e os próprios arquivos. Não há armazenamento de senhas ou outras informações pessoais sensíveis, exceto os caminhos dos arquivos do usuário.

## 8. Justificativas e Trade-offs

*   **Arquitetura em Camadas:**
    *   **Justificativa:** Promove SRP, testabilidade (mocking de camadas/serviços), manutenibilidade e clareza. Permite que diferentes partes da equipe (se houvesse) trabalhem em paralelo em diferentes camadas.
    *   **Trade-off:** Pode introduzir um pouco mais de boilerplate para a comunicação entre camadas (ex: DTOs, chamadas de serviço) em comparação com uma abordagem monolítica mais simples. No entanto, para um projeto com a complexidade descrita, os benefícios superam esse custo.
*   **Abstração da Infraestrutura:**
    *   **Justificativa:** Conforme Diretriz 3. Desacopla a lógica de negócios das implementações concretas de acesso a arquivos, hashing, etc. Facilita a testagem (mocking dos serviços de infra) e a substituição de bibliotecas subjacentes se necessário, sem impactar o core da aplicação.
    *   **Trade-off:** Leve aumento na quantidade de código devido às interfaces e wrappers.
*   **`concurrent.futures` para Paralelismo:**
    *   **Justificativa:** Biblioteca padrão do Python, bem testada, e adequada para tarefas I/O-bound (como leitura de arquivos) e CPU-bound (como hashing, se o GIL for liberado pela biblioteca de hashing, o que BLAKE3 faz). `ThreadPoolExecutor` é geralmente mais simples para I/O-bound e evita a complexidade de `multiprocessing` para uma aplicação desktop.
    *   **Trade-off:** `ThreadPoolExecutor` ainda é limitado pelo GIL para código Python puro CPU-bound, mas BLAKE3 libera o GIL, tornando-o eficaz.
*   **`stream-unzip` para ZIPs:**
    *   **Justificativa:** Essencial para lidar com grandes arquivos ZIP sem consumir memória excessiva, atendendo ao requisito de baixo uso de memória.
    *   **Trade-off:** Pode ser um pouco mais complexo de usar do que a biblioteca `zipfile` padrão para operações simples, mas o benefício de streaming compensa para o caso de uso.
*   **Sem Banco de Dados Externo:**
    *   **Justificativa:** Simplifica a implantação e o gerenciamento para um aplicativo desktop de usuário final. Os dados de backup são gerenciados com arquivos e um log JSON simples.
    *   **Trade-off:** Consultas complexas sobre o log de backup seriam menos eficientes do que com um SQL DB, mas para o escopo atual, é suficiente.
*   **Python Dataclasses / Pydantic para Modelos:**
    *   **Justificativa:** Dataclasses são leves e parte da stdlib. Pydantic adiciona validação robusta que pode ser útil, especialmente para configurações e dados de entrada. A escolha entre eles pode ser feita por módulo; Pydantic é recomendado para `AppConfig` e `ScanSettings`.
    *   **Trade-off:** Pydantic adiciona uma dependência, mas seus benefícios de validação e serialização geralmente compensam.
*   **Foco em Idênticos (Hashing) vs. Similaridade Perceptual:**
    *   **Justificativa:** Simplifica significativamente o algoritmo de detecção e atende ao requisito de "arquivos idênticos". Similaridade perceptual é um problema muito mais complexo.
    *   **Trade-off:** Não encontrará imagens/vídeos que são visualmente semelhantes mas não idênticos em bytes. Isso está alinhado com as restrições.