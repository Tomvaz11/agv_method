# Blueprint Arquitetural: Fotix

Este documento detalha a arquitetura técnica de alto nível para o `Fotix`, um aplicativo desktop para localização e remoção de arquivos de mídia duplicados.

## 1. Visão Geral da Arquitetura

A arquitetura proposta para o `Fotix` é uma **Arquitetura em Camadas com Inversão de Dependência**, inspirada em princípios da Clean Architecture / Arquitetura Hexagonal. Essa abordagem foi escolhida para maximizar a modularidade, testabilidade e manutenibilidade do código.

As camadas são:

1.  **Camada de Apresentação (UI):** Responsável pela interface com o usuário. Contém os componentes visuais e a lógica de apresentação.
2.  **Camada de Aplicação:** Orquestra os casos de uso do sistema. Atua como um intermediário entre a UI e o Domínio, sem conter lógica de negócio.
3.  **Camada de Domínio (Core):** O coração da aplicação. Contém os modelos de dados (entidades) e a lógica de negócio pura (ex: algoritmo de seleção de arquivo), sem nenhuma dependência de frameworks externos ou de infraestrutura.
4.  **Camada de Infraestrutura:** Implementa as interfaces definidas pela Camada de Aplicação para interagir com o "mundo exterior" (sistema de arquivos, bibliotecas de hashing, GUI, etc.).

O princípio de Inversão de Dependência é fundamental: as camadas superiores (Aplicação, Domínio) definem interfaces (contratos) que as camadas inferiores (Infraestrutura) devem implementar. Isso desacopla a lógica de negócio das implementações técnicas concretas.

## 2. Diagrama de Componentes (Simplificado)

```mermaid
graph TD
    subgraph Camada de Apresentação (UI)
        A1(fotix.ui)
    end

    subgraph Camada de Aplicação
        B1(fotix.application.services)
    end

    subgraph Camada de Domínio (Core)
        C1(fotix.domain.models)
        C2(fotix.domain.logic)
    end

    subgraph Camada de Infraestrutura
        D1(fotix.infrastructure.filesystem_service)
        D2(fotix.infrastructure.hashing_service)
        D3(fotix.infrastructure.concurrency_service)
        D4(fotix.infrastructure.backup_service)
        D5(fotix.infrastructure.logging_service)
    end

    subgraph Contratos (Interfaces)
        I1(fotix.application.interfaces)
    end

    A1 -- Interage com --> B1
    B1 -- Depende de --> I1
    B1 -- Depende de --> C1
    B1 -- Depende de --> C2

    D1 -- Implementa --> I1
    D2 -- Implementa --> I1
    D3 -- Implementa --> I1
    D4 -- Implementa --> I1
    
    C2 -- Usa --> C1

    style I1 fill:#f9f,stroke:#333,stroke-width:2px
```
*As setas indicam dependências de código (quem importa quem).*

## 3. Descrição dos Componentes, Interfaces e Modelos de Domínio

### 3.1. Consistência dos Modelos de Dados (SSOT do Domínio)

#### **Módulo: `fotix.domain.models`**
-   **Responsabilidade Principal:** Define todas as estruturas de dados canônicas (entidades e DTOs) do projeto, servindo como a Fonte Única da Verdade (SSOT). Garante validação de dados na criação dos objetos.
-   **Tecnologias Chave:** Pydantic `BaseModel` para definição, validação e serialização de todos os modelos.
-   **Dependências Diretas:** Nenhuma (apenas bibliotecas externas como Pydantic).
-   **Modelos Definidos:**
    -   `ScanConfig(BaseModel)`: Configurações de uma varredura.
        -   `target_paths: list[Path]`
        -   `include_zips: bool = True`
        -   `recursive: bool = True`
    -   `MediaFile(BaseModel)`: Representa um arquivo de mídia analisado.
        -   `path: Path`
        -   `size: int`
        -   `creation_time: datetime`
        -   `resolution: tuple[int, int] | None`
        -   `file_hash: str | None = None`
    -   `DuplicateSet(BaseModel)`: Um conjunto de arquivos idênticos.
        -   `files: list[MediaFile]`
        -   `keeper: MediaFile | None = None` # O arquivo a ser mantido
        -   `duplicates_to_remove: list[MediaFile] = []` # Os arquivos a serem removidos
    -   `ScanResult(BaseModel)`: O resultado agregado de uma varredura completa.
        -   `total_files_scanned: int`
        -   `total_space_saved: int`
        -   `duplicate_sets_found: list[DuplicateSet]`
    -   `BackupInfo(BaseModel)`: Informações sobre um arquivo que foi movido para o backup.
        -   `original_path: Path`
        -   `backup_path: Path`
        -   `timestamp: datetime`

---

### 3.2. Outros Componentes

#### **Camada de Domínio (Core)**

-   **Módulo:** `fotix.domain.logic.keeper_selection`
    -   **Responsabilidade Principal:** Implementa a lógica de negócio pura para decidir qual arquivo manter em um `DuplicateSet`. Encapsula as regras de negócio (maior resolução, data mais antiga, nome de arquivo "limpo").
    -   **Tecnologias Chave:** Python (Lógica Pura).
    -   **Dependências Diretas:** `fotix.domain.models`.

#### **Camada de Aplicação**

-   **Módulo:** `fotix.application.interfaces`
    -   **Responsabilidade Principal:** Define os contratos (interfaces abstratas) que a Camada de Infraestrutura deve implementar. Isso desacopla a aplicação das implementações concretas.
    -   **Tecnologias Chave:** `typing.Protocol` ou `abc.ABC`.
    -   **Dependências Diretas:** `fotix.domain.models`.

-   **Módulo:** `fotix.application.services.scan_service`
    -   **Responsabilidade Principal:** Orquestra o caso de uso principal: "Executar Varredura de Duplicatas". Coordena a busca de arquivos, hashing, identificação de duplicatas, seleção do "keeper" e a remoção/backup, utilizando os serviços de infraestrutura através de suas interfaces. Gerencia o progresso e reporta o status.
    -   **Tecnologias Chave:** Python (Lógica Pura de orquestração).
    -   **Dependências Diretas:** `fotix.application.interfaces`, `fotix.domain.models`, `fotix.domain.logic.keeper_selection`.

#### **Camada de Infraestrutura**

-   **Módulo:** `fotix.infrastructure.filesystem_service`
    -   **Responsabilidade Principal:** Implementa a interface `IFileSystemService`. Lida com todas as interações de baixo nível com o sistema de arquivos: listar arquivos, obter metadados (tamanho, data), ler arquivos ZIP de forma progressiva e mover/deletar arquivos. Mapeia os dados brutos do sistema de arquivos para o modelo `MediaFile`.
    -   **Tecnologias Chave:** `pathlib`, `shutil`, `stream-unzip`.
    -   **Dependências Diretas:** `fotix.application.interfaces`, `fotix.domain.models`.

-   **Módulo:** `fotix.infrastructure.hashing_service`
    -   **Responsabilidade Principal:** Implementa a interface `IHashingService`. Calcula o hash de um arquivo de forma eficiente.
    -   **Tecnologias Chave:** `blake3`.
    -   **Dependências Diretas:** `fotix.application.interfaces`.

-   **Módulo:** `fotix.infrastructure.concurrency_service`
    -   **Responsabilidade Principal:** Implementa a interface `IConcurrencyService`. Abstrai a execução paralela de tarefas (como hashing de múltiplos arquivos), gerenciando um pool de processos ou threads.
    -   **Tecnologias Chave:** `concurrent.futures`.
    -   **Dependências Diretas:** `fotix.application.interfaces`.

-   **Módulo:** `fotix.infrastructure.backup_service`
    -   **Responsabilidade Principal:** Implementa a interface `IBackupService`. Gerencia a remoção segura de arquivos (movendo-os para uma pasta de backup) e sua posterior restauração.
    -   **Tecnologias Chave:** `send2trash`, `shutil`.
    -   **Dependências Diretas:** `fotix.application.interfaces`, `fotix.domain.models`.

-   **Módulo:** `fotix.infrastructure.logging_service`
    -   **Responsabilidade Principal:** Implementa a interface `ILoggingService`. Configura e fornece uma instância de logger para ser usada em toda a aplicação.
    -   **Tecnologias Chave:** `logging` (stdlib).
    -   **Dependências Diretas:** `fotix.application.interfaces`.

#### **Camada de Apresentação (UI)**

-   **Módulo:** `fotix.ui`
    -   **Responsabilidade Principal:** Construir e gerenciar a Interface Gráfica do Usuário. Lida com a entrada do usuário e exibe os dados e o progresso da aplicação. Comunica-se exclusivamente com os serviços da Camada de Aplicação.
    -   **Tecnologias Chave:** PySide6 (Qt for Python).
    -   **Dependências Diretas:** `fotix.application.services.scan_service`, `fotix.domain.models` (para exibir os dados).
    -   **Decomposição em Componentes/Telas:**
        1.  **`MainWindow (main_window.py)`**: A janela principal da aplicação. Age como um contêiner para as outras views. Inicia e controla o `QThread` para as operações de longa duração.
        2.  **`SettingsView (settings_view.py)`**: Um widget/tela onde o usuário seleciona os diretórios a serem escaneados, define se a busca será recursiva e se arquivos ZIP devem ser incluídos. Interage com `ScanService` para iniciar uma nova varredura.
        3.  **`ProgressView (progress_view.py)`**: Um widget/tela que exibe o progresso da varredura em tempo real (barra de progresso, arquivos sendo analisados) e um log de eventos. Conecta-se a sinais emitidos pelo `ScanService`.
        4.  **`ResultsView (results_view.py)`**: Após a varredura, esta tela exibe os conjuntos de duplicatas encontrados, permitindo ao usuário revisar as decisões automáticas antes de confirmar a exclusão. Interage com `ScanService` para confirmar a remoção.
        5.  **`RestoreView (restore_view.py)`**: Uma tela para visualizar os backups existentes e restaurar arquivos removidos para seus locais originais. Interage com o `BackupService` (via `ScanService` ou um novo `RestoreService` na camada de aplicação).

## 4. Definição das Interfaces Principais

As interfaces são definidas em `fotix.application.interfaces` e são cruciais para o desacoplamento.

```python
# fotix/application/interfaces.py

from typing import Protocol, Iterable, Callable
from pathlib import Path
from fotix.domain.models import MediaFile, DuplicateSet, ScanConfig, BackupInfo

# --- Interfaces de Serviço ---

class IFileSystemService(Protocol):
    def find_media_files(self, config: ScanConfig) -> Iterable[MediaFile]:
        """Encontra e retorna um iterador de MediaFiles com base na configuração."""
        ...

    def get_file_bytes_chunked(self, path: Path) -> Iterable[bytes]:
        """Lê um arquivo em pedaços (chunks) para hashing eficiente."""
        ...

class IHashingService(Protocol):
    def calculate_hash(self, file_path: Path, file_system_service: IFileSystemService) -> str:
        """Calcula o hash de um arquivo usando o serviço de filesystem."""
        ...

class IBackupService(Protocol):
    def backup_file(self, file_to_backup: MediaFile) -> BackupInfo:
        """Move um arquivo para a localização de backup e retorna informações sobre ele."""
        ...

    def restore_file(self, backup_info: BackupInfo) -> Path:
        """Restaura um arquivo do backup para sua localização original."""
        ...

    def list_backups(self) -> list[BackupInfo]:
        """Lista todos os arquivos atualmente no backup."""
        ...

class IConcurrencyService(Protocol):
    def run_parallel(self, tasks: Iterable[Callable], max_workers: int | None = None) -> None:
        """Executa uma coleção de tarefas (callables) em paralelo."""
        ...
        
class ILoggingService(Protocol):
    def info(self, message: str) -> None: ...
    def warning(self, message: str) -> None: ...
    def error(self, message: str, exc_info: bool = False) -> None: ...

# --- Configuração e Construção de Componentes (via __init__) ---

# Exemplo: BackupService
class BackupService: # fotix.infrastructure.backup_service.py
    def __init__(self, backup_root_path: Path, logger: ILoggingService):
        """
        Recebe suas dependências e configurações via construtor.
        - backup_root_path: O diretório raiz onde os backups serão armazenados.
        - logger: Uma instância de um serviço de logging.
        """
        self._backup_root = backup_root_path
        self._logger = logger
        if not self._backup_root.exists():
            self._backup_root.mkdir(parents=True)
        # ... resto da implementação

# Exemplo: ScanService
class ScanService: # fotix.application.services.scan_service.py
    def __init__(
        self,
        fs_service: IFileSystemService,
        hash_service: IHashingService,
        concurrency_service: IConcurrencyService,
        backup_service: IBackupService,
        logger: ILoggingService
    ):
        """
        ScanService é construído com implementações concretas das interfaces
        de que necessita (Injeção de Dependência).
        """
        self.fs_service = fs_service
        self.hash_service = hash_service
        # ... e assim por diante
```

## 5. Gerenciamento de Dados

Não há um banco de dados tradicional. A persistência de dados se limita a:

1.  **Backup de Arquivos:** Os arquivos marcados para remoção são fisicamente movidos para um diretório de backup (`~/.fotix/backup/`). A estrutura de diretórios original pode ser preservada dentro do backup para facilitar a restauração.
2.  **Logs:** Logs de operação são escritos em arquivos de texto em `~/.fotix/logs/` para auditoria e depuração.
3.  **Configurações (se necessário):** Configurações simples do usuário (como o último diretório usado) podem ser salvas em um arquivo de configuração (ex: `config.ini` ou `config.json`) em `~/.fotix/`.

## 6. Estrutura de Diretórios Proposta (`src` layout)

```
fotix-project/
├── .gitignore
├── .venv/
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── pyproject.toml       # Para dependências (Poetry/Hatch) e configurações do projeto
├── src/
│   └── fotix/
│       ├── __init__.py
│       ├── __main__.py      # Ponto de entrada (executa a UI)
│       │
│       ├── application/
│       │   ├── __init__.py
│       │   ├── interfaces.py
│       │   └── services/
│       │       ├── __init__.py
│       │       └── scan_service.py
│       │
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   └── logic/
│       │       ├── __init__.py
│       │       └── keeper_selection.py
│       │
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   ├── backup_service.py
│       │   ├── concurrency_service.py
│       │   ├── filesystem_service.py
│       │   ├── hashing_service.py
│       │   └── logging_service.py
│       │
│       └── ui/
│           ├── __init__.py
│           ├── assets/           # Ícones, etc.
│           ├── main_window.py
│           ├── progress_view.py
│           ├── restore_view.py
│           ├── results_view.py
│           └── settings_view.py
│
└── tests/
    ├── __init__.py
    ├── test_application/
    ├── test_domain/
    └── test_infrastructure/
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
.venv/
venv/
ENV/
env/
env.bak/
venv.bak/

# Environment variables
.env
.env.*

# IDEs
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/
*.cover
nosetests.xml
coverage.xml

# Fotix specific
.fotix/
```

## 8. Arquivo `README.md` Proposto

```markdown
# Fotix

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)

Uma aplicação desktop robusta para encontrar e remover arquivos de mídia duplicados de forma inteligente e segura.

## Sobre o Projeto

Fotix é uma ferramenta desenvolvida em Python e PySide6 projetada para ajudar usuários a liberar espaço em disco, organizando suas coleções de fotos e vídeos. Ele escaneia diretórios e arquivos ZIP, identifica arquivos **idênticos** através de hashing (BLAKE3) e utiliza um algoritmo inteligente para decidir qual cópia manter com base em critérios como resolução, data de criação e nome do arquivo.

### Funcionalidades Chave

*   **Análise Profunda:** Varre diretórios locais e arquivos ZIP.
*   **Detecção Precisa:** Usa hashing BLAKE3 para identificar duplicatas idênticas.
*   **Seleção Inteligente:** Automaticamente sugere qual arquivo manter.
*   **Remoção Segura:** Move arquivos para uma lixeira/backup interno para fácil restauração.
*   **Desempenho Otimizado:** Utiliza processamento paralelo para acelerar a análise de grandes volumes de dados.
*   **Interface Intuitiva:** UI limpa e fácil de usar, construída com PySide6.

## Stack Tecnológica

*   **Linguagem:** Python 3.10+
*   **Interface Gráfica (GUI):** PySide6 (Qt for Python)
*   **Motor de Hashing:** `blake3`
*   **Manipulação de Arquivos:** `pathlib`, `shutil`, `send2trash`
*   **Processamento Paralelo:** `concurrent.futures`
*   **Leitura de ZIPs:** `stream-unzip`
*   **Modelagem de Dados:** `pydantic`

## Como Começar

Siga estas instruções para obter uma cópia do projeto em execução em sua máquina local para desenvolvimento e testes.

### Pré-requisitos

*   Python 3.10 ou superior
*   Poetry (recomendado para gerenciamento de dependências)

### Instalação

1.  Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/fotix.git
    cd fotix
    ```
2.  Instale as dependências do projeto:
    ```sh
    # Usando Poetry
    poetry install

    # Ou usando pip com pyproject.toml (requer pip >= 21.1)
    pip install .
    ```

### Execução

Para iniciar a aplicação:

```sh
# Usando Poetry
poetry run python -m fotix

# Ou se instalado globalmente/no venv
python -m fotix
```

## Como Executar os Testes

Para executar a suíte de testes automatizados, utilize o pytest:

```sh
# Usando Poetry
poetry run pytest

# Ou diretamente
pytest
```

## Estrutura do Projeto

O projeto segue uma arquitetura em camadas para garantir a separação de responsabilidades e a manutenibilidade:

*   `src/fotix/domain/`: Lógica de negócio e modelos de dados puros.
*   `src/fotix/application/`: Orquestração de casos de uso e definição de interfaces.
*   `src/fotix/infrastructure/`: Implementação de interações com o mundo exterior (filesystem, hashing, etc.).
*   `src/fotix/ui/`: Componentes da interface gráfica do usuário (PySide6).
*   `tests/`: Testes unitários e de integração.
```

## 9. Arquivo `LICENSE` Proposto

Sugestão: **Licença MIT**. É permissiva, simples e amplamente utilizada.

```text
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

Agradecemos seu interesse em contribuir com o Fotix! Seguir estas diretrizes nos ajuda a manter a qualidade e a consistência do projeto.

## Filosofia de Desenvolvimento (Método AGV)

Este projeto segue uma abordagem de desenvolvimento estruturada, baseada na arquitetura definida no `Blueprint Arquitetural`. Antes de iniciar uma contribuição significativa, por favor, familiarize-se com a arquitetura do projeto.

1.  **Respeite as Camadas:** Todo código novo deve pertencer à camada apropriada:
    *   **`domain`:** Lógica de negócio pura, sem dependências de IO ou frameworks.
    *   **`application`:** Orquestração de casos de uso. Define interfaces, não as implementa.
    *   **`infrastructure`:** Implementação de interfaces para interagir com o sistema de arquivos, rede, etc.
    *   **`ui`:** Código relacionado à interface do usuário (PySide6).

2.  **Use as Interfaces:** Ao adicionar funcionalidades na camada de aplicação, sempre programe voltado para as interfaces (definidas em `application/interfaces.py`), não para as implementações concretas da infraestrutura.

3.  **Adicione Testes:** Toda nova funcionalidade ou correção de bug deve ser acompanhada por testes.
    *   Lógica de domínio deve ter testes unitários extensivos.
    *   Serviços de aplicação podem ser testados com mocks para as dependências de infraestrutura.

4.  **Mantenha os Modelos no Domínio:** Todas as estruturas de dados principais são definidas com Pydantic em `domain/models.py`. Use esses modelos em toda a aplicação para garantir consistência. Não crie DTOs duplicados em outras camadas.

## Submetendo uma Contribuição

1.  Faça um "fork" do repositório.
2.  Crie uma nova "branch" para sua feature (`git checkout -b feature/minha-feature`).
3.  Implemente suas mudanças, seguindo a arquitetura e adicionando testes.
4.  Certifique-se de que todos os testes estão passando (`pytest`).
5.  Faça o "commit" de suas mudanças (`git commit -m 'feat: Adiciona minha feature'`).
6.  Faça o "push" para a sua branch (`git push origin feature/minha-feature`).
7.  Abra um "Pull Request" detalhando as mudanças que você fez.
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

### Deprecated
-

### Removed
-

### Fixed
-

### Security
-

## [0.1.0] - YYYY-MM-DD

### Added
- Initial project structure based on Tocrisna v3.0 blueprint.
- Core domain models, application services, and infrastructure interfaces.
- Basic scaffolding for PySide6 UI.
- Initial set of governance files (README, LICENSE, CONTRIBUTING).
```

## 12. Considerações de Segurança

1.  **Operações de Arquivo Seguras:** A utilização de `send2trash` em vez de `os.remove` ou `shutil.rmtree` é um pilar de segurança, pois permite a recuperação de arquivos deletados acidentalmente através da lixeira do sistema operacional.
2.  **Validação de Input:** O uso de Pydantic para os modelos `ScanConfig` ajuda a validar os caminhos e configurações fornecidas pelo usuário antes de iniciar operações custosas ou de risco no sistema de arquivos.
3.  **Não-Destrutivo por Padrão:** O sistema de backup automático antes da remoção garante que nenhuma informação seja perdida permanentemente por padrão. A restauração é um caso de uso de primeira classe.
4.  **Escopo de Acesso:** A aplicação só acessa os caminhos explicitamente fornecidos pelo usuário, não realizando varreduras em diretórios de sistema ou áreas inesperadas.

## 13. Justificativas e Trade-offs

*   **Decisão:** Adotar uma Arquitetura em Camadas estrita com Inversão de Dependência.
    *   **Justificativa:** Essa abordagem, embora mais verbosa inicialmente (devido à definição de interfaces), paga dividendos imensos em projetos de médio a longo prazo. Ela torna o código extremamente testável (é possível testar a lógica da aplicação com um `FileSystemService` falso em memória), mais fácil de entender (cada componente tem uma responsabilidade clara) e mais fácil de evoluir (a implementação de hashing pode ser trocada sem afetar o resto do sistema).
    *   **Trade-off:** Para um script muito simples, seria um exagero. No entanto, para um "produto de engenharia" completo como o `Fotix`, com GUI, processamento assíncrono e operações críticas de arquivo, o investimento na estrutura é justificado.

*   **Decisão:** Abstrair o `concurrent.futures` em um `ConcurrencyService`.
    *   **Justificativa:** Permite que o modelo de concorrência seja alterado (ex: de `ThreadPoolExecutor` para `ProcessPoolExecutor`, ou até mesmo para uma biblioteca como `asyncio`) sem alterar a lógica do `ScanService` que o utiliza. Também facilita os testes, permitindo a injeção de um `ConcurrencyService` síncrono que executa tarefas em série.

## 14. Exemplo de Bootstrapping/Inicialização (`src/fotix/__main__.py`)

Este trecho conceitual demonstra como os componentes são instanciados e conectados na inicialização da aplicação, seguindo o padrão de Injeção de Dependência.

```python
# src/fotix/__main__.py

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

# Importações das implementações concretas e da UI
from fotix.ui.main_window import MainWindow
from fotix.application.services.scan_service import ScanService
from fotix.infrastructure.filesystem_service import FileSystemService
from fotix.infrastructure.hashing_service import HashingService
from fotix.infrastructure.concurrency_service import ConcurrencyService
from fotix.infrastructure.backup_service import BackupService
from fotix.infrastructure.logging_service import LoggingService # Implementação real

def main():
    """Ponto de entrada principal da aplicação."""
    
    # 1. Configuração Centralizada
    # Em uma app real, isso poderia vir de um arquivo de config ou args de linha de comando
    APP_DATA_PATH = Path.home() / ".fotix"
    BACKUP_ROOT_PATH = APP_DATA_PATH / "backup"
    LOG_FILE_PATH = APP_DATA_PATH / "logs" / "fotix.log"

    # 2. Construção da Camada de Infraestrutura (Injeção de Dependência)
    # Cada serviço é instanciado com suas próprias configurações e dependências.
    
    # Logger é geralmente o primeiro a ser criado
    logger = LoggingService(log_file_path=LOG_FILE_PATH, level="INFO")
    logger.info("Iniciando a aplicação Fotix...")

    # Os outros serviços recebem suas configs e o logger
    filesystem_service = FileSystemService(logger=logger)
    hashing_service = HashingService(logger=logger)
    concurrency_service = ConcurrencyService(logger=logger)
    backup_service = BackupService(backup_root_path=BACKUP_ROOT_PATH, logger=logger)

    # 3. Construção da Camada de Aplicação
    # O ScanService é injetado com as instâncias concretas dos serviços de infraestrutura.
    scan_service = ScanService(
        fs_service=filesystem_service,
        hash_service=hashing_service,
        concurrency_service=concurrency_service,
        backup_service=backup_service,
        logger=logger
    )

    # 4. Construção e Execução da Camada de Apresentação (UI)
    app = QApplication(sys.argv)
    
    # A janela principal recebe o serviço de aplicação para poder interagir com ele.
    window = MainWindow(scan_service=scan_service)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```