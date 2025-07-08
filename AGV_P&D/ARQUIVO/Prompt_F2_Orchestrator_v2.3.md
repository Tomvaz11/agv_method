# AGV Prompt: OrchestratorHelper v2.3 (Lean com Cenários de TI)

**Tarefa Principal:** Analisar o `@Blueprint_Arquitetural.md`, que é a fonte única da verdade sobre a arquitetura. Suas responsabilidades são: (1) Gerar o "Alvo 0" para setup do projeto, (2) Derivar uma ordem de implementação lógica para os demais módulos, e (3) Gerar cenários chave para os Testes de Integração.

**Input Principal (Blueprint Arquitetural):**

# --- Conteúdo do Blueprint Arquitetural ---
# Proposta de Arquitetura Técnica: Fotix

Este documento detalha a arquitetura técnica de alto nível para o aplicativo `Fotix`, projetado para ser modular, manutenível e escalável, seguindo os princípios da filosofia AGV.

## 1. Visão Geral da Arquitetura

A arquitetura proposta para o `Fotix` é uma **Arquitetura em Camadas (Layered Architecture)**, fortemente inspirada nos princípios da Clean Architecture. Essa abordagem promove uma clara separação de responsabilidades, desacoplando a lógica de negócios das implementações de UI e infraestrutura.

As camadas são:

1.  **Apresentação (UI - `fotix.ui`):** Responsável pela interação com o usuário. Contém todos os componentes da interface gráfica (PySide6). Ela não possui lógica de negócio, apenas exibe dados e captura as intenções do usuário, delegando as ações para a Camada de Aplicação.
2.  **Aplicação (`fotix.app`):** Orquestra os casos de uso do sistema. Atua como um intermediário entre a UI e o Core, combinando as regras de negócio do Core com os serviços de infraestrutura para executar tarefas completas (ex: "iniciar uma varredura completa"). Utiliza o **Padrão Observer** para notificar a UI sobre o progresso de operações longas de forma assíncrona.
3.  **Core / Domínio (`fotix.core`):** O coração da aplicação. Contém as entidades de negócio (modelos de dados), as regras de negócio puras (ex: como decidir qual duplicata manter) e as interfaces que o domínio espera que o mundo exterior implemente. Esta camada não depende de nenhuma outra.
4.  **Infraestrutura (`fotix.infrastructure`):** Contém as implementações concretas das interfaces definidas pelo Core e pela Aplicação. Lida com todas as interações com o mundo exterior: sistema de arquivos, hashing, descompactação de ZIPs, logging, etc.

**Justificativa:** Esta arquitetura garante:
-   **Alta Testabilidade:** A lógica do Core e da Aplicação pode ser testada de forma isolada, injetando implementações "mock" dos serviços de infraestrutura.
-   **Manutenibilidade:** A troca de uma biblioteca (ex: um novo algoritmo de hashing) afeta apenas um componente na camada de infraestrutura, sem impactar o resto do sistema.
-   **Clareza:** As dependências fluem em uma única direção (de fora para dentro), tornando o fluxo de dados e controle fácil de entender.

## 2. Diagrama de Componentes (Simplificado)

```mermaid
graph TD
    subgraph Apresentação (UI)
        UI_MainWindow("MainWindow (PySide6)")
        UI_Views("Telas/Componentes UI")
    end

    subgraph Aplicação
        App_Orchestrator("ScanOrchestratorService")
        App_Backup("BackupRestoreService")
    end

    subgraph Core / Domínio
        Core_Models("Models (Pydantic)")
        Core_Finder("DuplicateFinder")
        Core_Strategy("SelectionStrategy")
    end

    subgraph Infraestrutura
        Infra_FS("FileSystemService")
        Infra_Zip("ZipReaderService")
        Infra_Hash("HashingService")
        Infra_Concurrency("ConcurrencyService")
        Infra_Backup("BackupPersistenceService")
        Infra_Log("LoggingService")
    end

    UI_MainWindow --> App_Orchestrator
    UI_Views --> App_Orchestrator
    UI_Views --> App_Backup

    App_Orchestrator --> Core_Finder
    App_Orchestrator --> Core_Strategy
    App_Orchestrator --> Infra_FS
    App_Orchestrator --> Infra_Zip
    App_Orchestrator --> Infra_Hash
    App_Orchestrator --> Infra_Concurrency
    App_Orchestrator --> Infra_Backup

    App_Backup --> Infra_Backup

    Infra_Backup --> Infra_FS

    style Core_Models fill:#f9f,stroke:#333,stroke-width:2px
    style Core_Finder fill:#f9f,stroke:#333,stroke-width:2px
    style Core_Strategy fill:#f9f,stroke:#333,stroke-width:2px
```

## 3. Descrição dos Componentes, Interfaces e Modelos

### 3.1. Camada de Domínio/Core (`fotix.core`) - SSOT dos Modelos de Dados

Esta seção é a **Fonte Única da Verdade (SSOT)** para todos os modelos de dados do projeto. Todas as outras camadas devem usar e referenciar estes modelos.

*   **Módulo:** `fotix.core.models`
*   **Responsabilidade Principal:** Definir todas as estruturas de dados canônicas do domínio, garantindo validação e consistência.
*   **Tecnologias Chave:** Pydantic `BaseModel`.
*   **Definições dos Modelos:**
    ```python
    # fotix/core/models.py
    from datetime import datetime
    from pathlib import Path
    from typing import Optional, List
    from pydantic import BaseModel, Field

    class FileInfo(BaseModel):
        """Representa os metadados essenciais de um único arquivo."""
        path: Path
        size: int
        creation_date: datetime
        hash: Optional[str] = None
        is_in_zip: bool = False
        zip_path: Optional[Path] = None

    class DuplicateGroup(BaseModel):
        """Agrupa um conjunto de arquivos idênticos (duplicatas)."""
        files: List[FileInfo]
        hash: str
        file_to_keep: Optional[FileInfo] = None
        files_to_remove: List[FileInfo] = Field(default_factory=list)

    class ScanConfig(BaseModel):
        """Configurações para uma operação de varredura."""
        source_paths: List[Path]
        include_zips: bool = True

    class ScanProgress(BaseModel):
        """Representa o estado do progresso da varredura."""
        phase: str # Ex: "Indexing files", "Hashing", "Analyzing"
        processed_files: int
        total_files: int
        current_file: Optional[Path] = None

    class ScanResult(BaseModel):
        """Agrega os resultados de uma varredura completa."""
        duplicate_groups: List[DuplicateGroup]
        total_files_scanned: int
        total_space_saved_bytes: int = 0
        total_duplicates_found: int = 0

    class BackupManifestEntry(BaseModel):
        """Entrada no manifesto de backup."""
        original_path: Path
        backup_path: Path
        backup_timestamp: datetime
        hash: str

    class AppConfig(BaseModel):
        """Configuração geral da aplicação."""
        backup_root_path: Path
        log_level: str = "INFO"
        max_workers: int = 4
    ```

---

### 3.2. Decomposição dos Componentes por Camada

#### **Camada de Core / Domínio (`fotix.core`)** (continuação)

*   **Componente:** `fotix.core.duplicate_finder.DuplicateFinder`
    *   **Responsabilidade Principal:** Receber uma lista de `FileInfo`, agrupar arquivos por tamanho e, em seguida, por hash para encontrar grupos de duplicatas.
    *   **Tecnologias Chave:** Python (Lógica Pura).
    *   **Dependências Diretas:** `fotix.core.models`.

*   **Componente:** `fotix.core.selection_strategy.SelectionStrategy`
    *   **Responsabilidade Principal:** Implementar o **Padrão Strategy**. Receber um `DuplicateGroup` e aplicar um conjunto de regras (resolução, data, nome) para determinar qual `FileInfo` deve ser mantido.
    *   **Tecnologias Chave:** Python (Lógica Pura).
    *   **Dependências Diretas:** `fotix.core.models`.

#### **Camada de Aplicação (`fotix.app`)**

*   **Componente:** `fotix.app.scan_orchestrator.ScanOrchestratorService`
    *   **Responsabilidade Principal:** Orquestrar o fluxo completo de varredura: chamar o `FileSystemService` para listar arquivos, o `ConcurrencyService` para paralelizar o hashing, o `DuplicateFinder` para agrupar, o `SelectionStrategy` para escolher o melhor arquivo, e notificar a UI sobre o progresso (Observer Pattern).
    *   **Tecnologias Chave:** Python (Lógica Pura).
    *   **Dependências Diretas:** `fotix.core.models`, `fotix.core.duplicate_finder`, `fotix.core.selection_strategy`, `fotix.infrastructure.interfaces`.

*   **Componente:** `fotix.app.backup_restore.BackupRestoreService`
    *   **Responsabilidade Principal:** Orquestrar as operações de backup e restauração, interagindo com o serviço de persistência de backup. Mapeia a intenção do usuário (ex: "restaurar este arquivo") para chamadas concretas na infraestrutura.
    *   **Tecnologias Chave:** Python (Lógica Pura).
    *   **Dependências Diretas:** `fotix.core.models`, `fotix.infrastructure.interfaces`.

#### **Camada de Apresentação (UI - `fotix.ui`)**

*   **Responsabilidade Principal:** Renderizar a interface gráfica, exibir dados recebidos dos serviços de aplicação e encaminhar eventos do usuário.
*   **Tecnologias Chave:** PySide6.
*   **Dependências Diretas:** `fotix.app.scan_orchestrator`, `fotix.app.backup_restore`, `fotix.core.models`.
*   **Decomposição em Telas/Componentes:**
    *   `MainWindow`: A janela principal que hospeda as outras views e a barra de menus/ferramentas.
    *   `ScanSetupView`: Um painel/widget onde o usuário seleciona diretórios, define opções (ex: incluir ZIPs) e inicia a varredura. Interage com `ScanOrchestratorService`.
    *   `ProgressView`: Um componente (pode ser um diálogo modal ou um painel) que exibe o progresso de uma operação longa, recebendo atualizações (`ScanProgress`) do `ScanOrchestratorService`.
    *   `ResultsView`: Uma view complexa (provavelmente usando `QTreeView` ou `QTableView`) para exibir os `DuplicateGroup` encontrados. Permite ao usuário revisar as seleções automáticas e aprovar a remoção. Interage com `ScanOrchestratorService`.
    *   `BackupRestoreView`: Uma tela para listar os backups existentes (via `BackupRestoreService`) e permitir que o usuário selecione itens para restauração.

#### **Camada de Infraestrutura (`fotix.infrastructure`)**

*   **Componente:** `fotix.infrastructure.file_system.WindowsFileSystemService`
    *   **Responsabilidade Principal:** Implementar a interface `IFileSystemService`. Realizar operações concretas no sistema de arquivos, como escanear diretórios, obter metadados, mover e deletar arquivos de forma segura. Mapeia dados brutos do sistema de arquivos para o modelo `FileInfo`.
    *   **Tecnologias Chave:** `pathlib`, `shutil`, `send2trash`.
    *   **Dependências Diretas:** `fotix.core.models`.

*   **Componente:** `fotix.infrastructure.zip_reader.StreamZipReaderService`
    *   **Responsabilidade Principal:** Implementar a interface `IZipReaderService`. Usar `stream-unzip` para ler o conteúdo de arquivos ZIP de forma eficiente em termos de memória, extraindo arquivos como streams de bytes. Mapeia metadados do ZIP para o modelo `FileInfo`.
    *   **Tecnologias Chave:** `stream-unzip`.
    *   **Dependências Diretas:** `fotix.core.models`.

*   **Componente:** `fotix.infrastructure.hashing.Blake3HashingService`
    *   **Responsabilidade Principal:** Implementar a interface `IHashingService`. Calcular o hash BLAKE3 de um stream de bytes de um arquivo.
    *   **Tecnologias Chave:** `blake3`.
    *   **Dependências Diretas:** Nenhuma do projeto.

*   **Componente:** `fotix.infrastructure.concurrency.ThreadPoolConcurrencyService`
    *   **Responsabilidade Principal:** Implementar a interface `IConcurrencyService`. Gerenciar um pool de threads para executar tarefas (como hashing) em paralelo, abstraindo o uso direto de `concurrent.futures`.
    *   **Tecnologias Chave:** `concurrent.futures`.
    *   **Dependências Diretas:** Nenhuma do projeto.

*   **Componente:** `fotix.infrastructure.backup_persistence.JsonBackupPersistenceService`
    *   **Responsabilidade Principal:** Implementar a interface `IBackupPersistenceService`. Gerenciar o backup de arquivos (movendo-os para o diretório de backup) e a persistência do manifesto de backup em um arquivo JSON.
    *   **Tecnologias Chave:** `json`, `pathlib`.
    *   **Dependências Diretas:** `fotix.core.models`.

*   **Componente:** `fotix.infrastructure.logging.LoggingService`
    *   **Responsabilidade Principal:** Configurar e fornecer uma instância de logger padronizada para toda a aplicação, com base nas configurações.
    *   **Tecnologias Chave:** `logging` (stdlib).
    *   **Dependências Diretas:** Nenhuma do projeto.

## 4. Definição das Interfaces Principais

Aqui definimos os contratos de comunicação entre as camadas. As implementações na infraestrutura herdarão dessas classes base abstratas.

```python
# fotix/infrastructure/interfaces.py
from abc import ABC, abstractmethod
from typing import Iterator, List, Tuple, IO
from fotix.core.models import FileInfo, ScanConfig, BackupManifestEntry, BackupManifest

class IFileSystemService(ABC):
    @abstractmethod
    def find_files(self, config: ScanConfig) -> Iterator[FileInfo]:
        """Varre os caminhos de origem e retorna um iterador de FileInfo."""
        pass

    @abstractmethod
    def move_file(self, source: Path, destination: Path) -> None:
        """Move um arquivo."""
        pass

    @abstractmethod
    def delete_file_safely(self, path: Path) -> None:
        """Move um arquivo para a lixeira do sistema."""
        pass

class IZipReaderService(ABC):
    @abstractmethod
    def stream_zip_chunks(self, zip_path: Path) -> Iterator[Tuple[str, int, IO[bytes]]]:
        """Retorna um iterador de (nome_do_arquivo, tamanho, stream_de_bytes) para cada arquivo no ZIP."""
        pass

class IHashingService(ABC):
    @abstractmethod
    def calculate_hash(self, stream: IO[bytes]) -> str:
        """Calcula o hash de um stream de dados."""
        pass

class IConcurrencyService(ABC):
    @abstractmethod
    def run_in_parallel(self, func, tasks: list) -> Iterator:
        """Executa uma função em paralelo para uma lista de tarefas."""
        pass

class IBackupPersistenceService(ABC):
    @abstractmethod
    def __init__(self, backup_root_path: Path):
        """O serviço é configurado com o caminho raiz do backup."""
        self.backup_root_path = backup_root_path

    @abstractmethod
    def backup_file(self, file: FileInfo) -> BackupManifestEntry:
        """Copia um arquivo para o diretório de backup e retorna a entrada do manifesto."""
        pass

    @abstractmethod
    def restore_file(self, entry: BackupManifestEntry) -> None:
        """Restaura um arquivo do backup para sua localização original."""
        pass
        
    @abstractmethod
    def load_manifest(self) -> BackupManifest:
        """Carrega o manifesto de backup."""
        pass

    @abstractmethod
    def save_manifest(self, manifest: BackupManifest) -> None:
        """Salva o manifesto de backup."""
        pass
```

## 5. Gerenciamento de Dados

A persistência de dados no `Fotix` é limitada a dois artefatos principais, ambos gerenciados pela camada de **Infraestrutura**:

1.  **Backup de Arquivos:** Os arquivos marcados para remoção são movidos para um diretório de backup seguro, definido pelo usuário. Essa operação é gerenciada pelo `JsonBackupPersistenceService`.
2.  **Manifesto de Backup:** Um arquivo `manifest.json` será mantido na raiz do diretório de backup. Ele conterá uma lista de objetos `BackupManifestEntry`, registrando o caminho original, o novo caminho no backup, o timestamp e o hash de cada arquivo salvo. Isso permite a funcionalidade de restauração.
3.  **Configurações da Aplicação:** Um arquivo simples (ex: `config.json` ou `settings.ini`) será armazenado em um local apropriado para dados do aplicativo (ex: `%APPDATA%/Fotix`) para persistir configurações como o caminho do diretório de backup, nível de log, etc.

## 6. Estrutura de Diretórios Proposta (`src` layout)

```
fotix/
├── .gitignore
├── .venv/
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── pyproject.toml  # Ou requirements.txt
├── src/
│   └── fotix/
│       ├── __init__.py
│       ├── main.py        # Ponto de entrada, bootstrapping
│       ├── app/
│       │   ├── __init__.py
│       │   ├── backup_restore.py
│       │   └── scan_orchestrator.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── duplicate_finder.py
│       │   └── selection_strategy.py
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   ├── interfaces.py
│       │   ├── backup_persistence.py
│       │   ├── concurrency.py
│       │   ├── file_system.py
│       │   ├── hashing.py
│       │   ├── logging.py
│       │   └── zip_reader.py
│       └── ui/
│           ├── __init__.py
│           ├── main_window.py
│           ├── views/
│           │   ├── __init__.py
│           │   ├── results_view.py
│           │   └── ...
│           └── assets/
│               └── icon.png
└── tests/
    ├── __init__.py
    ├── test_app/
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

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE-specific
.idea/
.vscode/
*.suo
*.ntvs*
*.njsproj
*.sln
*.swp

# OS-specific
.DS_Store
Thumbs.db

# Fotix specific
/config.json
/fotix_log.log
/backup_storage/
```

## 8. Arquivo `README.md` Proposto

````markdown
# Fotix

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-em_desenvolvimento-orange.svg)

Um aplicativo desktop inteligente para encontrar e remover arquivos de mídia duplicados com segurança.

## Sobre o Projeto

Fotix é uma ferramenta poderosa desenvolvida em Python e PySide6 para ajudar usuários a liberar espaço em disco, localizando e removendo arquivos de imagem e vídeo que são **idênticamente duplicados**. Ele varre múltiplos diretórios e até mesmo arquivos ZIP, usando um algoritmo de decisão para escolher a melhor cópia para manter com base em critérios como resolução, data e nome do arquivo.

Principais funcionalidades:
-   🔎 **Detecção Precisa:** Utiliza hashing BLAKE3 para garantir que apenas arquivos 100% idênticos sejam marcados.
-   🧠 **Seleção Inteligente:** Decide automaticamente qual arquivo manter, evitando cópias de baixa qualidade ou com nomes genéricos.
-   📦 **Suporte a ZIP:** Capaz de analisar o conteúdo de arquivos `.zip` sem a necessidade de descompactá-los completamente.
-   🛡️ **Backup e Restauração:** Todos os arquivos removidos são enviados para um backup seguro, permitindo a restauração com um clique.
-   ⚡ **Otimizado para Performance:** Projetado com processamento paralelo e assíncrono para lidar com grandes volumes de arquivos sem travar a interface.

## Stack Tecnológica

*   **Linguagem:** Python 3.10+
*   **Interface Gráfica (GUI):** PySide6 (Qt for Python)
*   **Motor de Hashing:** BLAKE3
*   **Manipulação de Arquivos:** pathlib, shutil, send2trash
*   **Paralelismo:** concurrent.futures
*   **Leitura de ZIPs:** stream-unzip

## Como Começar

Siga estas instruções para obter uma cópia do projeto em sua máquina local para desenvolvimento e testes.

### Pré-requisitos

*   Python 3.10 ou superior
*   Git

### Instalação

1.  Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/fotix.git
    cd fotix
    ```

2.  Crie e ative um ambiente virtual:
    ```sh
    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  Instale as dependências:
    ```sh
    pip install -r requirements.txt
    # ou, se estiver usando pyproject.toml com Poetry/PDM
    # poetry install
    ```

4.  Execute a aplicação:
    ```sh
    python src/fotix/main.py
    ```

## Como Executar os Testes

Para executar os testes automatizados do projeto:

```sh
pytest
```

## Estrutura do Projeto

O projeto segue uma arquitetura em camadas para garantir a separação de responsabilidades e a manutenibilidade:

-   `src/fotix/`: Contém todo o código fonte da aplicação.
    -   `ui/`: Camada de Apresentação (componentes PySide6).
    -   `app/`: Camada de Aplicação (orquestração dos casos de uso).
    -   `core/`: Camada de Domínio (lógica de negócio e modelos de dados).
    -   `infrastructure/`: Camada de Infraestrutura (interação com sistema de arquivos, hashing, etc.).
-   `tests/`: Contém os testes unitários e de integração.
````

## 9. Arquivo `LICENSE` Proposto

A licença MIT é uma excelente escolha padrão, pois é permissiva e amplamente utilizada.

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

Agradecemos seu interesse em contribuir com o Fotix! Seguir estas diretrizes ajuda a comunicar que você respeita o tempo dos desenvolvedores que gerenciam e desenvolvem este projeto.

## Código de Conduta

Este projeto e todos que participam dele são regidos pelo nosso [Código de Conduta](CODE_OF_CONDUCT.md). Ao participar, você deverá manter este código.

## Fluxo de Trabalho de Contribuição

1.  **Crie um Fork:** Faça um fork do repositório para sua própria conta do GitHub.
2.  **Clone seu Fork:** Clone o repositório para sua máquina local.
3.  **Crie uma Branch:** Crie uma nova branch para suas alterações (`git checkout -b feature/minha-feature-incrivel`).
4.  **Codifique:** Faça suas alterações no código.
    -   **Siga a Arquitetura:** Respeite a arquitetura em camadas definida no blueprint. A lógica de negócio deve residir no `core`, a orquestração na `app`, a interação com o sistema de arquivos na `infrastructure`, e a UI na `ui`.
    -   **Adicione Testes:** Se você adicionar uma nova funcionalidade, por favor, adicione testes unitários correspondentes no diretório `tests/`.
    -   **Mantenha o Estilo:** Siga o estilo de código existente (PEP 8). Considere usar um formatador como `black` e um linter como `flake8`.
5.  **Faça o Commit:** Faça o commit de suas alterações com mensagens claras e descritivas.
6.  **Envie para o GitHub:** Envie suas alterações para o seu fork (`git push origin feature/minha-feature-incrivel`).
7.  **Abra um Pull Request:** Abra um Pull Request do seu fork para a branch `main` do repositório original. Certifique-se de descrever claramente suas alterações e por que elas são necessárias.

## Relatando Bugs

-   Use a seção de **Issues** do GitHub para relatar bugs.
-   Seja o mais detalhado possível: descreva os passos para reproduzir o bug, o comportamento esperado e o que realmente aconteceu. Inclua a versão do sistema operacional e do Python.

Obrigado por sua contribuição!
```

## 11. Estrutura do `CHANGELOG.md`

```markdown
# Changelog

Todos as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Adicionado
-   ...

### Modificado
-   ...

### Removido
-   ...

## [0.1.0] - YYYY-MM-DD

### Adicionado
-   Estrutura inicial do projeto e definição da arquitetura.
-   Funcionalidade básica de varredura de diretórios.
-   Esqueleto da interface gráfica com PySide6.
```

## 12. Considerações de Segurança

-   **Validação de Input:** Todos os caminhos fornecidos pelo usuário na UI serão validados para garantir que são caminhos de diretório ou arquivo válidos antes de serem processados.
-   **Remoção Segura:** A utilização da biblioteca `send2trash` em vez de `os.remove` ou `shutil.rmtree` é um pilar de segurança, pois move os arquivos para a lixeira do sistema operacional, permitindo uma recuperação fácil pelo usuário fora da aplicação, como uma última camada de proteção.
-   **Path Traversal:** Embora seja uma aplicação desktop local, as operações com caminhos devem ser tratadas com cuidado, usando `pathlib` para construir caminhos de forma segura e evitar a concatenação manual de strings que poderiam levar a vulnerabilidades de travessia de diretório.
-   **Manifesto de Backup:** O hash do arquivo será salvo no manifesto de backup. Durante uma restauração, pode-se opcionalmente verificar se o hash do arquivo no backup corresponde ao registrado, garantindo a integridade.

## 13. Justificativas e Trade-offs

-   **Arquitetura em Camadas:** Escolhida pela sua robustez em separar responsabilidades, o que aumenta a testabilidade e manutenibilidade. O custo é uma maior quantidade de "boilerplate" (interfaces, injeção de dependência), mas os benefícios em um projeto de médio porte como este superam o custo inicial.
-   **Abstração da Infraestrutura:** Abstrair `pathlib`, `concurrent.futures`, etc., por trás de interfaces pode parecer excessivo para uma aplicação simples. No entanto, isso é crucial para testes unitários e permite, por exemplo, trocar o executor de concorrência (de threads para processos) ou o sistema de arquivos (para um sistema de arquivos em memória para testes) com impacto mínimo.
-   **Padrão Observer para UI:** Em vez de acoplar a UI diretamente a chamadas de bloqueio, o `ScanOrchestratorService` emitirá sinais (eventos) de progresso. A UI se inscreve nesses sinais. Isso mantém a GUI 100% responsiva, mesmo durante varreduras pesadas, o que é um requisito não funcional chave.
-   **Pydantic para Modelos:** Utilizar Pydantic adiciona uma dependência, mas oferece validação de tipos em tempo de execução, serialização/desserialização para JSON gratuita e uma forma clara de definir as estruturas de dados, o que reduz bugs e melhora a clareza do código.

## 14. Exemplo de Bootstrapping/Inicialização (`src/fotix/main.py`)

Este trecho conceitual demonstra como os componentes seriam instanciados e conectados na inicialização, ilustrando a Injeção de Dependência.

```python
# src/fotix/main.py (Simplificado)
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

# Importações das implementações concretas e dos serviços de aplicação
from fotix.ui.main_window import MainWindow
from fotix.app.scan_orchestrator import ScanOrchestratorService
from fotix.app.backup_restore import BackupRestoreService
from fotix.infrastructure.file_system import WindowsFileSystemService
from fotix.infrastructure.zip_reader import StreamZipReaderService
from fotix.infrastructure.hashing import Blake3HashingService
from fotix.infrastructure.concurrency import ThreadPoolConcurrencyService
from fotix.infrastructure.backup_persistence import JsonBackupPersistenceService
from fotix.core.duplicate_finder import DuplicateFinder
from fotix.core.selection_strategy import DefaultSelectionStrategy
from fotix.core.models import AppConfig

def main():
    """Ponto de entrada da aplicação Fotix."""
    
    # 1. Carregar Configurações
    # Em uma implementação real, isso viria de um arquivo config.json
    app_config = AppConfig(
        backup_root_path=Path.home() / "FotixBackups",
        log_level="INFO",
        max_workers=8
    )
    
    # 2. Construir Dependências (Camada de Infraestrutura)
    # Os componentes são instanciados com suas configurações via __init__
    fs_service = WindowsFileSystemService()
    zip_service = StreamZipReaderService()
    hashing_service = Blake3HashingService()
    concurrency_service = ThreadPoolConcurrencyService(max_workers=app_config.max_workers)
    backup_persistence_service = JsonBackupPersistenceService(
        backup_root_path=app_config.backup_root_path
    )
    
    # 3. Construir Componentes do Core
    duplicate_finder = DuplicateFinder()
    selection_strategy = DefaultSelectionStrategy()
    
    # 4. Construir Serviços da Camada de Aplicação (Injetando as dependências)
    scan_orchestrator = ScanOrchestratorService(
        file_system_service=fs_service,
        zip_reader_service=zip_service,
        hashing_service=hashing_service,
        concurrency_service=concurrency_service,
        duplicate_finder=duplicate_finder,
        selection_strategy=selection_strategy
    )
    
    backup_restore_service = BackupRestoreService(
        backup_persistence_service=backup_persistence_service,
        file_system_service=fs_service
    )
    
    # 5. Construir e Executar a UI (Injetando os serviços da aplicação)
    app = QApplication(sys.argv)
    
    # A MainWindow recebe os serviços que ela precisa para funcionar
    main_window = MainWindow(
        scan_orchestrator=scan_orchestrator,
        backup_restore_service=backup_restore_service
    )
    
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

**Diretrizes Essenciais:**

1.  **Análise do Grafo de Dependências:** Analise as dependências diretas entre os "Módulos Principais" no Blueprint para definir a sequência.

2.  **Criação do "Alvo 0 - Setup do Projeto Profissional":** Sua primeira tarefa é SEMPRE gerar um item inicial na ordem de implementação chamado **"Alvo 0: Setup do Projeto Profissional"**. A responsabilidade deste alvo é criar o andaime ("scaffolding") completo, incluindo:
    *   A estrutura de diretórios base (`src/nome_do_projeto`, `tests/unit`, `tests/integration`).
    *   Os arquivos `__init__.py` necessários.
    *   O arquivo `pyproject.toml` configurando dependências, `pytest`, e as ferramentas de qualidade **`ruff`** (linter) e **`black`** (formatador).
    *   O arquivo de configuração do `pre-commit` (`.pre-commit-config.yaml`) para automatizar a execução de `ruff` e `black`.
    *   Instruções claras para o Coordenador sobre como instalar as dependências (`pip install -e .[dev]`) e inicializar o `pre-commit` (`pre-commit install`).

3.  **Geração da Ordem Sequencial:** Após o "Alvo 0", crie uma lista numerada contendo **apenas os nomes completos dos "Módulos Principais"**. A sequência deve respeitar as dependências.

4.  **Identificação de Pontos de Teste de Integração (TI):**
    *   Identifique grupos de módulos recém-listados que completam um "subsistema coerente" ou um "fluxo funcional significativo".
    *   Após o último módulo de um desses grupos, insira um ponto de verificação no formato exato:
        `>>> PARADA PARA TESTES DE INTEGRAÇÃO (Nome do Subsistema em maiúsculas) <<<`

5.  **Geração de Cenários de Teste de Integração:**
    *   Para cada `>>> PARADA ... <<<` criada, você **DEVE** gerar uma seção detalhada logo abaixo dela.
    *   Esta seção deve conter:
        *   **Módulos no Grupo:** Liste os módulos principais implementados desde a última parada.
        *   **Objetivo do Teste:** Descreva em uma frase clara o que se espera validar com a integração deste grupo, baseando-se nas responsabilidades combinadas dos módulos conforme o Blueprint.
        *   **Cenários Chave:** Liste de 2 a 4 cenários de teste específicos e acionáveis que verifiquem as interações mais críticas entre os módulos do grupo.

6.  **Simplicidade do Output:** O resultado final deve ser um documento Markdown contendo apenas as instruções para o Coordenador, a lista de Módulos Base, e a lista numerada da ordem de implementação com as paradas de teste detalhadas. **Não inclua descrições de módulos ou justificativas de ordem.** Essa informação reside exclusivamente no Blueprint.

**Resultado Esperado:**

Um documento Markdown (`Output_Ordem_e_Testes.md`) contendo a ordem de implementação e, para cada ponto de TI, os detalhes (Módulos, Objetivo, Cenários) para guiar a próxima fase de testes.