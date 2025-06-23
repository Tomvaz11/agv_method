# Blueprint Arquitetural: Fotix

## 1. Visão Geral da Arquitetura

A arquitetura proposta para o `Fotix` é uma **Arquitetura em Camadas (Layered Architecture)**, com forte influência dos princípios da Clean Architecture. Essa abordagem foi escolhida para maximizar a **modularidade**, a **testabilidade** e a **separação de responsabilidades (SRP)**.

As camadas são organizadas da seguinte forma:

1.  **Camada de Apresentação (UI):** Responsável por toda a interação com o usuário. Construída com PySide6, esta camada é "burra": ela apenas exibe dados e delega todas as ações do usuário para a Camada de Aplicação. Ela não contém lógica de negócio.
2.  **Camada de Aplicação (Application):** Atua como o orquestrador central. Ela define os casos de uso do sistema (ex: "Iniciar uma varredura de duplicatas") e coordena as interações entre a UI e as camadas inferiores (Core e Infraestrutura).
3.  **Camada de Domínio (Core):** O coração do sistema. Contém os modelos de dados canônicos (entidades de negócio) e a lógica de negócio pura, como o algoritmo de seleção de qual arquivo manter. Esta camada é completamente independente de qualquer framework externo (UI, banco de dados, sistema de arquivos).
4.  **Camada de Infraestrutura (Infrastructure):** Implementa as interações com o mundo exterior. Contém os "adaptadores" para o sistema de arquivos, hashing, manipulação de ZIPs, logging e concorrência. Ela implementa as interfaces definidas pela Camada de Aplicação, desacoplando a lógica de negócio dos detalhes de implementação.

Essa estrutura garante que a lógica de negócio (Core) possa ser testada isoladamente e que as tecnologias de infraestrutura (ex: a biblioteca de hashing) possam ser trocadas com o mínimo de impacto no resto do sistema.

## 2. Diagrama de Componentes (Simplificado)

O diagrama abaixo ilustra o fluxo de dependências. As setas apontam para o componente do qual se depende. Note que todas as dependências apontam para "dentro", em direção à Camada de Domínio.

```mermaid
graph TD
    subgraph Camada de Apresentação (UI)
        A[fotix.ui]
    end

    subgraph Camada de Aplicação
        B[fotix.application.services]
    end

    subgraph Camada de Domínio (Core)
        C[fotix.domain.models]
        D[fotix.domain.strategies]
    end

    subgraph Camada de Infraestrutura
        E[fotix.infrastructure.file_system]
        F[fotix.infrastructure.hashing]
        G[fotix.infrastructure.backup]
        H[fotix.infrastructure.concurrency]
        I[fotix.infrastructure.zip_handler]
        J[fotix.infrastructure.logging]
    end

    A -- Interage com / Delega para --> B

    B -- Usa --> C
    B -- Usa --> D
    B -- Usa Interfaces de --> E
    B -- Usa Interfaces de --> F
    B -- Usa Interfaces de --> G
    B -- Usa Interfaces de --> H
    B -- Usa Interfaces de --> I
    B -- Usa Interfaces de --> J

    D -- Usa --> C

    style C fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#f9f,stroke:#333,stroke-width:2px
```

## 3. Descrição dos Componentes, Interfaces e Modelos de Domínio

### 3.1. Camada de Domínio / Core (Fonte Única da Verdade para Modelos)

#### `fotix.domain.models`
-   **Responsabilidade Principal:** Define as estruturas de dados canônicas (entidades e objetos de valor) que representam os conceitos de negócio do Fotix. Esta é a **Fonte Única da Verdade (SSOT)** para todos os modelos de dados do projeto.
-   **Tecnologias Chave:** Pydantic `BaseModel` para validação, tipagem e serialização.
-   **Dependências Diretas:** Nenhuma (além de `pydantic`).
-   **Modelos de Dados Principais:**
    -   `FileMeta(BaseModel)`: Representa metadados de um único arquivo.
        -   `path: Path`
        -   `size: int`
        -   `creation_time: datetime`
        -   `hash: str | None = None`
        -   `resolution: tuple[int, int] | None = None`
        -   `is_in_zip: bool = False`
    -   `DuplicateSet(BaseModel)`: Agrupa uma lista de arquivos idênticos.
        -   `files: list[FileMeta]`
        -   `file_to_keep: FileMeta | None = None`
    -   `ScanConfig(BaseModel)`: Configurações para uma operação de varredura.
        -   `target_paths: list[Path]`
        -   `include_zips: bool = True`
    -   `ScanStats(BaseModel)`: Estatísticas resumidas de uma operação.
        -   `files_scanned: int = 0`
        -   `duplicates_found: int = 0`
        -   `space_saved_bytes: int = 0`
        -   `total_time_seconds: float = 0`

#### `fotix.domain.strategies`
-   **Responsabilidade Principal:** Implementa a lógica de negócio pura e sem estado para decidir qual arquivo manter de um `DuplicateSet`. Encapsula o "algoritmo inteligente". Segue o padrão **Strategy**.
-   **Tecnologias Chave:** Python (Lógica Pura).
-   **Dependências Diretas:** `fotix.domain.models`.

---

### 3.2. Camada de Aplicação

#### `fotix.application.services`
-   **Responsabilidade Principal:** Orquestrar os casos de uso. O `ScanService` é o principal serviço, responsável por:
    1.  Receber uma `ScanConfig`.
    2.  Usar `ConcurrencyService` e `FileSystemService` para encontrar todos os arquivos.
    3.  Coordenar o `HashingService` para calcular hashes em paralelo.
    4.  Agrupar arquivos por hash para criar `DuplicateSet`s.
    5.  Aplicar o `ISelectionStrategy` do domínio para escolher o arquivo a ser mantido.
    6.  Coordenar `BackupService` e `FileSystemService` para remover os arquivos selecionados.
    7.  Emitir sinais/callbacks com o progresso e os resultados.
-   **Tecnologias Chave:** Python (Lógica de Orquestração).
-   **Dependências Diretas:**
    -   `fotix.domain.models`
    -   `fotix.domain.strategies`
    -   Interfaces de todos os serviços de `fotix.infrastructure`

---

### 3.3. Camada de Infraestrutura

#### `fotix.infrastructure.file_system`
-   **Responsabilidade Principal:** Abstrair todas as interações diretas com o sistema de arquivos. Implementa a interface `IFileSystemService`. Responsável por mapear os dados brutos do sistema de arquivos para o modelo `FileMeta`.
-   **Tecnologias Chave:** `pathlib`, `shutil`, `send2trash`, `os`.
-   **Dependências Diretas:** `fotix.domain.models`.

#### `fotix.infrastructure.hashing`
-   **Responsabilidade Principal:** Abstrair o cálculo de hashes de arquivos. Implementa a interface `IHashingService`. Otimizado para ler arquivos em chunks para não sobrecarregar a memória.
-   **Tecnologias Chave:** `blake3`.
-   **Dependências Diretas:** Nenhuma.

#### `fotix.infrastructure.zip_handler`
-   **Responsabilidade Principal:** Abstrair a leitura e extração de conteúdo de arquivos ZIP de forma eficiente em termos de memória. Implementa a interface `IZipHandlerService`.
-   **Tecnologias Chave:** `stream-unzip`.
-   **Dependências Diretas:** `fotix.domain.models`.

#### `fotix.infrastructure.backup`
-   **Responsabilidade Principal:** Gerenciar o backup seguro de arquivos antes da remoção e a sua posterior restauração. Mantém um manifesto (ex: JSON) dos arquivos movidos. Implementa `IBackupService`.
-   **Tecnologias Chave:** `pathlib`, `shutil`, `json`.
-   **Dependências Diretas:** `fotix.domain.models`.

#### `fotix.infrastructure.concurrency`
-   **Responsabilidade Principal:** Abstrair a execução de tarefas em paralelo. Implementa `IConcurrencyService` para gerenciar um pool de threads ou processos.
-   **Tecnologias Chave:** `concurrent.futures`.
-   **Dependências Diretas:** Nenhuma.

#### `fotix.infrastructure.logging`
-   **Responsabilidade Principal:** Configurar e fornecer uma interface padronizada para o sistema de logging da aplicação.
-   **Tecnologias Chave:** `logging` (stdlib).
-   **Dependências Diretas:** Nenhuma.

---

### 3.4. Camada de Apresentação (UI)

#### `fotix.ui`
-   **Responsabilidade Principal:** Fornecer a interface gráfica para o usuário, apresentar o progresso e os resultados, e capturar as intenções do usuário, delegando-as ao `ScanService`.
-   **Tecnologias Chave:** PySide6.
-   **Dependências Diretas:** `fotix.application.services`, `fotix.domain.models`.
-   **Decomposição dos Componentes de UI:**
    -   `MainWindow (main_window.py)`: O contêiner principal da aplicação. Gerencia a navegação entre as diferentes telas/views.
    -   `ConfigView (views/config_view.py)`: Tela inicial onde o usuário seleciona diretórios, arquivos ZIP e outras opções de varredura. Interage com `ScanService` para iniciar uma nova varredura.
    -   `ProgressView (views/progress_view.py)`: Um componente (possivelmente um modal ou uma área da `MainWindow`) que exibe o progresso em tempo real da varredura (ex: barra de progresso, arquivos sendo processados). Ouve sinais/eventos do `ScanService`.
    -   `ResultsView (views/results_view.py)`: Tela que exibe os conjuntos de duplicatas encontrados. Permite ao usuário revisar as seleções automáticas e, se desejar, alterá-las antes de confirmar a remoção. Interage com `ScanService` para executar a remoção.
    -   `RestoreView (views/restore_view.py)`: Tela que interage com o `BackupService` para listar os backups disponíveis e permitir que o usuário restaure arquivos removidos.
    -   `ScanWorker (worker.py)`: Um `QObject` com os métodos de varredura que é movido para uma `QThread`. Ele encapsula a chamada ao `ScanService` e emite sinais (`PySide6.QtCore.Signal`) para a thread principal da UI, garantindo que a interface permaneça responsiva.

## 4. Definição das Interfaces Principais

As interfaces são definidas como contratos que a Camada de Aplicação espera que a Camada de Infraestrutura cumpra. A passagem de configurações é feita via construtor (`__init__`) para promover injeção de dependência.

```python
# Em fotix/infrastructure/interfaces.py (conceitual)
from typing import Protocol, Iterator
from pathlib import Path
from fotix.domain.models import FileMeta, DuplicateSet

# --- Interface de Domínio ---
class ISelectionStrategy(Protocol):
    def choose_file_to_keep(self, duplicates: list[FileMeta]) -> FileMeta:
        """Dado um conjunto de arquivos duplicados, retorna o que deve ser mantido."""
        ...

# --- Interfaces de Infraestrutura ---
class IFileSystemService(Protocol):
    def find_media_files(self, paths: list[Path]) -> Iterator[FileMeta]:
        """Encontra todos os arquivos de imagem/vídeo nos caminhos fornecidos, recursivamente."""
        ...
    
    def get_image_resolution(self, file_path: Path) -> tuple[int, int] | None:
        ...

    def move_to_trash(self, file_path: Path) -> None:
        """Move um arquivo para a lixeira do sistema de forma segura."""
        ...

class IZipHandlerService(Protocol):
    def stream_files_from_zip(self, zip_path: Path) -> Iterator[tuple[FileMeta, bytes]]:
        """Lê um arquivo ZIP e retorna um iterador de (metadados, conteúdo_em_bytes) para cada arquivo de mídia interno."""
        ...

class IHashingService(Protocol):
    def calculate_hash(self, file_content_bytes: bytes) -> str:
        """Calcula o hash BLAKE3 para um conteúdo de arquivo em bytes."""
        ...

class IBackupService(Protocol):
    def __init__(self, backup_root_path: Path): ...
    
    def backup_file(self, file_path: Path) -> Path:
        """Copia um arquivo para o diretório de backup e registra no manifesto. Retorna o novo caminho."""
        ...
    
    def restore_file(self, backup_id: str) -> Path:
        """Restaura um arquivo do backup para seu local original. Retorna o caminho restaurado."""
        ...
    
    def list_backups(self) -> list[dict]:
        """Lista os arquivos disponíveis para restauração a partir do manifesto."""
        ...

class IConcurrencyService(Protocol):
    def __init__(self, max_workers: int | None = None): ...

    def map(self, func, iterable) -> Iterator:
        """Aplica uma função a cada item de um iterável em paralelo."""
        ...
```

## 5. Gerenciamento de Dados

A persistência de dados no `Fotix` é minimalista, conforme as restrições:
-   **Dados de Sessão:** Durante a execução de uma varredura, todos os dados (listas de arquivos, hashes, conjuntos de duplicatas) são mantidos em memória, utilizando os modelos Pydantic definidos em `fotix.domain.models`. A arquitetura com iteradores (`Iterator`) e processamento em lote ajuda a controlar o uso de memória.
-   **Persistência de Backup:** O `BackupService` é o único componente que persiste dados em disco. Ele cria um diretório de backup (ex: `C:\Users\User\AppData\Local\Fotix\Backup`) e, dentro dele, mantém um arquivo de manifesto (ex: `manifest.json`). Este JSON armazena um registro de cada arquivo removido, incluindo seu caminho original, o caminho no diretório de backup e um timestamp, permitindo a funcionalidade de restauração.

## 6. Estrutura de Diretórios Proposta

A estrutura segue o layout `src` moderno para um empacotamento limpo e resolução de imports inequívoca.

```
fotix/
├── .gitignore
├── pyproject.toml
├── README.md
├── src/
│   └── fotix/
│       ├── __init__.py
│       ├── __main__.py          # Permite rodar com 'python -m fotix'
│       ├── main.py              # Ponto de entrada, bootstrapping
│       │
│       ├── application/
│       │   ├── __init__.py
│       │   └── services.py        # ScanService
│       │
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── models.py          # SSOT dos modelos Pydantic
│       │   └── strategies.py      # ISelectionStrategy e implementações
│       │
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   ├── backup.py          # BackupService
│       │   ├── concurrency.py     # ConcurrencyService
│       │   ├── file_system.py     # FileSystemService
│       │   ├── hashing.py         # HashingService
│       │   ├── logging.py         # Configuração do logger
│       │   └── zip_handler.py     # ZipHandlerService
│       │
│       └── ui/
│           ├── __init__.py
│           ├── main_window.py
│           ├── signals.py         # Sinais globais da UI
│           ├── worker.py          # QThread/QRunnable para o ScanService
│           └── views/
│               ├── __init__.py
│               ├── config_view.py
│               ├── progress_view.py
│               └── results_view.py
│
└── tests/
    ├── __init__.py
    ├── test_application/
    ├── test_domain/
    └── test_infrastructure/
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
pip-wheel-metadata/
share/python-wheels/
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
.pytest_cache/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
htmlcov/
.tox/

# Caches de ferramentas de desenvolvimento
.ruff_cache/
.pyright_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs e Editores
.idea/
.vscode/
*.swp
*~

# Qt / PySide
# Arquivos gerados pela compilação de .ui e .qrc
*_ui.py
*_rc.py
```

## 8. Considerações de Segurança

-   **Remoção Segura:** A utilização da biblioteca `send2trash` em vez de `os.remove` ou `shutil.rmtree` é um pilar de segurança fundamental. Isso move os arquivos para a lixeira do sistema operacional, fornecendo uma camada de recuperação essencial para o usuário final, prevenindo a perda acidental e permanente de dados.
-   **Validação de Input:** O uso de Pydantic para os modelos de configuração (`ScanConfig`) e de dados (`FileMeta`) garante que os dados que fluem pelo sistema sejam do tipo e formato esperados, prevenindo erros e comportamentos inesperados.
-   **Tratamento de Exceções:** Operações de I/O (leitura, escrita, remoção) na camada de infraestrutura devem ser rigorosamente encapsuladas em blocos `try...except` para lidar com erros de permissão (`PermissionError`), arquivos não encontrados (`FileNotFoundError`) e outros problemas do sistema de arquivos, reportando-os de forma clara para a UI.

## 9. Justificativas e Trade-offs

-   **Arquitetura em Camadas:** Escolhida pela alta manutenibilidade e testabilidade. O trade-off é um leve aumento no "boilerplate" (criação de interfaces, injeção de dependência), que é amplamente compensado pela clareza e robustez em projetos de médio a grande porte.
-   **Padrão Strategy para Seleção:** Isola a lógica de decisão, tornando-a fácil de modificar ou estender (ex: adicionar uma nova estratégia baseada em metadados de vídeo) sem alterar o fluxo principal da aplicação.
-   **Abstração da Infraestrutura:** Envolve um esforço inicial maior para criar wrappers (ex: `FileSystemService`), mas desacopla o núcleo da aplicação de bibliotecas específicas, facilitando futuras atualizações ou substituições de tecnologia (ex: trocar `blake3` por `sha256` exigiria mudar apenas uma classe).
-   **Processamento Assíncrono na UI:** A utilização de um `QThread` (`ScanWorker`) é crucial para não congelar a interface gráfica. O trade-off é a complexidade adicional de gerenciar a comunicação entre threads usando sinais e slots, que é um padrão idiomático e robusto no ecossistema Qt.

## 10. Exemplo de Bootstrapping/Inicialização (`src/fotix/main.py`)

Este trecho conceitual demonstra como os componentes são instanciados e conectados na inicialização, seguindo o princípio de Injeção de Dependência.

```python
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

# Importações das classes concretas e da UI
from fotix.application.services import ScanService
from fotix.domain.strategies import DefaultSelectionStrategy
from fotix.infrastructure.file_system import FileSystemService
from fotix.infrastructure.hashing import HashingService
from fotix.infrastructure.backup import BackupService
from fotix.infrastructure.concurrency import ConcurrencyService
from fotix.infrastructure.zip_handler import ZipHandlerService
from fotix.ui.main_window import MainWindow

def run():
    """Ponto de entrada principal da aplicação."""
    # 1. Configuração (poderia vir de um arquivo de settings ou CLI)
    APP_DATA_PATH = Path(os.getenv("APPDATA")) / "Fotix"
    BACKUP_PATH = APP_DATA_PATH / "Backup"
    BACKUP_PATH.mkdir(parents=True, exist_ok=True)
    MAX_WORKERS = os.cpu_count() or 4

    # 2. Instanciação dos Serviços de Infraestrutura (dependências)
    #    As configurações são passadas via __init__
    file_system_service = FileSystemService()
    hashing_service = HashingService()
    zip_handler_service = ZipHandlerService()
    backup_service = BackupService(backup_root_path=BACKUP_PATH)
    concurrency_service = ConcurrencyService(max_workers=MAX_WORKERS)
    
    # 3. Instanciação da Estratégia de Domínio
    selection_strategy = DefaultSelectionStrategy()

    # 4. Injeção de Dependência: Instanciação do Serviço de Aplicação
    #    Passamos as implementações concretas da infraestrutura para o serviço.
    scan_service = ScanService(
        file_system_service=file_system_service,
        hashing_service=hashing_service,
        zip_handler_service=zip_handler_service,
        backup_service=backup_service,
        concurrency_service=concurrency_service,
        selection_strategy=selection_strategy
    )

    # 5. Inicialização da UI
    #    A janela principal recebe o serviço de aplicação para poder interagir com ele.
    app = QApplication(sys.argv)
    main_window = MainWindow(scan_service=scan_service)
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    run()
```

## 11. Arquivo `pyproject.toml` Proposto

Este arquivo define o projeto, suas dependências e a configuração de ferramentas, garantindo um ambiente de desenvolvimento e teste consistente.

```toml
[project]
name = "fotix"
version = "0.1.0"
description = "Aplicativo desktop para encontrar e remover arquivos de mídia duplicados."
authors = [
    { name = "Seu Nome", email = "seu.email@exemplo.com" },
]
readme = "README.md"
requires-python = ">=3.10"
license = { file = "LICENSE" } # Adicione um arquivo LICENSE
classifiers = [
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Operating System :: Microsoft :: Windows",
    "Topic :: Desktop Environment",
    "Topic :: Utilities",
]

# Dependências de produção
dependencies = [
    "pyside6~=6.6.0",
    "pydantic~=2.5.0",
    "blake3~=0.3.3",
    "stream-unzip~=0.1.0",
    "send2trash~=1.8.2",
]

[project.urls]
Homepage = "https://github.com/seu_usuario/fotix"
Repository = "https://github.com/seu_usuario/fotix"

# Ponto de entrada para executar o aplicativo
[project.scripts]
fotix = "fotix.main:run"

# Dependências de desenvolvimento
[project.optional-dependencies]
dev = [
    "pytest~=7.4.0",
    "pytest-cov~=4.1.0",
    "ruff~=0.1.7",
    "pyright~=1.1.338",
    "pytest-qt~=4.2.0", # Para testar a UI
]

# Configuração do Pytest
[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q --cov=src/fotix --cov-report=term-missing"
testpaths = ["tests"]
# CRUCIAL: Garante que os testes possam importar de 'src/fotix'
pythonpath = ["src"]

# Configuração do Ruff (linter e formatação)
[tool.ruff]
line-length = 88
select = ["E", "F", "W", "I", "UP"] # Standard + isort + pyupgrade
ignore = []
src = ["src", "tests"]

[tool.ruff.mccabe]
max-complexity = 10

# Configuração do Pyright (Type Checker)
[tool.pyright]
include = ["src", "tests"]
exclude = ["**/__pycache__"]
# CRUCIAL: Garante que o VSCode/Pyright encontre os módulos em 'src/'
extraPaths = ["src"]
typeCheckingMode = "basic" # Ou "strict" para maior rigor

reportMissingImports = true
reportMissingTypeStubs = false
```