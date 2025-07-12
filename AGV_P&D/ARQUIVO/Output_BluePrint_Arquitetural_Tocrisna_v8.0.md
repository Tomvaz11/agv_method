Excelente. A seguir, apresento o Blueprint Arquitetural para o projeto `Fotix`, seguindo o template Tocrisna v4.0 e as diretrizes AGV.

***

# Blueprint Arquitetural: Fotix v1.0

Este documento define a arquitetura de alto nível para o projeto Fotix, servindo como a fonte única da verdade para a estrutura técnica e de produto.

## 1. Visão Geral da Arquitetura

A arquitetura escolhida para o Fotix é uma **Arquitetura em Camadas (Layered Architecture)**, com uma clara separação entre Apresentação (UI), Aplicação (Use Cases), Domínio (Core Business Logic) e Infraestrutura (Detalhes Técnicos).

**Justificativa:**
*   **Modularidade e SRP:** Cada camada tem uma responsabilidade única, facilitando o desenvolvimento e a manutenção. A UI não sabe como os arquivos são lidos; o Core não sabe sobre a UI.
*   **Testabilidade:** A camada de Domínio e Aplicação podem ser testadas de forma isolada da UI e do sistema de arquivos real, permitindo testes unitários robustos e rápidos.
*   **Manutenibilidade:** Alterações em uma camada (ex: trocar a biblioteca de GUI ou o algoritmo de hash) têm impacto mínimo nas outras, desde que os contratos (interfaces) sejam respeitados.
*   **Clareza:** A estrutura é intuitiva e amplamente compreendida, reduzindo a curva de aprendizado para novos desenvolvedores.

## 2. Diagrama de Componentes (Simplificado)

```mermaid
graph TD
    subgraph Camada de Apresentação (UI)
        A[fotix.ui.main_window.MainWindow]
        B[fotix.ui.config_view.ConfigView]
        C[fotix.ui.results_view.ResultsView]
        D[fotix.ui.progress_view.ProgressView]
    end

    subgraph Camada de Aplicação
        E[fotix.application.scan_service.ScanService]
    end

    subgraph Camada de Domínio/Core
        F[fotix.core.models]
        G[fotix.core.duplicate_finder.DuplicateFinder]
        H[fotix.core.keeper_selection.KeeperSelector]
    end

    subgraph Camada de Infraestrutura
        I[fotix.infrastructure.file_system_service.FileSystemService]
        J[fotix.infrastructure.hashing_service.HashingService]
        K[fotix.infrastructure.backup_service.BackupService]
        L[fotix.infrastructure.concurrency_service.ConcurrencyService]
        M[fotix.infrastructure.zip_service.ZipService]
        N[fotix.infrastructure.logging_service.LoggingService]
    end

    A --> E
    B --> E
    C --> E
    D --> E

    E --> G
    E --> H
    E --> I
    E --> J
    E --> K
    E --> L
    E --> M
    E --> N

    G --> F
    H --> F
```
*As setas indicam dependências (direção do fluxo de chamadas/importações).*

## 3. Descrição dos Componentes, Interfaces e Modelos de Domínio

### 3.1. Consistência dos Modelos de Dados (SSOT do Domínio)

Esta seção é a Fonte Única da Verdade para as estruturas de dados do projeto. Todos os modelos são definidos aqui e referenciados por outras camadas.

*   **Módulo:** `fotix.core.models`
    *   **Responsabilidade Principal:** Definir as entidades centrais e estruturas de dados do domínio do Fotix. Servir como a fonte única da verdade (SSOT) para os modelos de dados.
    *   **Tecnologias Chave:** Pydantic `BaseModel` para validação, tipagem e serialização.
    *   **Dependências Diretas:** Nenhuma (módulo base).
    *   **Modelos Definidos:**
        ```python
        from pydantic import BaseModel
        from pathlib import Path
        from datetime import datetime

        class MediaFile(BaseModel):
            """Representa um único arquivo de mídia analisado."""
            path: Path
            size_bytes: int
            creation_date: datetime
            file_hash: str | None = None
            resolution: tuple[int, int] | None = None # (width, height) para imagens

        class DuplicateSet(BaseModel):
            """Representa um conjunto de arquivos idênticos, com um eleito para ser mantido."""
            keeper: MediaFile
            duplicates: list[MediaFile]

        class ScanConfig(BaseModel):
            """Configurações para uma operação de escaneamento."""
            search_paths: list[Path]
            include_zips: bool = True
            min_file_size_kb: int = 10 # Ignora arquivos muito pequenos
            backup_location: Path

        class ScanProgress(BaseModel):
            """Estrutura para reportar o progresso da análise."""
            current_stage: str # Ex: "Indexing files", "Hashing files", "Analyzing duplicates"
            processed_files: int
            total_files: int
            current_file: str = ""

        class ScanResult(BaseModel):
            """O resultado final de uma operação de escaneamento."""
            duplicate_sets: list[DuplicateSet]
            total_files_scanned: int
            total_duplicates_found: int
            space_saved_bytes: int
            scan_duration_seconds: float
        ```

### 3.2. Camada de Domínio/Core

Componentes que contêm a lógica de negócio pura, sem dependências de infraestrutura.

*   **Módulo:** `fotix.core.duplicate_finder`
    *   **Responsabilidade Principal:** Receber uma lista de `MediaFile` com hashes e agrupá-los em dicionários ou listas por hash idêntico.
    *   **Tecnologias Chave:** Python (Lógica Pura).
    *   **Dependências Diretas:** `fotix.core.models`.

*   **Módulo:** `fotix.core.keeper_selection`
    *   **Responsabilidade Principal:** Aplicar a lógica de negócio para selecionar o "keeper" de um conjunto de duplicatas. Implementa o algoritmo de decisão (maior resolução, data mais antiga, nome de arquivo limpo).
    *   **Tecnologias Chave:** Python (Lógica Pura).
    *   **Dependências Diretas:** `fotix.core.models`.

### 3.3. Camada de Infraestrutura

Implementações concretas de serviços externos e de baixo nível.

*   **Módulo:** `fotix.infrastructure.file_system_service`
    *   **Responsabilidade Principal:** Abstrair todas as interações diretas com o sistema de arquivos. Mapear informações do sistema de arquivos para o modelo `MediaFile` (parcialmente, sem hash).
    *   **Tecnologias Chave:** `pathlib`, `shutil`, `send2trash`, `os`.
    *   **Dependências Diretas:** `fotix.core.models`.

*   **Módulo:** `fotix.infrastructure.hashing_service`
    *   **Responsabilidade Principal:** Calcular o hash de um arquivo de forma eficiente.
    *   **Tecnologias Chave:** `blake3`.
    *   **Dependências Diretas:** Nenhuma.

*   **Módulo:** `fotix.infrastructure.backup_service`
    *   **Responsabilidade Principal:** Gerenciar o backup e a restauração de arquivos, movendo-os para um local seguro e mantendo um manifesto.
    *   **Tecnologias Chave:** `pathlib`, `shutil`, `json` (para o manifesto).
    *   **Dependências Diretas:** `fotix.core.models`.

*   **Módulo:** `fotix.infrastructure.concurrency_service`
    *   **Responsabilidade Principal:** Fornecer uma abstração para execução de tarefas em paralelo.
    *   **Tecnologias Chave:** `concurrent.futures.ThreadPoolExecutor`.
    *   **Dependências Diretas:** Nenhuma.

*   **Módulo:** `fotix.infrastructure.zip_service`
    *   **Responsabilidade Principal:** Ler e extrair arquivos de um arquivo ZIP de forma progressiva e com baixo uso de memória. Mapear os metadados do arquivo ZIP para o modelo `MediaFile` (parcialmente).
    *   **Tecnologias Chave:** `stream-unzip`.
    *   **Dependências Diretas:** `fotix.core.models`.

*   **Módulo:** `fotix.infrastructure.logging_service`
    *   **Responsabilidade Principal:** Configurar e fornecer uma instância de logger padronizada para todo o aplicativo.
    *   **Tecnologias Chave:** `logging` (stdlib).
    *   **Dependências Diretas:** Nenhuma.

### 3.4. Camada de Aplicação

Orquestra os casos de uso do aplicativo, conectando a UI aos serviços de domínio e infraestrutura.

*   **Módulo:** `fotix.application.scan_service`
    *   **Responsabilidade Principal:** Orquestrar o fluxo completo de análise: receber `ScanConfig` da UI, usar serviços de infraestrutura para listar e hashear arquivos, usar lógica de domínio para encontrar duplicatas e selecionar keepers, e finalmente remover arquivos duplicados usando o `BackupService`. Emite sinais/eventos de progresso.
    *   **Tecnologias Chave:** Python (Lógica de Orquestração).
    *   **Dependências Diretas:** `fotix.core.models`, `fotix.core.duplicate_finder`, `fotix.core.keeper_selection`, e as interfaces dos serviços de infraestrutura.

### 3.5. Camada de Apresentação (UI)

Componentes visuais que interagem com o usuário.

*   **Módulo:** `fotix.ui.main_window`
    *   **Responsabilidade Principal:** Janela principal da aplicação. Contém e gerencia as outras views (`ConfigView`, `ResultsView`, etc.). Atua como um Controller, instanciando e conectando os serviços da camada de aplicação com os componentes da UI. É responsável por mapear os `ScanResult` do domínio para os ViewModels da `ResultsView`.
    *   **Tecnologias Chave:** PySide6.
    *   **Dependências Diretas:** `fotix.application.scan_service`, `fotix.ui.*` (outras views).

*   **Módulo:** `fotix.ui.config_view`
    *   **Responsabilidade Principal:** Fornecer widgets para o usuário selecionar diretórios, configurar opções e iniciar a análise. Emite um objeto `ScanConfig`.
    *   **Tecnologias Chave:** PySide6.
    *   **Dependências Diretas:** `fotix.core.models` (especificamente `ScanConfig`).

*   **Módulo:** `fotix.ui.results_view`
    *   **Responsabilidade Principal:** Exibir os resultados da análise em um formato claro e interativo (ex: tabela ou árvore).
    *   **Tecnologias Chave:** PySide6 (`QTableView` ou `QTreeView`).
    *   **Dependências Diretas:** Nenhuma direta (recebe dados via modelo/sinal).
    *   **Contrato de Dados da View (ViewModel):**
        *   `ResultsViewModel(ViewModel)`: Representa uma única linha na tabela de resultados, correspondendo a um `DuplicateSet` completo.
            ```python
            # Definição conceitual do ViewModel
            class ResultsViewModel:
                keeper_name: str         # "IMG_2023.JPG"
                keeper_path: str         # "C:/Photos/2023"
                keeper_details: str      # "3.5 MB | 4032x3024"
                duplicates_count: int    # 2
                duplicates_summary: str  # "IMG_2023(1).JPG, photo_copy.JPG"
                space_to_be_saved_mb: float # 7.0
            ```
        *   **Mapeamento de Origem:** O `MainWindow` (ou um controller dedicado) receberá o `ScanResult`. Ele irá iterar sobre `ScanResult.duplicate_sets`. Para cada `DuplicateSet` do modelo de domínio, ele criará uma instância do `ResultsViewModel`, preenchendo os campos a partir das propriedades do `keeper` e da lista `duplicates`. Esta lista de `ResultsViewModel`s será então passada para o `QAbstractTableModel` que alimenta a `ResultsView`.

*   **Módulo:** `fotix.ui.progress_view`
    *   **Responsabilidade Principal:** Exibir o progresso de uma operação longa (a análise), incluindo uma barra de progresso e texto de status.
    *   **Tecnologias Chave:** PySide6 (`QProgressBar`, `QLabel`).
    *   **Dependências Diretas:** Nenhuma (reage a sinais/eventos que carregam um objeto `ScanProgress`).

## 4. Definição das Interfaces Principais

Aqui definimos os contratos formais entre os componentes, com foco na injeção de dependências via construtor (`__init__`).

---
**Interface: `IFileSystemService` (implementada por `FileSystemService`)**
```python
class IFileSystemService(Protocol):
    def find_media_files(self, paths: list[Path]) -> Generator[MediaFile, None, None]: ...
    def get_file_size(self, path: Path) -> int: ...
    def get_creation_date(self, path: Path) -> datetime: ...
    def get_image_resolution(self, path: Path) -> tuple[int, int] | None: ...
    def move_to_trash(self, path: Path) -> None: ...
    def create_directory(self, path: Path) -> None: ...
```

---
**Interface: `IHashingService` (implementada por `HashingService`)**
```python
class IHashingService(Protocol):
    # __init__ pode aceitar configuração, como o tamanho do buffer de leitura
    def __init__(self, buffer_size: int = 65536): ...
    def calculate_hash(self, file_path: Path) -> str: ...
```

---
**Interface: `IZipService` (implementada por `ZipService`)**
```python
class IZipService(Protocol):
    def stream_files_from_zip(self, zip_path: Path) -> Generator[tuple[str, datetime, int, IO[bytes]], None, None]:
        """Gera tuplas de (nome_interno, data_mod, tamanho, file_like_object)"""
        ...
```

---
**Interface: `IBackupService` (implementada por `BackupService`)**
```python
class IBackupService(Protocol):
    def __init__(self, backup_root: Path): ...
    def backup_file(self, source_path: Path) -> Path: ...
    def restore_file(self, backup_id: str) -> Path: ...
    def list_backups(self) -> list[dict]: ...
```

---
**Interface: `IConcurrencyService` (implementada por `ConcurrencyService`)**
```python
class IConcurrencyService(Protocol):
    def __init__(self, max_workers: int | None = None): ...
    def map(self, func: Callable, items: Iterable) -> Generator: ...
```

---
**Componente de Aplicação: `ScanService` (Configuração)**
```python
class ScanService:
    def __init__(
        self,
        file_system_service: IFileSystemService,
        hashing_service: IHashingService,
        zip_service: IZipService,
        backup_service: IBackupService,
        concurrency_service: IConcurrencyService,
        duplicate_finder: DuplicateFinder, # Pode ser injetado ou instanciado
        keeper_selector: KeeperSelector,   # Pode ser injetado ou instanciado
        logger: logging.Logger
    ): ...

    def run_scan(self, config: ScanConfig) -> ScanResult: ...
    # Este método emitirá sinais de progresso (ex: usando PySide6.QtCore.Signal)
    # progress_updated = Signal(ScanProgress)
    # scan_finished = Signal(ScanResult)
```

## 5. Gerenciamento de Dados

A persistência de dados é limitada ao sistema de arquivos.
*   **Estado da Aplicação:** O estado é gerenciado em memória durante a execução. A configuração da análise (`ScanConfig`) é criada pela UI e passada para o `ScanService`.
*   **Backups:** O `BackupService` é responsável por persistir os arquivos removidos. Ele gerencia uma estrutura de diretórios dedicada (definida em `ScanConfig.backup_location`) e pode usar um arquivo de manifesto (`manifest.json`) para rastrear metadados sobre os arquivos em backup, facilitando a restauração.
*   **Logs:** O `LoggingService` configura o logging para um arquivo (ex: `fotix.log`), persistindo o histórico de operações e erros.

## 6. Estrutura de Diretórios Proposta

Utilizando o layout `src` para melhor empacotamento e separação de código-fonte de outros arquivos do projeto.

```
fotix/
├── .gitignore
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
├── README.md
├── pyproject.toml         # ou requirements.txt para dependências
├── src/
│   └── fotix/
│       ├── __init__.py
│       ├── __main__.py      # Ponto de entrada da aplicação
│       ├── application/
│       │   ├── __init__.py
│       │   └── scan_service.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── duplicate_finder.py
│       │   └── keeper_selection.py
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   ├── backup_service.py
│       │   ├── concurrency_service.py
│       │   ├── file_system_service.py
│       │   ├── hashing_service.py
│       │   ├── logging_service.py
│       │   └── zip_service.py
│       └── ui/
│           ├── __init__.py
│           ├── main_window.py
│           ├── config_view.py
│           ├── results_view.py
│           └── progress_view.py
└── tests/
    ├── __init__.py
    ├── test_core/
    └── test_application/
```

## 7. Arquivo `.gitignore` Proposto

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
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

# Virtualenv
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs & Editors
.idea/
.vscode/
*.swp
*~
*.sublime-project
*.sublime-workspace

# PySide/PyQt
*.ui
# Se os arquivos .py forem gerados a partir de .ui, adicione-os aqui
# Ex: ui_*.py

# OS-specific
.DS_Store
Thumbs.db
Desktop.ini

# Log files
*.log
logs/

# Test artifacts
.pytest_cache/
.coverage
htmlcov/
```

## 8. Arquivo `README.md` Proposto

```markdown
# Fotix 📷✨

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-em_desenvolvimento-orange.svg)

Um aplicativo desktop inteligente para encontrar e remover arquivos de mídia duplicados, otimizado para grandes coleções.

## Sobre o Projeto

Fotix é uma ferramenta poderosa para fotógrafos, videomakers e qualquer pessoa que lide com grandes volumes de imagens e vídeos. Ele escaneia seus diretórios, incluindo arquivos ZIP, e identifica arquivos **idênticos** com base em seu conteúdo.

Quando duplicatas são encontradas, o Fotix usa um algoritmo inteligente para decidir qual versão manter (baseado em resolução, data e nome do arquivo) e move as cópias indesejadas para uma lixeira segura, com um sistema de backup para fácil restauração.

### Stack Tecnológica

*   **Linguagem:** Python 3.10+
*   **Interface Gráfica (GUI):** PySide6 (Qt for Python)
*   **Motor de Hashing:** BLAKE3
*   **Paralelismo:** `concurrent.futures`
*   **Manipulação de ZIP:** `stream-unzip`
*   **Modelos de Dados:** Pydantic

## Como Começar

Siga estas instruções para obter uma cópia do projeto e executá-la em sua máquina local.

### Pré-requisitos

*   Python 3.10 ou superior
*   Pip (gerenciador de pacotes do Python)

### Instalação

1.  Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/fotix.git
    cd fotix
    ```

2.  Crie e ative um ambiente virtual:
    ```sh
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  Instale as dependências:
    ```sh
    pip install -r requirements.txt 
    # ou pip install -e . se usar pyproject.toml
    ```

4.  Execute a aplicação:
    ```sh
    python src/fotix
    ```

## Como Executar os Testes

Para executar a suíte de testes automatizados, utilize o pytest:

```sh
pytest
```

## Estrutura do Projeto

O projeto segue uma arquitetura em camadas para garantir modularidade e manutenibilidade.

-   `src/fotix/`: Contém todo o código-fonte da aplicação.
    -   `ui/`: Camada de apresentação (componentes PySide6).
    -   `application/`: Camada de orquestração e casos de uso.
    -   `core/`: Camada de domínio, com a lógica de negócio pura e os modelos de dados.
    -   `infrastructure/`: Camada de infraestrutura, com implementações de acesso ao sistema de arquivos, hashing, etc.
-   `tests/`: Contém os testes unitários e de integração.
```

## 9. Arquivo `LICENSE` Proposto

A licença **MIT** é uma excelente escolha padrão, pois é permissiva e amplamente utilizada.

```
MIT License

Copyright (c) [Ano] [Nome do Proprietário do Copyright]

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

## 10. Arquivo `CONTRIBUTING.md` Proposto

```markdown
# Como Contribuir para o Fotix

Agradecemos seu interesse em contribuir! Para garantir a qualidade e a consistência do projeto, pedimos que siga estas diretrizes.

## Método AGV

Este projeto segue os princípios da **Arquitetura Guiada pela Vontade (AGV)**. Isso significa que valorizamos:

1.  **Clareza e Modularidade:** O código deve ser fácil de entender e organizado em componentes com responsabilidades bem definidas.
2.  **Adesão à Arquitetura:** Todas as contribuições devem respeitar a arquitetura em camadas definida no `Blueprint Arquitetural`.
    -   **UI** fala com a **Aplicação**.
    -   **Aplicação** orquestra o **Domínio** e a **Infraestrutura**.
    -   **Domínio** contém a lógica de negócio pura.
    -   **Infraestrutura** lida com detalhes externos (arquivos, rede, etc.).
3.  **Testes são Obrigatórios:** Nenhuma nova funcionalidade ou correção de bug é aceita sem testes unitários ou de integração correspondentes.
4.  **Interfaces Explícitas:** A comunicação entre as camadas deve, sempre que possível, ocorrer através das interfaces definidas.

## Processo de Contribuição

1.  **Crie uma Issue:** Antes de começar a trabalhar, abra uma issue descrevendo a funcionalidade que você quer adicionar ou o bug que pretende corrigir.
2.  **Faça um Fork e Crie um Branch:** Faça um fork do repositório e crie um novo branch para seu trabalho (`git checkout -b feature/nome-da-feature`).
3.  **Desenvolva:** Escreva seu código, seguindo a arquitetura e as convenções do projeto.
4.  **Escreva Testes:** Adicione testes que cubram suas alterações.
5.  **Garanta que os Testes Passem:** Execute `pytest` para garantir que todas as verificações estão passando.
6.  **Faça um Pull Request:** Envie um Pull Request para o branch `main` do repositório original. Descreva claramente suas alterações e vincule a issue que você criou.

Obrigado por ajudar a tornar o Fotix ainda melhor!
```

## 11. Estrutura do `CHANGELOG.md`

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 

### Changed
-

### Fixed
- 

## [0.1.0] - YYYY-MM-DD

### Added
- Initial project structure based on Tocrisna v4.0 Blueprint.
- Core components for file scanning, hashing, and duplicate detection.
- Basic PySide6 UI for configuration and results display.
```

## 12. Considerações de Segurança

*   **Remoção Segura de Arquivos:** O uso de `send2trash` em vez de `os.remove` é fundamental. Isso move os arquivos para a lixeira do sistema operacional, agindo como uma primeira camada de recuperação antes do sistema de backup do próprio Fotix.
*   **Validação de Caminhos:** Todos os caminhos de diretório fornecidos pelo usuário na UI devem ser validados na camada de aplicação para garantir que são diretórios válidos e existentes antes de iniciar o processamento, prevenindo erros e potenciais vulnerabilidades de path traversal.
*   **Tratamento de Exceções:** Operações de I/O (leitura, escrita, remoção) são propensas a falhas (permissões, disco cheio, arquivo em uso). A camada de infraestrutura deve capturar essas exceções (`PermissionError`, `FileNotFoundError`, etc.) e propagá-las de forma controlada ou logá-las, garantindo que a aplicação não trave de forma inesperada.

## 13. Justificativas e Trade-offs

*   **Arquitetura em Camadas vs. Simplicidade:** Embora uma abordagem mais simples (tudo em um ou dois arquivos) pudesse ser mais rápida para um protótipo, a arquitetura em camadas foi escolhida para garantir a manutenibilidade e testabilidade a longo prazo, o que é crucial para um "produto de engenharia".
*   **`stream-unzip` vs. `zipfile` (stdlib):** A biblioteca padrão `zipfile` pode exigir que grandes arquivos ZIP sejam lidos na memória para extração, o que é inviável para o caso de uso. `stream-unzip` foi escolhido especificamente por sua capacidade de processar ZIPs como um stream, mantendo o uso de memória baixo e constante.
*   **Abstração de Concorrência:** Abstrair `concurrent.futures` em um `ConcurrencyService` pode parecer um excesso, mas permite trocar a estratégia de paralelismo no futuro (ex: de `ThreadPoolExecutor` para `ProcessPoolExecutor` para tarefas que consomem muita CPU) em um único local, sem alterar a camada de aplicação.

## 14. Exemplo de Bootstrapping/Inicialização (`src/fotix/__main__.py`)

Este trecho conceitual demonstra como os componentes são instanciados e conectados, respeitando a injeção de dependência.

```python
# src/fotix/__main__.py
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

# Importações das classes de serviço e UI
from fotix.infrastructure.file_system_service import FileSystemService
from fotix.infrastructure.hashing_service import HashingService
from fotix.infrastructure.zip_service import ZipService
from fotix.infrastructure.backup_service import BackupService
from fotix.infrastructure.concurrency_service import ConcurrencyService
from fotix.infrastructure.logging_service import LoggingService
from fotix.core.duplicate_finder import DuplicateFinder
from fotix.core.keeper_selection import KeeperSelector
from fotix.application.scan_service import ScanService
from fotix.ui.main_window import MainWindow
from fotix.core.models import ScanConfig # Usado para valores padrão

def main():
    """Ponto de entrada principal da aplicação Fotix."""

    # 1. Configuração Central
    APP_NAME = "Fotix"
    ORG_NAME = "FotixApp"
    LOG_FILE_PATH = Path.home() / ".fotix" / "fotix.log"
    DEFAULT_BACKUP_PATH = Path.home() / ".fotix" / "backup"

    # 2. Instanciação da Camada de Infraestrutura (com suas configurações)
    logging_service = LoggingService(log_file=LOG_FILE_PATH, level="INFO")
    logger = logging_service.get_logger()

    logger.info("Iniciando Fotix...")

    file_system_service = FileSystemService()
    hashing_service = HashingService()
    zip_service = ZipService()
    concurrency_service = ConcurrencyService(max_workers=4) # Exemplo de configuração
    
    # O BackupService é instanciado com o caminho padrão, mas pode ser reconfigurado pela UI
    backup_service = BackupService(backup_root=DEFAULT_BACKUP_PATH)

    # 3. Instanciação da Camada de Domínio (sem estado, podem ser instanciados diretamente)
    duplicate_finder = DuplicateFinder()
    keeper_selector = KeeperSelector()

    # 4. Injeção de Dependência: Instanciando a Camada de Aplicação
    # O ScanService recebe todas as suas dependências através do construtor.
    scan_service = ScanService(
        file_system_service=file_system_service,
        hashing_service=hashing_service,
        zip_service=zip_service,
        backup_service=backup_service,
        concurrency_service=concurrency_service,
        duplicate_finder=duplicate_finder,
        keeper_selector=keeper_selector,
        logger=logger,
    )

    # 5. Inicialização da Camada de Apresentação (UI)
    app = QApplication(sys.argv)
    app.setOrganizationName(ORG_NAME)
    app.setApplicationName(APP_NAME)
    
    # A MainWindow recebe o serviço de aplicação para poder orquestrar as ações do usuário.
    # Ela também pode receber configurações padrão.
    default_config = ScanConfig(search_paths=[], backup_location=DEFAULT_BACKUP_PATH)
    window = MainWindow(scan_service=scan_service, default_config=default_config)
    window.show()

    logger.info("Aplicação pronta.")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```