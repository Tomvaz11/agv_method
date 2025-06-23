### **Instruções para o Coordenador**

A seguir, a sequência de implementação e os pontos de parada para Testes de Integração (TI). Cada ponto de parada define o escopo, o objetivo e os cenários chave para garantir a qualidade e a correta integração dos componentes desenvolvidos.

### **Módulos Base a Serem Implementados (Interfaces)**

Antes de iniciar a sequência, o `ImplementadorMestre` deve criar o arquivo de interfaces que servirá como contrato para as camadas.

*   `src/fotix/infrastructure/interfaces.py`

---

## Alvo Zero: Setup do Projeto

**Instrução para o `ImplementadorMestre`:** Crie os seguintes arquivos e diretórios para estabelecer a estrutura fundamental do projeto.

1.  Crie o arquivo `pyproject.toml` na raiz do projeto com o seguinte conteúdo:
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

2.  Crie o arquivo `.gitignore` na raiz do projeto com o seguinte conteúdo:
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

3.  Crie os seguintes arquivos `__init__.py` vazios para definir a estrutura de pacotes:
    *   `src/fotix/__init__.py`
    *   `src/fotix/application/__init__.py`
    *   `src/fotix/domain/__init__.py`
    *   `src/fotix/infrastructure/__init__.py`
    *   `src/fotix/ui/__init__.py`
    *   `src/fotix/ui/views/__init__.py`
    *   `tests/__init__.py`
    *   `tests/test_application/__init__.py`
    *   `tests/test_domain/__init__.py`
    *   `tests/test_infrastructure/__init__.py`

---

## Sequência de Implementação e Pontos de Teste

1.  `fotix.domain.models`
2.  `fotix.domain.strategies`

`>>> PARADA PARA TESTES DE INTEGRAÇÃO (DOMÍNIO / CORE) <<<`
-   **Módulos no Grupo:** `fotix.domain.models`, `fotix.domain.strategies`.
-   **Objetivo do Teste:** Validar que os modelos de dados centrais (`FileMeta`, `DuplicateSet`) podem ser instanciados corretamente e que a lógica de negócio encapsulada na estratégia de seleção (`ISelectionStrategy`) opera corretamente sobre esses modelos, sem dependências externas.
-   **Cenários Chave:**
    1.  **Cenário de Instanciação e Validação:** Criar uma instância de `FileMeta` com dados válidos e inválidos para garantir que as validações do Pydantic funcionam. Criar um `DuplicateSet` contendo uma lista de `FileMeta`.
    2.  **Cenário de Lógica da Estratégia:** Instanciar a `DefaultSelectionStrategy`. Criar um `DuplicateSet` com 3 arquivos, onde um é claramente o "melhor" (ex: o mais antigo). Passar a lista de arquivos para o método `choose_file_to_keep` e verificar se o `FileMeta` correto é retornado.

---

3.  `fotix.infrastructure.logging`
4.  `fotix.infrastructure.hashing`
5.  `fotix.infrastructure.concurrency`
6.  `fotix.infrastructure.file_system`
7.  `fotix.infrastructure.zip_handler`
8.  `fotix.infrastructure.backup`

`>>> PARADA PARA TESTES DE INTEGRAÇÃO (INFRAESTRUTURA) <<<`
-   **Módulos no Grupo:** Todos os módulos de `fotix.infrastructure`.
-   **Objetivo do Teste:** Garantir que cada adaptador de infraestrutura interage corretamente com o mundo externo (sistema de arquivos, bibliotecas de terceiros) e que eles se integram entre si e com os modelos de domínio.
-   **Cenários Chave:**
    1.  **Cenário de Descoberta e Hashing:** Usar o `FileSystemService` para encontrar um arquivo de teste real em disco. Verificar se ele cria um objeto `FileMeta` correto. Ler o conteúdo do arquivo e passá-lo para o `HashingService` para calcular o seu hash. Garantir que o resultado é um hash válido e consistente.
    2.  **Cenário de Leitura de ZIP:** Usar o `ZipHandlerService` para ler um arquivo `.zip` de teste que contém imagens. Verificar se o serviço itera sobre os arquivos internos, retornando tuplas de (`FileMeta`, `bytes`) onde `FileMeta.is_in_zip` é `True`.
    3.  **Cenário de Backup e Manifesto:** Usar o `BackupService` para fazer o backup de um arquivo de teste. Verificar se o arquivo foi fisicamente copiado para o diretório de backup e se uma entrada correspondente foi adicionada ao arquivo `manifest.json`.
    4.  **Cenário de Concorrência:** Usar o `ConcurrencyService.map` para aplicar uma função simples (como o `HashingService.calculate_hash`) a uma lista de conteúdos de arquivos em bytes, validando que todos os resultados são calculados e retornados corretamente.

---

9.  `fotix.application.services`

`>>> PARADA PARA TESTES DE INTEGRAÇÃO (LÓGICA DE APLICAÇÃO - HEADLESS) <<<`
-   **Módulos no Grupo:** `fotix.application.services` e todos os módulos das camadas de Domínio e Infraestrutura.
-   **Objetivo do Teste:** Validar o fluxo de negócio de ponta a ponta sem a interface gráfica. O teste deve verificar se o `ScanService` orquestra corretamente os serviços de infraestrutura para executar uma varredura completa, desde a configuração até a identificação de duplicatas.
-   **Cenários Chave:**
    1.  **Cenário de Varredura Completa:** Criar um diretório de teste com subdiretórios e arquivos duplicados. Instanciar o `ScanService` com implementações reais dos serviços de infraestrutura. Invocar o serviço com um `ScanConfig` apontando para o diretório de teste. Verificar se o resultado final é uma lista de `DuplicateSet`s corretamente identificados e com o `file_to_keep` preenchido pela estratégia de domínio.
    2.  **Cenário de Limpeza (Backup e Remoção):** Após uma varredura bem-sucedida, invocar a função de limpeza do `ScanService`. Verificar (inspecionando o sistema de arquivos) se os arquivos duplicados (exceto o `file_to_keep`) foram movidos para o diretório de backup (via `BackupService`) e subsequentemente enviados para a lixeira (via `FileSystemService`).
    3.  **Cenário de Varredura com ZIPs:** Executar uma varredura em um diretório que contém um arquivo ZIP com duplicatas de arquivos externos. Validar que o `ScanService` orquestra o `ZipHandlerService` e que os arquivos de dentro do ZIP são corretamente incluídos nos `DuplicateSet`s.

---

10. `fotix.ui.main_window`
11. `fotix.ui.views.config_view`
12. `fotix.ui.views.progress_view`
13. `fotix.ui.views.results_view`
14. `fotix.ui.views.restore_view`
15. `fotix.ui.worker`
16. `fotix.main` (ponto de entrada/bootstrapping)

`>>> PARADA PARA TESTES DE INTEGRAÇÃO (APLICAÇÃO COMPLETA COM UI) <<<`
-   **Módulos no Grupo:** Todos os módulos de `fotix.ui` e `fotix.main`.
-   **Objetivo do Teste:** Assegurar que a camada de Apresentação (UI) se conecta e interage corretamente com a camada de Aplicação (`ScanService`), que a UI permanece responsiva durante operações longas (usando o `ScanWorker`) e que o ciclo de vida da aplicação (seleção -> progresso -> resultados -> limpeza) funciona como esperado do ponto de vista do usuário.
-   **Cenários Chave:**
    1.  **Cenário de Ciclo de Varredura via UI:** Usando `pytest-qt`, simular a inicialização da aplicação. Simular o usuário selecionando um diretório na `ConfigView` e clicando em "Iniciar Varredura". Verificar se o `ScanWorker` é iniciado, se a `ProgressView` é exibida e se, ao final, a `ResultsView` é populada com dados (mockados ou de uma pequena varredura real).
    2.  **Cenário de Ação na UI e Resposta do Serviço:** Na `ResultsView` preenchida, simular o clique no botão "Remover Duplicatas". Verificar se a chamada correspondente no `ScanService` é executada. Utilizar `mocker` para espionar o método do serviço e confirmar que ele foi chamado com os argumentos corretos.
    3.  **Cenário de Restauração via UI:** Simular a navegação para a `RestoreView`. Verificar se a view chama o `BackupService.list_backups` e exibe a lista. Simular o clique em um item e no botão "Restaurar", e confirmar (usando `mocker`) que o `BackupService.restore_file` foi invocado.