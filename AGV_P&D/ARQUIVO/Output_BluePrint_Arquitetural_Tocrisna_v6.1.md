# Proposta de Arquitetura Técnica: Fotix

Este documento descreve a arquitetura técnica de alto nível para o aplicativo `Fotix`, projetado para ser modular, manutenível e escalável, seguindo os princípios da filosofia AGV.

## 1. Visão Geral da Arquitetura

A arquitetura escolhida para o `Fotix` é uma **Arquitetura em Camadas (Layered Architecture)**, fortemente inspirada nos princípios da Clean Architecture. Essa abordagem promove uma clara separação de responsabilidades, desacoplamento e alta testabilidade.

As camadas são organizadas com uma regra de dependência estrita: camadas externas dependem de camadas internas, mas nunca o contrário.

1.  **Camada de Apresentação (UI):** Responsável por toda a interação com o usuário. Contém os componentes visuais (janelas, botões) e lida com eventos de entrada do usuário.
2.  **Camada de Aplicação:** Orquestra os casos de uso do sistema (ex: "Iniciar uma varredura", "Restaurar arquivos"). Ela não contém lógica de negócio, mas utiliza os serviços das camadas de Core e Infraestrutura para executar as tarefas.
3.  **Camada Core (Domínio):** O coração da aplicação. Contém a lógica de negócio pura (ex: como identificar um conjunto de duplicatas, como decidir qual arquivo é o "melhor" para manter) e os modelos de dados canônicos do sistema. Esta camada é totalmente independente de detalhes de infraestrutura (UI, banco de dados, sistema de arquivos).
4.  **Camada de Infraestrutura:** Contém as implementações concretas que interagem com o mundo exterior (sistema de arquivos, bibliotecas de hashing, processamento paralelo, logging). Ela implementa as interfaces definidas pela Camada de Aplicação/Core.

**Justificativa:** Esta abordagem é ideal para o `Fotix` porque:
*   **Isola a Lógica de Negócio:** A lógica de seleção e identificação de duplicatas (`Core`) pode ser testada de forma unitária, sem depender da GUI ou do sistema de arquivos.
*   **Facilita a Manutenção:** Alterar a GUI (`PySide6`) não impacta a lógica de processamento de arquivos. Trocar a biblioteca de hashing exigiria apenas uma mudança na camada de `Infraestrutura`.
*   **Promove Testabilidade:** A injeção de dependência é natural neste modelo. A `Camada de Aplicação` recebe "serviços" da `Infraestrutura` via construtor, permitindo a substituição por mocks em testes.
*   **Mantém a GUI Responsiva:** A `Camada de Aplicação` pode usar um `ConcurrencyService` da `Infraestrutura` para executar tarefas pesadas em threads separadas, comunicando-se com a `UI` via sinais e slots (padrão Observer) para atualizações de progresso, sem travar a interface.

## 2. Diagrama de Componentes (Simplificado)

```mermaid
graph TD
    subgraph Camada de Apresentação (UI)
        UI_Components[Telas e Componentes PySide6]
    end

    subgraph Camada de Aplicação
        A1[scan_service.py]
        A2[backup_service.py]
    end

    subgraph "Camada Core (Domínio)"
        C1[models.py - SSOT]
        C2[duplicate_finder.py]
        C3[selection_strategy.py]
    end

    subgraph Camada de Infraestrutura
        I1[file_system_service.py]
        I2[hash_service.py]
        I3[zip_service.py]
        I4[concurrency_service.py]
        I5[log_service.py]
    end

    %% Fluxo de Dependência
    UI_Components -- Interage com --> A1
    UI_Components -- Interage com --> A2

    A1 -- Usa --> C2
    A1 -- Usa --> C3
    A1 -- Depende de --> I1
    A1 -- Depende de --> I2
    A1 -- Depende de --> I3
    A1 -- Depende de --> I4
    A1 -- Depende de --> I5

    A2 -- Depende de --> I1
    A2 -- Depende de --> I5

    %% A SSOT (Single Source of Truth) dos modelos é usada por todas as camadas
    UI_Components -- Usa Modelos --> C1
    A1 -- Usa Modelos --> C1
    A2 -- Usa Modelos --> C1
    I1 -- Produz/Consome Modelos --> C1
```
*Legenda: A seta `-->` indica uma dependência (ex: "UI depende da Aplicação").*

## 3. Descrição dos Componentes e Modelos de Domínio

### 3.1. Camada Core (Domínio) - `fotix.core`

O coração da lógica de negócio, sem dependências de infraestrutura.

#### `fotix.core.models`
**Responsabilidade Principal:** Fonte Única da Verdade (SSOT) para todas as estruturas de dados do domínio. Define os contratos de dados que fluem entre as camadas.
**Tecnologia Chave:** **Pydantic `BaseModel`** para validação, tipagem e serialização.
**Dependências Diretas:** Nenhuma (além de `pydantic` e tipos Python).
**Modelos Principais:**
*   `FileRecord(BaseModel)`: Representa um arquivo individual com seus metadados.
    *   `path: Path`
    *   `size_bytes: int`
    *   `creation_date: datetime`
    *   `resolution: Optional[Tuple[int, int]]`
    *   `file_hash: Optional[str]`
*   `DuplicateSet(BaseModel)`: Representa um conjunto de arquivos idênticos.
    *   `files: List[FileRecord]`
    *   `file_hash: str`
*   `ScanSettings(BaseModel)`: Configurações para uma operação de varredura.
    *   `target_paths: List[Path]`
    *   `include_zips: bool`
    *   `min_file_size_mb: float`
*   `ScanResult(BaseModel)`: Resultado de uma varredura completa.
    *   `duplicate_sets: List[DuplicateSet]`
    *   `total_files_scanned: int`
    *   `total_space_saved_bytes: int`
*   `BackupManifest(BaseModel)`: Estrutura do arquivo que gerencia o backup.
    *   `backup_id: UUID`
    *   `timestamp: datetime`
    *   `original_path: Path`
    *   `backup_path: Path`

---

#### `fotix.core.duplicate_finder`
**Responsabilidade Principal:** Implementa a lógica pura de identificação de duplicatas a partir de uma lista de `FileRecord`. Agrupa arquivos por tamanho e depois por hash.
**Tecnologia Chave:** Python (Lógica Pura).
**Dependências Diretas:** `fotix.core.models`.

---

#### `fotix.core.selection_strategy`
**Responsabilidade Principal:** Implementa o **Padrão Strategy** para decidir qual arquivo manter de um `DuplicateSet`. A lógica é baseada em resolução, data e nome do arquivo.
**Tecnologia Chave:** Python (Lógica Pura).
**Dependências Diretas:** `fotix.core.models`.

---

### 3.2. Camada de Infraestrutura - `fotix.infrastructure`

Implementações concretas que interagem com o sistema operacional e bibliotecas de baixo nível.

#### `fotix.infrastructure.file_system_service`
**Responsabilidade Principal:** Abstrai todas as interações com o sistema de arquivos. Mapeia os dados brutos de arquivos para os modelos `FileRecord`.
**Tecnologia Chave:** `pathlib`, `shutil`, `send2trash`, `os`.
**Dependências Diretas:** `fotix.core.models`.

---

#### `fotix.infrastructure.hash_service`
**Responsabilidade Principal:** Abstrai o cálculo de hash de arquivos.
**Tecnologia Chave:** `blake3`.
**Dependências Diretas:** Nenhuma (além de `blake3`).

---

#### `fotix.infrastructure.zip_service`
**Responsabilidade Principal:** Abstrai a leitura e extração de arquivos de dentro de arquivos ZIP de forma eficiente.
**Tecnologia Chave:** `stream-unzip`.
**Dependências Diretas:** Nenhuma (além de `stream-unzip`).

---

#### `fotix.infrastructure.concurrency_service`
**Responsabilidade Principal:** Abstrai a execução de tarefas em paralelo para otimizar o uso de CPU.
**Tecnologia Chave:** `concurrent.futures.ThreadPoolExecutor`.
**Dependências Diretas:** Nenhuma.

---

#### `fotix.infrastructure.log_service`
**Responsabilidade Principal:** Configura e fornece uma interface padronizada para o sistema de logging da aplicação.
**Tecnologia Chave:** `logging` (stdlib).
**Dependências Diretas:** Nenhuma.

---

### 3.3. Camada de Aplicação - `fotix.application`

Orquestra os casos de uso do sistema.

#### `fotix.application.scan_service`
**Responsabilidade Principal:** Orquestra o caso de uso principal: "Escanear e Limpar Duplicatas". Utiliza os serviços de infraestrutura para obter dados, os serviços do core para processá-los e notifica a UI sobre o progresso (Padrão Observer).
**Tecnologia Chave:** Python (Lógica Pura de Orquestração).
**Dependências Diretas:** `fotix.core.*`, `fotix.application.backup_service`, `fotix.infrastructure.*` (interfaces).

---

#### `fotix.application.backup_service`
**Responsabilidade Principal:** Gerencia o ciclo de vida dos backups: mover arquivos para a área de backup, registrar em um manifesto e restaurá-los.
**Tecnologia Chave:** Python (Lógica Pura de Orquestração).
**Dependências Diretas:** `fotix.core.models`, `fotix.infrastructure.file_system_service`, `fotix.infrastructure.log_service`.

---

### 3.4. Camada de Apresentação (UI) - `fotix.ui`

A interface gráfica com o usuário.

**Tecnologia Chave:** **PySide6**.
**Dependências Diretas:** `fotix.application.*` (para invocar casos de uso).

**Decomposição dos Componentes de UI:**
*   **`MainWindow`**: A janela principal da aplicação. Contém o layout geral e orquestra a exibição das outras views.
    *   **Interage com:** `ScanService`, `BackupService`.
*   **`SettingsView`**: Um widget ou diálogo onde o usuário seleciona os diretórios a serem escaneados, define filtros (tamanho mínimo, etc.) e inicia o processo.
    *   **Interage com:** `ScanService` (para iniciar a varredura).
*   **`ProgressView`**: Exibe o progresso da varredura em tempo real (barra de progresso, arquivo atual, estatísticas). Ouve os sinais emitidos pelo `ScanService`.
    *   **Interage com:** `ScanService` (recebe atualizações).
*   **`ResultsView`**: Apresenta os conjuntos de duplicatas encontrados em uma tabela ou lista. Permite ao usuário revisar as decisões automáticas e, opcionalmente, intervir antes da remoção.
    *   **Interage com:** `ScanService` (para obter resultados e confirmar a limpeza).
*   **`RestoreView`**: Uma tela para visualizar os backups existentes (lidos do manifesto) e permitir que o usuário restaure arquivos ou grupos de arquivos para suas localizações originais.
    *   **Interage com:** `BackupService`.

---

## 4. Definição das Interfaces Principais

As interfaces são definidas como classes com métodos que serão implementados na camada de infraestrutura. A injeção de dependência ocorrerá via construtor (`__init__`).

```python
# fotix/infrastructure/interfaces.py (Conceitual)
from abc import ABC, abstractmethod
from typing import List, Generator, Tuple
from pathlib import Path
from fotix.core.models import FileRecord, ScanSettings, DuplicateSet, BackupManifest

class IFileSystemService(ABC):
    def __init__(self, backup_root_dir: Path): ...
    @abstractmethod
    def find_files(self, settings: ScanSettings) -> Generator[Path, None, None]: ...
    @abstractmethod
    def get_file_metadata(self, path: Path) -> FileRecord: ...
    @abstractmethod
    def move_to_backup(self, file_path: Path) -> Path: ...
    @abstractmethod
    def restore_from_backup(self, backup_path: Path, original_path: Path) -> None: ...
    @abstractmethod
    def read_backup_manifests(self) -> List[BackupManifest]: ...
    @abstractmethod
    def write_backup_manifest(self, manifest: BackupManifest) -> None: ...

class IHashService(ABC):
    @abstractmethod
    def calculate_file_hash(self, file_path: Path) -> str: ...

class IZipService(ABC):
    @abstractmethod
    def stream_unzip(self, zip_path: Path) -> Generator[Tuple[str, bytes], None, None]: ...

class IConcurrencyService(ABC):
    def __init__(self, max_workers: int): ...
    @abstractmethod
    def run_in_parallel(self, func, items: List) -> List: ...

class ISelectionStrategy(ABC):
    @abstractmethod
    def choose_best_file(self, duplicate_set: DuplicateSet) -> FileRecord: ...
```

**Exemplo de Construção e Injeção:**

```python
# fotix/application/scan_service.py
from fotix.infrastructure.interfaces import *
from fotix.core.models import ScanSettings, ScanResult

class ScanService:
    def __init__(
        self,
        file_system_service: IFileSystemService,
        hash_service: IHashService,
        concurrency_service: IConcurrencyService,
        selection_strategy: ISelectionStrategy,
        # ... outros serviços injetados
    ):
        # As configurações (como max_workers) já foram passadas na instanciação dos serviços
        self.fs = file_system_service
        self.hasher = hash_service
        self.concurrency = concurrency_service
        self.strategy = selection_strategy
        # ...
    
    def execute_scan(self, settings: ScanSettings) -> ScanResult:
        # 1. Usa self.fs para encontrar arquivos
        # 2. Usa self.concurrency e self.hasher para calcular hashes em paralelo
        # 3. Usa a lógica do core para agrupar duplicatas
        # 4. Usa self.strategy para escolher qual arquivo manter
        # 5. Retorna o ScanResult
        ...
```

## 5. Gerenciamento de Dados

A persistência de dados no `Fotix` é limitada e baseada no sistema de arquivos:
*   **Dados do Usuário:** São os próprios arquivos de imagem e vídeo, que não são alterados até a fase de remoção.
*   **Dados de Backup:** Os arquivos removidos são movidos para um diretório de backup seguro (ex: `C:\Users\<user>\AppData\Local\Fotix\Backup`).
*   **Manifesto de Backup:** Para cada operação de backup, um arquivo JSON (seguindo o modelo `BackupManifest` de Pydantic) será salvo no diretório de backup. Ele registrará o caminho original do arquivo, o novo caminho no backup e um timestamp. O `BackupService` usará esses manifestos para popular a `RestoreView`.

## 6. Estrutura de Diretórios Proposta

A estrutura `src` é adotada para uma separação clara entre o código-fonte do pacote e outros artefatos do projeto.

```
fotix-project/
├── .gitignore
├── pyproject.toml
├── README.md
├── scripts/
│   └── build.py
├── src/
│   └── fotix/
│       ├── __init__.py
│       ├── main.py                 # Ponto de entrada, bootstrapping
│       ├── application/
│       │   ├── __init__.py
│       │   ├── scan_service.py
│       │   └── backup_service.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── duplicate_finder.py
│       │   └── selection_strategy.py
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   ├── interfaces.py
│       │   ├── file_system_service.py
│       │   ├── hash_service.py
│       │   ├── zip_service.py
│       │   ├── concurrency_service.py
│       │   └── log_service.py
│       └── ui/
│           ├── __init__.py
│           ├── main_window.py
│           ├── widgets/
│           │   ├── settings_view.py
│           │   └── results_view.py
│           └── assets/
│               └── icon.png
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_application/
    ├── test_core/
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
*.egg-info/
.installed.cfg
*.egg
MANUFTAMER.v1/

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.pytest_cache/
.hypothesis/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE specific
.idea/
.vscode/
*.swp
*.swo

# Qt/PySide specific
*.ui.py  # Generated from .ui files

# Fotix specific
logs/
fotix_backup/
```

## 8. Considerações de Segurança

*   **Remoção Segura:** A utilização de `send2trash` em vez de `os.remove` é um requisito fundamental, movendo arquivos para a Lixeira do sistema em vez de excluí-los permanentemente por padrão.
*   **Validação de Caminho:** Embora o usuário selecione os diretórios via GUI, qualquer entrada de caminho deve ser normalizada e validada para evitar ataques de *Path Traversal*. A biblioteca `pathlib` ajuda a mitigar esses riscos.
*   **Não Execução de Código:** O aplicativo apenas lê e move arquivos de mídia. Não há `eval()` ou execução de código de fontes não confiáveis.
*   **Backup:** O sistema de backup automático é a principal medida de segurança contra remoções acidentais.

## 9. Justificativas e Trade-offs

*   **Decisão:** Adotar uma Arquitetura em Camadas.
    *   **Justificativa:** Proporciona o mais alto grau de modularidade e testabilidade, alinhado com os princípios AGV. Permite que o core do `Fotix` evolua independentemente da UI ou das bibliotecas de sistema de arquivos.
    *   **Trade-off:** Introduz uma pequena quantidade de "boilerplate" na forma de classes de serviço e interfaces de abstração. O ganho em manutenibilidade e resiliência a longo prazo supera significativamente o custo inicial de desenvolvimento.
*   **Decisão:** Usar `concurrent.futures` em vez de `asyncio`.
    *   **Justificativa:** As operações principais (hashing de arquivos, I/O) são vinculadas à CPU e ao disco. `ThreadPoolExecutor` do `concurrent.futures` é uma solução mais simples e direta para paralelizar essas tarefas bloqueantes do que o `asyncio`, que é mais adequado para I/O de rede com muitas conexões simultâneas.

## 10. Exemplo de Bootstrapping/Inicialização

```python
# src/fotix/main.py
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from fotix.ui.main_window import MainWindow
from fotix.application.scan_service import ScanService
from fotix.application.backup_service import BackupService
from fotix.infrastructure.file_system_service import ConcreteFileSystemService
from fotix.infrastructure.hash_service import ConcreteHashService
from fotix.infrastructure.concurrency_service import ConcreteConcurrencyService
from fotix.core.selection_strategy import DefaultSelectionStrategy

def main():
    """Ponto de entrada que instancia e injeta as dependências."""
    # 1. Configuração
    # Em uma aplicação real, isso viria de um arquivo de config ou de settings da UI
    config = {
        "backup_root": Path.home() / "AppData" / "Local" / "Fotix" / "Backup",
        "max_workers": 4, 
    }
    config["backup_root"].mkdir(parents=True, exist_ok=True)

    # 2. Instanciação dos Serviços de Infraestrutura (com suas configs)
    # A configuração é passada via __init__
    fs_service = ConcreteFileSystemService(backup_root_dir=config["backup_root"])
    hash_service = ConcreteHashService()
    concurrency_service = ConcreteConcurrencyService(max_workers=config["max_workers"])
    
    # 3. Instanciação dos Componentes do Core
    selection_strategy = DefaultSelectionStrategy()

    # 4. Instanciação dos Serviços de Aplicação (Injetando dependências)
    backup_service_instance = BackupService(file_system_service=fs_service)
    
    scan_service_instance = ScanService(
        file_system_service=fs_service,
        hash_service=hash_service,
        concurrency_service=concurrency_service,
        selection_strategy=selection_strategy,
        backup_service=backup_service_instance
    )

    # 5. Instanciação da UI (Injetando os serviços de aplicação)
    app = QApplication(sys.argv)
    main_window = MainWindow(
        scan_service=scan_service_instance,
        backup_service=backup_service_instance
    )
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

## 11. Arquivo `pyproject.toml` Proposto

```toml
[project]
name = "fotix"
version = "1.0.0"
description = "Aplicativo desktop para localizar e remover arquivos de mídia duplicados."
authors = [
    { name = "AGV AI", email = "ai@example.com" },
]
readme = "README.md"
requires-python = ">=3.10"
classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Operating System :: Microsoft :: Windows",
    "Topic :: Desktop Environment",
    "Topic :: Utilities",
]

# Lista de dependências essenciais do projeto
dependencies = [
    "pyside6==6.6.0",
    "blake3==0.3.3",
    "send2trash==1.8.2",
    "stream-unzip==0.0.81",
    "pydantic==2.4.2",
]

[project.optional-dependencies]
dev = [
    "pytest==7.4.2",
    "pytest-cov==4.1.0",
    "pyright==1.1.328",
    "ruff==0.0.292",
]

[project.scripts]
fotix = "fotix.main:main"

# Configuração do Ruff (linter/formatter)
[tool.ruff]
line-length = 88
select = ["E", "F", "W", "I", "UP", "B", "C4"]
ignore = []

# CRUCIAL: Configuração do Pytest para encontrar os módulos em src/
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]

# CRUCIAL: Configuração do Pyright (ou Pylance no VSCode) para análise estática
[tool.pyright]
include = ["src", "tests"]
exclude = ["**/node_modules", "**/__pycache__"]
# Aponta para o diretório src para que imports como "from fotix.core import models" funcionem
extraPaths = ["src"]
reportMissingImports = true
reportUnusedVariable = "warning"
pythonVersion = "3.10"
pythonPlatform = "Windows"
```