### **Instruções para o Coordenador**

Este documento define a ordem de construção e os pontos de verificação para os testes de integração do projeto `Fotix`. Siga a sequência estritamente.

O primeiro passo é estabelecer a fundação do projeto conforme descrito no "Alvo 0". Após a conclusão, prossiga com a implementação dos módulos na ordem especificada.

---

### **Módulos Base a Serem Implementados**

*   `fotix.core.models`
*   `fotix.core.duplicate_finder`
*   `fotix.core.selection_strategy`
*   `fotix.infrastructure.interfaces`
*   `fotix.infrastructure.hashing`
*   `fotix.infrastructure.concurrency`
*   `fotix.infrastructure.file_system`
*   `fotix.infrastructure.zip_reader`
*   `fotix.app.scan_orchestrator`
*   `fotix.infrastructure.backup_persistence`
*   `fotix.app.backup_restore`
*   `fotix.ui` (representa todos os componentes da UI)
*   `fotix.main`

---

### **Ordem de Implementação e Pontos de Teste**

1.  **Alvo 0: Setup do Projeto Profissional**
    *   **Ação:** Criar a estrutura completa de diretórios e arquivos de configuração.
    *   **Estrutura de Diretórios:**
        ```
        fotix/
        ├── .git/
        ├── .venv/
        ├── .pre-commit-config.yaml
        ├── pyproject.toml
        ├── src/
        │   └── fotix/
        │       ├── __init__.py
        │       ├── main.py
        │       ├── app/
        │       │   └── __init__.py
        │       ├── core/
        │       │   └── __init__.py
        │       ├── infrastructure/
        │       │   └── __init__.py
        │       └── ui/
        │           └── __init__.py
        └── tests/
            ├── __init__.py
            ├── integration/
            │   └── __init__.py
            └── unit/
                └── __init__.py
        ```
    *   **Arquivo `.pre-commit-config.yaml`:**
        ```yaml
        repos:
        -   repo: https://github.com/pre-commit/pre-commit-hooks
            rev: v4.5.0
            hooks:
            -   id: trailing-whitespace
            -   id: end-of-file-fixer
            -   id: check-yaml
            -   id: check-added-large-files
        -   repo: https://github.com/psf/black
            rev: 24.4.2
            hooks:
            -   id: black
        -   repo: https://github.com/astral-sh/ruff-pre-commit
            rev: v0.4.3
            hooks:
            -   id: ruff
                args: [--fix]
            -   id: ruff-format
        ```
    *   **Arquivo `pyproject.toml`:**
        ```toml
        [build-system]
        requires = ["setuptools>=61.0"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "fotix"
        version = "0.1.0"
        authors = [
          { name="Seu Nome", email="seu@email.com" },
        ]
        description = "Ferramenta para encontrar e remover arquivos de mídia duplicados."
        readme = "README.md"
        requires-python = ">=3.10"
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]
        dependencies = [
            "pydantic>=2.0",
            "pyside6",
            "blake3",
            "stream-unzip",
            "send2trash",
        ]

        [project.urls]
        "Homepage" = "https://github.com/seu-usuario/fotix"

        [project.optional-dependencies]
        dev = [
            "pytest",
            "pytest-cov",
            "ruff",
            "black",
            "pre-commit",
        ]

        [tool.setuptools]
        packages = ["fotix"]
        package-dir = {"" = "src"}

        [tool.pytest.ini_options]
        minversion = "6.0"
        addopts = "-ra -q --cov=src/fotix --cov-report=html"
        testpaths = [
            "tests/unit",
            "tests/integration",
        ]
        ```
    *   **Instruções para o Coordenador:**
        1.  Execute `pip install -e .[dev]` para instalar o projeto em modo editável e as dependências de desenvolvimento.
        2.  Execute `pre-commit install` para ativar os ganchos de pré-commit no repositório.

---

2.  `fotix.core.models`
3.  `fotix.core.duplicate_finder`
4.  `fotix.core.selection_strategy`
5.  `fotix.infrastructure.interfaces`
6.  `fotix.infrastructure.hashing`
7.  `fotix.infrastructure.concurrency`
8.  `fotix.infrastructure.file_system`
9.  `fotix.infrastructure.zip_reader`

    `>>> PARADA PARA TESTES DE INTEGRAÇÃO (SUBSISTEMA DE ANÁLISE DE ARQUIVOS) <<<`

    *   **Módulos no Grupo:** `fotix.core.*`, `fotix.infrastructure.interfaces`, `fotix.infrastructure.hashing`, `fotix.infrastructure.concurrency`, `fotix.infrastructure.file_system`, `fotix.infrastructure.zip_reader`.
    *   **Objetivo do Teste:** Validar que os serviços de infraestrutura podem ser usados em conjunto pela lógica do `core` para, a partir de um conjunto de caminhos, identificar e agrupar arquivos duplicados, tanto no sistema de arquivos quanto dentro de arquivos ZIP.
    *   **Cenários Chave:**
        1.  **Cenário Padrão:** Criar uma estrutura de diretórios com 3 arquivos idênticos e 2 únicos. Utilizar o `FileSystemService` para listá-los, o `HashingService` (via `ConcurrencyService`) para calcular os hashes e o `DuplicateFinder` para confirmar que um único `DuplicateGroup` com 3 arquivos foi encontrado.
        2.  **Cenário com ZIP:** Criar um arquivo ZIP contendo uma cópia de um arquivo que também existe fora do ZIP. Utilizar o `ZipReaderService` e o `FileSystemService` para obter a lista de todos os `FileInfo`, e confirmar que o `DuplicateFinder` agrupa corretamente o arquivo externo e o interno.
        3.  **Cenário de Seleção:** Passar um `DuplicateGroup` para o `SelectionStrategy` e verificar se o arquivo correto é selecionado para ser mantido com base nas regras (ex: manter o arquivo com o caminho mais curto ou data mais recente).

---

10. `fotix.app.scan_orchestrator`

    `>>> PARADA PARA TESTES DE INTEGRAÇÃO (FLUXO DE VARREDURA COMPLETA - HEADLESS) <<<`

    *   **Módulos no Grupo:** `fotix.app.scan_orchestrator` (utilizando todos os módulos anteriores).
    *   **Objetivo do Teste:** Garantir que o `ScanOrchestratorService` coordena com sucesso todos os serviços subjacentes para executar um fluxo de varredura completo, desde a configuração inicial até a geração do resultado final, sem a UI.
    *   **Cenários Chave:**
        1.  **Orquestração Completa:** Instanciar o `ScanOrchestratorService` com implementações reais (ou mocks controlados) dos serviços de infraestrutura. Chamar o método principal de varredura com um `ScanConfig` apontando para uma pasta de teste. Validar se o `ScanResult` retornado contém os `DuplicateGroup` esperados e os totais corretos.
        2.  **Filtro de ZIP:** Executar uma varredura em um diretório que contém arquivos ZIP com duplicatas. Primeiro com `include_zips=True` e verificar se as duplicatas do ZIP são encontradas. Depois, com `include_zips=False` e verificar se são ignoradas.
        3.  **Observador de Progresso (Mock):** Criar um "observador" mock que se inscreve no `ScanOrchestratorService`. Iniciar uma varredura e verificar se o mock recebe múltiplas atualizações do tipo `ScanProgress`, validando as diferentes fases ("Indexing", "Hashing", "Analyzing").

---

11. `fotix.infrastructure.backup_persistence`
12. `fotix.app.backup_restore`

    `>>> PARADA PARA TESTES DE INTEGRAÇÃO (FLUXO DE BACKUP E RESTAURAÇÃO) <<<`

    *   **Módulos no Grupo:** `fotix.infrastructure.backup_persistence`, `fotix.app.backup_restore`.
    *   **Objetivo do Teste:** Validar o ciclo de vida completo de segurança de arquivos: fazer o backup de um arquivo, gerenciar o manifesto e restaurá-lo para sua localização original.
    *   **Cenários Chave:**
        1.  **Backup de Arquivo:** Utilizar o `BackupRestoreService` para fazer o backup de um `FileInfo`. Verificar se o arquivo físico foi movido para o diretório de backup configurado e se um `manifest.json` foi criado/atualizado com a `BackupManifestEntry` correta.
        2.  **Restauração de Arquivo:** Carregar um manifesto existente. Chamar o serviço para restaurar uma `BackupManifestEntry` específica. Verificar se o arquivo foi movido de volta para seu caminho original e se o manifesto foi devidamente atualizado (ex: a entrada foi removida).
        3.  **Falha na Restauração:** Tentar restaurar um arquivo para um local original que agora está ocupado por outro arquivo. O serviço deve lidar com isso de forma segura (ex: lançar uma exceção ou renomear o arquivo a ser restaurado) e não sobrescrever dados.

---

13. `fotix.ui`
14. `fotix.main`

    `>>> PARADA PARA TESTES DE INTEGRAÇÃO (TESTE DE SISTEMA END-TO-END COM UI) <<<`

    *   **Módulos no Grupo:** `fotix.ui`, `fotix.main`.
    *   **Objetivo do Teste:** Validar que a interface gráfica se integra corretamente com os serviços da camada de aplicação para executar as principais jornadas do usuário de ponta a ponta. (Estes testes podem ser manuais ou automatizados com frameworks de teste de UI).
    *   **Cenários Chave:**
        1.  **Jornada de Varredura e Limpeza:**
            a. O usuário abre o app, seleciona um diretório na `ScanSetupView`.
            b. O usuário clica em "Varrer"; a `ProgressView` aparece e exibe o progresso real.
            c. A varredura termina e a `ResultsView` é populada com os grupos de duplicatas.
            d. O usuário inspeciona os resultados, concorda com a seleção automática e clica em "Remover Duplicatas".
            e. Verificar (no sistema de arquivos) se os arquivos foram movidos para a pasta de backup.
        2.  **Jornada de Restauração:**
            a. O usuário navega para a `BackupRestoreView`.
            b. A lista de arquivos no backup é exibida corretamente.
            c. O usuário seleciona um arquivo e clica em "Restaurar".
            d. Verificar (no sistema de arquivos) se o arquivo retornou à sua localização original.
        3.  **Interatividade e Responsividade:** Durante uma varredura longa em um diretório com muitos arquivos, confirmar que a janela principal da aplicação permanece responsiva e pode ser movida ou minimizada.