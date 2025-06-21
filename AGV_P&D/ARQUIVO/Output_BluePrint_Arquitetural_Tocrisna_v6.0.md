# Proposta de Arquitetura Técnica: Fotix

Este documento detalha a arquitetura de alto nível para o aplicativo desktop `Fotix`, projetado para ser modular, manutenível e escalável, conforme as diretrizes do AGV.

## 1. Visão Geral da Arquitetura

A arquitetura proposta para o `Fotix` é uma **Arquitetura em Camadas (Layered Architecture)**, fortemente inspirada nos princípios da **Arquitetura Limpa (Clean Architecture)**. Esta abordagem garante uma separação clara de responsabilidades, desacoplamento e alta testabilidade.

As camadas são:
1.  **Presentation (UI):** Responsável pela interação com o usuário. Contém toda a lógica da interface gráfica (PySide6). Não possui lógica de negócio.
2.  **Application:** Orquestra os casos de uso do sistema. Atua como um intermediário entre a UI e o Core, utilizando os serviços de infraestrutura para executar as tarefas.
3.  **Core (Domain):** O coração do sistema. Contém a lógica de negócio pura e os modelos de domínio (entidades). É completamente independente de qualquer framework externo (UI, banco de dados, sistema de arquivos).
4.  **Infrastructure:** Contém as implementações concretas de interfaces definidas nas camadas superiores. Lida com detalhes externos como sistema de arquivos, bibliotecas de hashing, logging, etc.

**Justificativa:** Esta arquitetura é ideal para `Fotix` porque:
*   **Isola a Lógica de Negócio:** A lógica de identificação e seleção de duplicatas (o "molho secreto" do app) reside no Core, livre de dependências externas, facilitando testes e manutenção.
*   **Promove a Testabilidade:** Cada camada pode ser testada isoladamente. Serviços de infraestrutura podem ser substituídos por *mocks* para testar a camada de aplicação e o core de forma unitária.
*   **Facilita a Manutenção e Evolução:** Trocar a biblioteca de GUI ou o método de hashing se torna uma tarefa localizada na camada de Presentation ou Infrastructure, sem impactar a lógica central.
*   **Mantém a GUI Responsiva:** A camada de Aplicação orquestrará a execução de tarefas pesadas (escaneamento, hashing) em threads separadas, comunicando-se com a UI via sinais e slots (padrão Observer), garantindo que a interface nunca trave.

## 2. Diagrama de Componentes (Simplificado)

```mermaid
graph TD
    subgraph Presentation Layer
        UI_Components[UI: PySide6 Views & Widgets]
    end

    subgraph Application Layer
        App_ScanService[Application: ScanningService]
        App_ActionService[Application: ActionService]
    end

    subgraph Core (Domain) Layer
        Core_Models[Core: Models (Pydantic)]
        Core_DuplicateFinder[Core: DuplicateFinder]
        Core_SelectionStrategy[Core: SelectionStrategy]
    end

    subgraph Infrastructure Layer
        Infra_FileSystem[Infra: FileSystem Service]
        Infra_ZipScanner[Infra: ZipScanner Service]
        Infra_Hashing[Infra: Hashing Service]
        Infra_Concurrency[Infra: Concurrency Service]
        Infra_Backup[Infra: Backup Service]
        Infra_Logging[Infra: Logging Service]
    end

    %% Fluxo de Controle Principal
    UI_Components -- Inicia Ações --> App_ScanService
    UI_Components -- Inicia Ações --> App_ActionService

    %% Dependências da Camada de Aplicação
    App_ScanService -- Usa --> Core_DuplicateFinder
    App_ScanService -- Usa --> Core_SelectionStrategy
    App_ScanService -- Usa Interface de --> Infra_FileSystem
    App_ScanService -- Usa Interface de --> Infra_ZipScanner
    App_ScanService -- Usa Interface de --> Infra_Hashing
    App_ScanService -- Usa Interface de --> Infra_Concurrency

    App_ActionService -- Usa Interface de --> Infra_Backup
    App_ActionService -- Usa Interface de --> Infra_FileSystem

    %% Dependências do Core
    Core_DuplicateFinder -- Usa --> Core_Models
    Core_SelectionStrategy -- Usa --> Core_Models

    %% Dependências são definidas via Interfaces (Abstrações)
    style Infra_FileSystem fill:#f9f,stroke:#333,stroke-width:2px
    style Infra_ZipScanner fill:#f9f,stroke:#333,stroke-width:2px
    style Infra_Hashing fill:#f9f,stroke:#333,stroke-width:2px
    style Infra_Concurrency fill:#f9f,stroke:#333,stroke-width:2px
    style Infra_Backup fill:#f9f,stroke:#333,stroke-width:2px
    style Infra_Logging fill:#f9f,stroke:#333,stroke-width:2px

    linkStyle 6,7,8,9,10,11 stroke-dasharray: 5 5;

    note right of Infra_Backup
      As camadas superiores dependem de
      ABSTRAÇÕES (Interfaces) que são
      implementadas pela camada de
      INFRAESTRUTURA.
      (Inversão de Dependência)
    end
```

## 3. Descrição dos Componentes, Interfaces e Modelos de Domínio

### 3.1. Camada Core (Domain) - Fonte Única da Verdade (SSOT) para Modelos

Localização: `src/fotix/core/`

#### 3.1.1. `fotix.core.models`
Este módulo é a Fonte Única da Verdade para todas as estruturas de dados do projeto.

*   **Responsabilidade Principal:** Definir as entidades de negócio e estruturas de dados canônicas do sistema.
*   **Tecnologias Chave:** Pydantic `BaseModel` para validação, tipagem e serialização.
*   **Dependências Diretas:** Nenhuma (apenas bibliotecas padrão e Pydantic).
*   **Modelos Definidos:**
    *   `ScanConfig(BaseModel)`: Configurações para uma operação de escaneamento.
        *   `target_paths: list[Path]`
        *   `include_zip_files: bool`
        *   `excluded_folders: list[str]`
    *   `FileMetadata(BaseModel)`: Metadados extraídos de um arquivo de mídia.
        *   `resolution: tuple[int, int] | None`
        *   `creation_date: datetime | None`
    *   `FileRecord(BaseModel)`: Representação canônica de um arquivo no sistema.
        *   `absolute_path: Path`
        *   `size_bytes: int`
        *   `file_hash: str | None = None`
        *   `metadata: FileMetadata`
        *   `source_zip_path: Path | None = None` (se veio de um ZIP)
    *   `DuplicateSet(BaseModel)`: Um conjunto de arquivos idênticos.
        *   `file_hash: str`
        *   `files: list[FileRecord]`
        *   `keeper: FileRecord | None = None`
        *   `to_delete: list[FileRecord] = []`
    *   `ProcessingStats(BaseModel)`: Estatísticas do processamento.
        *   `total_files_scanned: int`
        *   `total_duplicates_found: int`
        *   `space_to_be_saved_bytes: int`
        *   `processing_time_seconds: float`

#### 3.1.2. `fotix.core.duplicate_finder`
*   **Responsabilidade Principal:** Receber uma lista de `FileRecord` com hashes preenchidos e agrupá-los em uma lista de `DuplicateSet`.
*   **Tecnologias Chave:** Python (Lógica Pura).
*   **Dependências Diretas:** `fotix.core.models`.

#### 3.1.3. `fotix.core.selection_strategy`
*   **Responsabilidade Principal:** Implementar o **Padrão Strategy** para decidir qual arquivo manter em um `DuplicateSet`. A lógica considera resolução, data e nome do arquivo.
*   **Tecnologias Chave:** Python (Lógica Pura).
*   **Dependências Diretas:** `fotix.core.models`.

---

### 3.2. Camada de Aplicação

Localização: `src/fotix/application/`

#### 3.2.1. `fotix.application.scanning_service`
*   **Responsabilidade Principal:** Orquestrar o fluxo completo de escaneamento e identificação de duplicatas. Utiliza serviços de infraestrutura para tarefas de baixo nível e o Core para a lógica de negócio. Emite sinais de progresso para a UI.
*   **Tecnologias Chave:** Python (Lógica de orquestração).
*   **Dependências Diretas:** `fotix.core.models`, `fotix.core.duplicate_finder`, `fotix.core.selection_strategy`, e as interfaces dos serviços de infraestrutura (`IFileSystemService`, `IZipScannerService`, `IHashingService`, `IConcurrencyService`, `ILoggingService`).

#### 3.2.2. `fotix.application.action_service`
*   **Responsabilidade Principal:** Orquestrar as ações de remoção e restauração de arquivos, garantindo que o backup seja feito antes de qualquer remoção.
*   **Tecnologias Chave:** Python (Lógica de orquestração).
*   **Dependências Diretas:** `fotix.core.models`, e as interfaces dos serviços de infraestrutura (`IBackupService`, `IFileSystemService`, `ILoggingService`).

---

### 3.3. Camada de Infraestrutura

Localização: `src/fotix/infrastructure/`

Esta camada implementa as interfaces de serviço.

#### 3.3.1. `fotix.infrastructure.file_system_service`
*   **Responsabilidade Principal:** Implementar a interface `IFileSystemService`, abstraindo as interações com o sistema de arquivos. Realiza a tradução de dados brutos (ex: `os.stat_result`) para os modelos do domínio (ex: `FileRecord`).
*   **Tecnologias Chave:** `pathlib`, `shutil`, `send2trash`.
*   **Dependências Diretas:** `fotix.core.models`.

#### 3.3.2. `fotix.infrastructure.zip_scanner_service`
*   **Responsabilidade Principal:** Implementar a interface `IZipScannerService`, lendo o conteúdo de arquivos ZIP de forma progressiva e eficiente em memória. Mapeia os dados do ZIP para o modelo `FileRecord`.
*   **Tecnologias Chave:** `stream-unzip`.
*   **Dependências Diretas:** `fotix.core.models`.

#### 3.3.3. `fotix.infrastructure.hashing_service`
*   **Responsabilidade Principal:** Implementar a interface `IHashingService`, calculando hashes de arquivos de forma eficiente.
*   **Tecnologias Chave:** `blake3`.
*   **Dependências Diretas:** Nenhuma (além das interfaces que implementa).

#### 3.3.4. `fotix.infrastructure.concurrency_service`
*   **Responsabilidade Principal:** Implementar a interface `IConcurrencyService`, gerenciando um pool de threads para executar tarefas em paralelo (como o hashing de múltiplos arquivos).
*   **Tecnologias Chave:** `concurrent.futures.ThreadPoolExecutor`.
*   **Dependências Diretas:** Nenhuma.

#### 3.3.5. `fotix.infrastructure.backup_service`
*   **Responsabilidade Principal:** Implementar a interface `IBackupService`. Gerencia a movimentação de arquivos para uma pasta de backup segura e mantém um manifesto (JSON) de cada operação de restauração.
*   **Tecnologias Chave:** `pathlib`, `shutil`, `json`.
*   **Dependências Diretas:** `fotix.core.models`.

#### 3.3.6. `fotix.infrastructure.logging_service`
*   **Responsabilidade Principal:** Implementar a interface `ILoggingService`. Configura e fornece um logger padronizado para ser usado em toda a aplicação.
*   **Tecnologias Chave:** `logging` (stdlib).
*   **Dependências Diretas:** Nenhuma.

---

### 3.4. Camada de Apresentação (UI)

Localização: `src/fotix/ui/`

*   **Responsabilidade Principal:** Fornecer a interface gráfica para o usuário, capturar inputs e exibir resultados e progresso. Comunica-se exclusivamente com os serviços da Camada de Aplicação.
*   **Tecnologias Chave:** PySide6.
*   **Decomposição em Componentes/Views:**
    *   **`MainWindow`:** A janela principal da aplicação, que contém e gerencia as outras views.
        *   **Interage com:** `ScanningService`, `ActionService`.
    *   **`ConfigView`:** Tela inicial para o usuário selecionar diretórios, ativar a busca em ZIPs e iniciar o escaneamento.
        *   **Interage com:** `ScanningService`.
    *   **`ProgressView`:** Componente (pode ser um diálogo ou uma área na `MainWindow`) que exibe o progresso do escaneamento em tempo real (ex: arquivos escaneados, progresso do hashing) e logs. Utilizará o mecanismo de sinais e slots do Qt para receber atualizações de um worker thread sem travar a UI.
        *   **Interage com:** Sinais emitidos pelo `ScanningService`.
    *   **`ResultsView`:** Tabela ou lista que exibe os `DuplicateSet` encontrados, destacando o arquivo a ser mantido (`keeper`) e permitindo que o usuário revise antes de confirmar a exclusão.
        *   **Interage com:** `ActionService`.
    *   **`RestoreView`:** Tela para listar os backups disponíveis e permitir que o usuário selecione um para restaurar os arquivos.
        *   **Interage com:** `ActionService`.

## 4. Definição das Interfaces Principais

As interfaces são contratos que garantem o desacoplamento. As implementações concretas (na camada de infraestrutura) serão injetadas nos componentes que as necessitam.

---

**Interface: `ILoggingService`**
*   **Propósito:** Fornecer um logger configurado.
*   **Assinaturas Chave:**
    *   `get_logger(name: str) -> logging.Logger`: Retorna uma instância de logger.

---

**Interface: `IFileSystemService`**
*   **Propósito:** Abstrair operações de leitura e manipulação no sistema de arquivos.
*   **Configuração via `__init__`:**
    *   `__init__(self, logger: ILoggingService)`
*   **Assinaturas Chave:**
    *   `scan_directory_recursively(self, path: Path) -> Iterator[Path]`: Retorna um iterador de caminhos de arquivos.
    *   `get_file_size(self, path: Path) -> int`: Retorna o tamanho do arquivo em bytes.
    *   `get_media_metadata(self, path: Path) -> FileMetadata`: Extrai metadados (resolução, data). Retorna um modelo `FileMetadata` do domínio.
    *   `move_to_trash(self, path: Path) -> None`: Move o arquivo para a lixeira do sistema.
    *   `read_file_chunks(self, path: Path, chunk_size: int = 8192) -> Iterator[bytes]`: Lê um arquivo em pedaços.

---

**Interface: `IHashingService`**
*   **Propósito:** Abstrair o cálculo de hash de arquivos.
*   **Configuração via `__init__`:** Não necessita de configuração especial.
*   **Assinaturas Chave:**
    *   `hash_file(self, path: Path) -> str`: Calcula e retorna o hash BLAKE3 de um arquivo.

---

**Interface: `IBackupService`**
*   **Propósito:** Gerenciar operações de backup e restauração.
*   **Configuração via `__init__`:**
    *   `__init__(self, backup_root_path: Path, logger: ILoggingService)`
*   **Assinaturas Chave:**
    *   `create_backup(self, files_to_backup: list[FileRecord]) -> str`: Move os arquivos para uma pasta de backup com um ID único e cria um manifesto. Retorna o ID do backup.
    *   `restore_from_backup(self, backup_id: str) -> None`: Restaura os arquivos de um backup específico para seus locais originais.
    *   `list_backups(self) -> list[dict]`: Lista os backups disponíveis.

---

**Interface: `IConcurrencyService`**
*   **Propósito:** Abstrair a execução de tarefas em paralelo.
*   **Configuração via `__init__`:**
    *   `__init__(self, max_workers: int | None = None)`
*   **Assinaturas Chave:**
    *   `run_in_parallel(self, fn: Callable, tasks: Iterable) -> list`: Executa a função `fn` para cada item em `tasks` usando um pool de threads.

## 5. Gerenciamento de Dados

A persistência de dados em `Fotix` é limitada e baseada em arquivos, sem a necessidade de um banco de dados.

*   **Backup:** Os dados de backup serão gerenciados pelo `BackupService`. Cada operação de remoção criará um novo subdiretório dentro de uma pasta `fotix_backups` (localizada, por exemplo, em `%APPDATA%/Fotix`). Este subdiretório conterá os arquivos removidos e um arquivo `manifest.json`, que armazena os metadados dos arquivos, incluindo seus caminhos originais, usando o modelo `FileRecord` serializado.
*   **Configurações do Usuário:** Configurações simples (como último diretório usado) podem ser salvas em um arquivo de configuração (ex: `config.json`) usando Pydantic para serialização/deserialização.
*   **Logs:** Logs serão escritos em arquivos de texto (`fotix.log`) pelo `LoggingService`.

## 6. Estrutura de Diretórios Proposta

Utilizando o layout `src` moderno para facilitar o empacotamento e a instalação.

```
fotix-project/
├── .gitignore
├── pyproject.toml         # Definição do projeto e dependências (Poetry, PDM ou Hatch)
├── README.md
└── src/
    └── fotix/
        ├── __main__.py        # Ponto de entrada, bootstrapping da aplicação
        ├── __init__.py
        |
        ├── core/              # Lógica de negócio e modelos (sem dependências externas)
        │   ├── __init__.py
        │   ├── models.py      # SSOT: Pydantic models (FileRecord, DuplicateSet, etc.)
        │   ├── duplicate_finder.py
        │   └── selection_strategy.py
        |
        ├── application/       # Orquestração dos casos de uso
        │   ├── __init__.py
        │   ├── interfaces.py    # Definição de todas as interfaces (IFileSystemService, etc.)
        │   ├── scanning_service.py
        │   └── action_service.py
        |
        ├── infrastructure/    # Implementações concretas de interfaces
        │   ├── __init__.py
        │   ├── file_system_service.py
        │   ├── zip_scanner_service.py
        │   ├── hashing_service.py
        │   ├── backup_service.py
        │   ├── concurrency_service.py
        │   └── logging_service.py
        |
        └── ui/                # Camada de apresentação (PySide6)
            ├── __init__.py
            ├── main_window.py
            ├── config_view.py
            ├── results_view.py
            └── components/      # Componentes reutilizáveis (ex: progress bar com texto)

```

## 7. Arquivo `.gitignore` Proposto

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
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
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
.hypothesis/
.pytest_cache/

# Environments
.env
.venv/
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE / Editor specific
.idea/
.vscode/
*.swp
*~

# Fotix specific
fotix_backups/
*.log
config.json

# Qt / PySide
.designer/
```

## 8. Considerações de Segurança

*   **Remoção Segura:** O uso da biblioteca `send2trash` em vez de `os.remove` é um pilar de segurança, pois permite a recuperação de arquivos pelo usuário através da Lixeira do sistema, prevenindo a perda acidental de dados.
*   **Operações de Arquivo:** Todas as operações de escrita/remoção no `FileSystemService` e `BackupService` devem ser envolvidas em blocos `try...except` para lidar com erros de permissão, disco cheio ou arquivos bloqueados, informando o usuário de forma clara.
*   **Validação de Input:** A UI deve validar os caminhos de diretório fornecidos pelo usuário para garantir que são válidos antes de passá-los para a camada de aplicação. Os modelos Pydantic na camada Core adicionam uma camada secundária de validação de dados.
*   **Não Execução de Código:** O sistema apenas lê e analisa metadados de arquivos, ele não executa nem interpreta o conteúdo dos arquivos de mídia, mitigando riscos de segurança associados a arquivos maliciosos.

## 9. Justificativas e Trade-offs

*   **Arquitetura em Camadas vs. Simples Script:** Embora um script monolítico pudesse funcionar, a arquitetura em camadas foi escolhida para garantir manutenibilidade e testabilidade a longo prazo. O custo inicial de configuração é compensado pela facilidade de modificar ou adicionar funcionalidades futuras (ex: suportar novos formatos de arquivo como RAR, ou adicionar novas estratégias de seleção).
*   **`concurrent.futures` vs. `asyncio`:** `ThreadPoolExecutor` de `concurrent.futures` é mais adequado aqui, pois as operações principais (leitura de disco, hashing) são limitadas por I/O e CPU, e as bibliotecas subjacentes (`pathlib`, `blake3`) são síncronas. Isso simplifica o código em comparação com uma implementação `asyncio` completa, que exigiria bibliotecas assíncronas para operações de arquivo (como `aiofiles`).
*   **Abstração de Infraestrutura:** A criação de *wrappers* (ex: `FileSystemService`) em vez de usar `pathlib` diretamente na camada de aplicação adiciona uma pequena sobrecarga, mas é crucial para a testabilidade, permitindo a fácil substituição por *mocks* em testes.

## 10. Exemplo de Bootstrapping/Inicialização (`src/fotix/__main__.py`)

Este exemplo conceitual demonstra como os componentes são instanciados e como as dependências são injetadas (Injeção de Dependência via construtor), unindo toda a arquitetura.

```python
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

# Importações de todas as camadas
from fotix.core.duplicate_finder import DuplicateFinder
from fotix.core.selection_strategy import DefaultSelectionStrategy
from fotix.application.scanning_service import ScanningService
from fotix.application.action_service import ActionService
from fotix.infrastructure.logging_service import LoggingService
from fotix.infrastructure.file_system_service import FileSystemService
from fotix.infrastructure.zip_scanner_service import ZipScannerService
from fotix.infrastructure.hashing_service import HashingService
from fotix.infrastructure.backup_service import BackupService
from fotix.infrastructure.concurrency_service import ConcurrencyService
from fotix.ui.main_window import MainWindow

def main():
    """Ponto de entrada principal: instancia e conecta os componentes."""

    # --- 1. Configuração Inicial ---
    # Valores que viriam de um arquivo de config ou de constantes
    APP_DATA_PATH = Path.home() / "AppData" / "Roaming" / "Fotix"
    BACKUP_ROOT_PATH = APP_DATA_PATH / "backups"
    LOG_FILE_PATH = APP_DATA_PATH / "fotix.log"
    
    # Garante que os diretórios existem
    APP_DATA_PATH.mkdir(parents=True, exist_ok=True)
    BACKUP_ROOT_PATH.mkdir(exist_ok=True)

    # --- 2. Instanciação da Camada de Infraestrutura (implementações concretas) ---
    # Estes são os "tijolos" que não dependem de outros serviços.
    
    # Serviços com configuração injetada
    logging_service = LoggingService(log_file_path=LOG_FILE_PATH, level="INFO")
    logger = logging_service.get_logger("fotix_app")
    
    # Serviços que dependem de configuração ou outros serviços básicos (como logger)
    file_system_service = FileSystemService(logger=logger)
    zip_scanner_service = ZipScannerService(logger=logger)
    hashing_service = HashingService()
    concurrency_service = ConcurrencyService(max_workers=8) # poderia ser configurável
    backup_service = BackupService(backup_root_path=BACKUP_ROOT_PATH, logger=logger)
    
    logger.info("Serviços de infraestrutura instanciados.")

    # --- 3. Instanciação da Camada Core (lógica pura) ---
    # Geralmente não precisam de injeção complexa
    duplicate_finder = DuplicateFinder()
    selection_strategy = DefaultSelectionStrategy()
    
    logger.info("Componentes do Core instanciados.")

    # --- 4. Instanciação da Camada de Aplicação (orquestradores) ---
    # Injeta as dependências (implementações da infraestrutura e componentes do core)
    scanning_service = ScanningService(
        file_system_service=file_system_service,
        zip_scanner_service=zip_scanner_service,
        hashing_service=hashing_service,
        concurrency_service=concurrency_service,
        duplicate_finder=duplicate_finder,
        selection_strategy=selection_strategy,
        logger=logger
    )

    action_service = ActionService(
        file_system_service=file_system_service,
        backup_service=backup_service,
        logger=logger
    )
    
    logger.info("Serviços de aplicação instanciados e injetados.")

    # --- 5. Instanciação e Execução da Camada de Apresentação (UI) ---
    # A UI recebe os serviços da aplicação para poder invocar os casos de uso
    app = QApplication(sys.argv)
    
    main_window = MainWindow(
        scanning_service=scanning_service,
        action_service=action_service
    )
    main_window.show()
    
    logger.info("Aplicação iniciada. Exibindo a janela principal.")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

```