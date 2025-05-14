# AGV Prompt Template: PreenchedorGenerico v1.1 - Preenchimento Assistido de Prompt AGV

**Tarefa Principal:** Preencher de forma **cirúrgica e precisa** todos os campos/placeholders necessários no template de prompt AGV fornecido (`Prompt_Tocle_Implementation_v1.1.md`), utilizando **exclusivamente** as informações contidas nos documentos fonte listados (`Output_Severino_DecisionLogic2.md` e `Output_Tocrisna_Architecture_v1.0.md`).

**Instruções Detalhadas:**

1.  **Análise das Fontes:** Estude cuidadosamente o conteúdo de todos os `Output_Severino_DecisionLogic2.md` e `Output_Tocrisna_Architecture_v1.0.md` para extrair as informações relevantes.
2.  **Análise do Template Alvo:** Identifique todos os placeholders (ex: `[PLACEHOLDER]`) e seções que precisam ser preenchidas no `Prompt_Tocle_Implementation_v1.1.md`.
3.  **Preenchimento Preciso:** Substitua cada placeholder no template alvo pela informação correspondente encontrada **exatamente** nos documentos fonte.
    *   **NÃO invente informações.** Se uma informação específica para um placeholder não for encontrada nas fontes, deixe o placeholder como está ou indique explicitamente `[INFORMAÇÃO NÃO ENCONTRADA NAS FONTES]`.
    *   **Use apenas as fontes fornecidas.** Não consulte fontes externas ou conhecimento prévio.
4.  **Formatação:** Mantenha a estrutura e formatação Markdown original do template alvo.

**Arquivos de Referência:**

1.  **Template Alvo (a ser preenchido):**
    ```markdown
    # --- Conteúdo de [Prompt_Tocle_Implementation_v1.1.md] ---
    # AGV Prompt Template: Tocle v1.1 - Implementação de Código Novo

**Tarefa Principal:** Implementar a funcionalidade/módulo descrito na seção "Especificação" abaixo, criando ou modificando o arquivo Python `[NOME_DO_ARQUIVO_A_SER_CRIADO_OU_MODIFICADO.py]`. Siga rigorosamente as diretrizes e o contexto arquitetural fornecido.

**Contexto Arquitetural (Definido por Tocrisna / Severino):**

*   **Nome do Projeto:** `[NOME_DO_PROJETO]`
*   **Objetivo Geral do Projeto:** `[BREVE DESCRIÇÃO DO PROPÓSITO GERAL DO PROJETO]`
*   **Localização deste Módulo/Arquivo:** `[CAMINHO/PASTA/ONDE/ESTE/ARQUIVO/DEVE_FICAR.py]`
*   **Principais Responsabilidades deste Módulo/Arquivo:** `[DESCRIÇÃO CONCISA DO QUE ESTE ARQUIVO DEVE FAZER, CONFORME ARQUITETURA]`
*   **Dependências Diretas deste Módulo:**
    *   `[COPIAR A LISTA EXPLÍCITA DE DEPENDÊNCIAS DIRETAS DO OUTPUT DO SEVERINO/BLUEPRINT. Ex:]`
    *   `fotix.domain.models`
    *   `utils.helpers`
*   **Interfaces de Dependências (Contratos a serem Usados):**
    *   `[FORNECER AQUI AS ASSINATURAS E DESCRIÇÕES DAS FUNÇÕES/MÉTODOS/CLASSES DE *OUTROS MÓDULOS* QUE ESTE CÓDIGO PRECISA CHAMAR. SEJA PRECISO. Ex:]`
    *   `utils.helpers.calcular_hash(file_path: Path) -> str`
*   **Interfaces Expostas (Contratos a serem Fornecidos - se aplicável):**
    *   `[SE ESTE MÓDULO EXPÕE FUNÇÕES/CLASSES PARA OUTROS USarem, LISTAR SUAS ASSINATURAS ESPERADAS AQUI. Ex:]`
    *   `Classe 'DecisionEngine' com método público 'decide_file_to_keep(group: DuplicateGroup) -> FileMetadata'`
*   **Padrões de Design Chave (Relevantes para esta Implementação):** `[PADRÕES RELEVANTES DA ARQUITETURA]`
*   **Estrutura de Dados Principal (Relevantes para esta Implementação):** `[DEFINIÇÃO DE DATACLASSES/NAMEDTUPLES RELEVANTES QUE ESTE MÓDULO USARÁ OU RETORNARÁ]`

**Especificação da Funcionalidade/Módulo a ser Implementada (Gerada por Severino):**

[COLE AQUI O OUTPUT COMPLETO DA ESPECIFICAÇÃO TÉCNICA DETALHADA GERADA PELO SEVERINO NA FASE 2.5]

**Stack Tecnológica Permitida (Definida na Fase 1):**

*   **Linguagem:** Python `[VERSÃO - Ex: 3.10+]`
*   **Frameworks Principais:** `[LISTAR - Ex: PySide6]`
*   **Bibliotecas Essenciais:** `[LISTAR - Ex: BLAKE3, send2trash, stream-unzip]` (Permitir importação apenas destas, das bibliotecas padrão Python e dos outros módulos do projeto listados nas 'Dependências Diretas', a menos que instruído a adicionar nova dependência).

**Diretrizes Específicas de Implementação:**

1.  **Aderência Estrita às Interfaces e Especificação:** Implementar a funcionalidade conforme descrito na Especificação, utilizando e expondo *exatamente* as interfaces definidas no Contexto Arquitetural.
2.  **Código Limpo e Legível (PEP 8):** Seguir rigorosamente o PEP 8. Priorizar clareza e simplicidade (KISS).
3.  **Modularidade e Coesão (SRP):** Criar funções e classes com responsabilidades únicas e bem definidas.
4.  **Type Hints (PEP 484):** Utilizar type hints completos e precisos.
5.  **Tratamento de Erros Robusto:** Antecipar e tratar erros potenciais conforme especificado. Usar exceções específicas.
6.  **Segurança Básica:** Validar inputs, evitar práticas inseguras.
7.  **Documentação (Docstrings PEP 257):** Escrever docstrings claras e completas, referenciando contratos de interface.
8.  **Sem Código Morto/Desnecessário:** Implementar apenas o necessário.
9.  **Testes Unitários:** **OBRIGATÓRIO:** Gerar testes unitários (usando `[NOME_DO_FRAMEWORK_DE_TESTE - Ex: pytest, unittest]`) para as funções/métodos públicos. Os testes devem:
    *   Cobrir casos de sucesso, erro e borda mencionados na Especificação.
    *   **Utilizar mocks/stubs para simular as "Interfaces de Dependências"** (não chamar o código real de outros módulos).
    *   Verificar se os "Outputs Esperados" estão corretos.
    *   Colocar os testes em `tests/unit/[caminho_correspondente]/test_[nome_do_modulo].py`.
10. **Eficiência (Consideração):** Escrever código razoavelmente eficiente, sem otimização prematura.
11. **Contexto Essencial:** **NOVO/IMPORTANTE:** Para implementar esta funcionalidade corretamente, você **precisará conhecer as definições exatas** dos arquivos/módulos listados na seção **"Dependências Diretas"** acima. Ao executar (ex: no Cursor/Augment), certifique-se de fornecer o conteúdo desses arquivos como contexto (ex: usando `@path/to/dependency.py`).

**Resultado Esperado:**

1.  **Código Python Completo:** O conteúdo final do arquivo `[NOME_DO_ARQUIVO_A_SER_CRIADO_OU_MODIFICADO.py]`.
2.  **Código de Testes Unitários:** O conteúdo do arquivo de teste correspondente com testes unitários usando mocks.
3.  **(Opcional) Breve Relatório:** Explicação de decisões, desafios ou sugestões.
    ```

2.  **Documentos Fonte (para consulta):**
    ```markdown
    # --- Conteúdo de [Output_Severino_DecisionLogic2.md] ---
    **Especificação da Funcionalidade/Módulo a ser Implementada:**

**1. Módulo Alvo:**
   `fotix/src/fotix/core/decision_logic.py`

**2. Função Alvo:**
   `decide_file_to_keep(group: DuplicateGroup) -> FileMetadata`

**3. Descrição Geral:**
   Implementar a lógica de decisão para selecionar um único arquivo `FileMetadata` a ser mantido dentro de um `DuplicateGroup`, que contém uma lista de arquivos duplicados (`FileMetadata`). A seleção deve seguir uma hierarquia de critérios: maior resolução, data de modificação mais recente e nome de arquivo mais curto. A função deve operar de forma pura, sem efeitos colaterais (como I/O ou modificação do estado global) e basear-se apenas nos dados fornecidos no `DuplicateGroup`.

**4. Inputs:**
   - `group`: Uma instância da classe `DuplicateGroup` (definida em `fotix.domain.models`). Espera-se que `group.files` contenha uma lista de objetos `FileMetadata` representando os arquivos duplicados. Cada `FileMetadata` *deve* idealmente conter os metadados necessários para a decisão (resolução, data de modificação), além dos campos base (`path`, `size`, `creation_time`).

**5. Output:**
   - Retorna: Um único objeto `FileMetadata`, correspondente ao arquivo selecionado para ser mantido, escolhido a partir da lista `group.files`.

**6. Lógica Detalhada e Regras de Negócio:**

   A função `decide_file_to_keep` deve executar os seguintes passos:

   a.  **Validação Inicial:**
       i.  Verificar se `group.files` não é `None` e contém pelo menos dois elementos. Se tiver menos de dois arquivos, a decisão não se aplica a um grupo de duplicatas. Lançar `ValueError` (Ver Seção 8 - Tratamento de Erros).
       ii. Se houver exatamente um arquivo, retornar esse arquivo (embora conceitualmente não seja um grupo de duplicatas, este pode ser um caso de borda a ser tratado). *Nota: O ponto i. tem precedência; se for estritamente para duplicatas, deve haver >= 2.* (Conforme diretriz 8, considerar o tratamento para < 2 como erro).

   b.  **Preparação dos Dados:**
       i.  Iterar sobre a lista `group.files`. Para cada `FileMetadata`, extrair os metadados relevantes para a decisão:
           -   **Resolução:** Assumir que `FileMetadata` terá um atributo ou método para fornecer a resolução como `(largura, altura)` ou `None` se não disponível/aplicável. Calcular a área (`largura * altura`).
           -   **Data de Modificação:** Assumir que `FileMetadata` terá um atributo ou método para fornecer a data/hora da última modificação (timestamp UTC ou objeto `datetime` comparável).
           -   **Nome do Arquivo:** Obter o nome base do arquivo a partir do `path` (`file.path.name`). Calcular o comprimento do nome.

   c.  **Aplicação dos Critérios (Hierárquico):**
   
       i.  **Critério 1: Maior Resolução:**
           -   Comparar todos os arquivos em `group.files` com base na área de resolução calculada.
           -   Arquivos sem dados de resolução (`None`) devem ser considerados como tendo a menor resolução possível (prioridade mais baixa neste critério).
           -   Selecionar o(s) arquivo(s) com a maior área de resolução.
           -   Se apenas um arquivo tiver a maior resolução, retorná-lo como o arquivo a ser mantido.
           -   Se houver empate (múltiplos arquivos com a mesma resolução máxima), passar esses arquivos empatados para o próximo critério.

       ii. **Critério 2: Data de Modificação Mais Recente (Aplicado aos Empatados da Resolução):**
           -   Comparar os arquivos empatados no critério anterior com base na sua data de modificação.
           -   Arquivos sem data de modificação (`None`) devem ser considerados como tendo a data mais antiga possível (prioridade mais baixa neste critério).
           -   Selecionar o(s) arquivo(s) com a data de modificação mais recente (maior timestamp).
           -   Se apenas um arquivo tiver a data mais recente, retorná-lo.
           -   Se houver empate (múltiplos arquivos com a mesma data de modificação mais recente), passar esses arquivos empatados para o próximo critério.

       iii. **Critério 3: Nome de Arquivo Mais Curto (Aplicado aos Empatados da Data):**
           -   Comparar os arquivos empatados no critério anterior com base no comprimento do nome do arquivo (`len(file.path.name)`).
           -   Selecionar o(s) arquivo(s) com o menor comprimento de nome.
           -   Se apenas um arquivo tiver o nome mais curto, retorná-lo.
           -   Se ainda houver empate (múltiplos arquivos com o mesmo menor comprimento de nome), selecionar arbitrariamente o *primeiro* arquivo encontrado entre os empatados finais (garantindo determinismo, por exemplo, baseado na ordem original da lista `group.files` filtrada). Retornar este arquivo.

**7. Dependências e Estruturas de Dados:**
   - A implementação deve usar as definições de `FileMetadata` e `DuplicateGroup` do módulo `fotix.domain.models`.
   - A implementação *não* deve chamar diretamente nenhuma função de I/O ou serviços externos. Deve operar exclusivamente sobre os dados passados via `group`.

**8. Tratamento de Erros:**
   - Se `group` for `None` ou `group.files` for `None`, lançar `ValueError` com uma mensagem apropriada (ex: "DuplicateGroup inválido ou lista de arquivos vazia.").
   - Se `group.files` contiver menos de 2 arquivos, lançar `ValueError` com uma mensagem apropriada (ex: "Não é possível decidir entre menos de dois arquivos.").
   - **Metadados Ausentes:** A lógica de decisão (passo 6.c) deve tratar explicitamente casos onde metadados (resolução, data de modificação) estão ausentes (`None`) para um ou mais arquivos, tratando-os como a menor prioridade dentro do respectivo critério, em vez de lançar um erro. Se *todos* os arquivos em um estágio de desempate não tiverem o metadado relevante, o processo continua para o próximo critério com todos esses arquivos.

**9. Casos de Borda:**
   - **Grupo com 2 arquivos:** A lógica deve funcionar corretamente.
   - **Todos os metadados idênticos:** Se todos os arquivos tiverem a mesma resolução (ou nenhuma), mesma data de modificação (ou nenhuma) e mesmo comprimento de nome, o critério 6.c.iii (último passo do desempate) garantirá que um arquivo seja escolhido (o primeiro entre os empatados finais).
   - **Arquivos sem resolução:** Serão corretamente priorizados abaixo dos que possuem resolução.
   - **Arquivos sem data de modificação:** Serão corretamente priorizados abaixo dos que possuem data de modificação.

**10. Premissas:**
    - Assume-se que a estrutura `FileMetadata` (definida em `fotix.domain.models`) conterá ou fornecerá acesso aos metadados necessários: resolução (como `(largura, altura)` ou similar) e data de modificação (como timestamp ou `datetime`). Se estes não estiverem presentes na definição atual, a implementação desta função assume que eles *serão* adicionados/acessíveis no objeto `FileMetadata` recebido.
    - Assume-se que a ordem dos arquivos dentro do `group.files` original pode ser usada como um critério final de desempate determinístico, se necessário.

**11. Exemplo (Ilustrativo):**

    ```
    # Exemplo de como a função seria chamada (não parte da implementação)
    # file1 = FileMetadata(path=Path("a.jpg"), size=100, creation_time=..., resolution=(1920, 1080), modification_time=1678886400.0, name_len=5)
    # file2 = FileMetadata(path=Path("b_copy.jpg"), size=100, creation_time=..., resolution=(1920, 1080), modification_time=1678886500.0, name_len=10)
    # file3 = FileMetadata(path=Path("c.jpg"), size=100, creation_time=..., resolution=(800, 600), modification_time=1678886600.0, name_len=5)
    # group = DuplicateGroup(files=[file1, file2, file3], hash_value="some_hash")
    #
    # chosen_file = decide_file_to_keep(group)
    # # Esperado: file2 (maior resolução empata file1 e file2, file2 é mais recente que file1)
    ```

    # --- Conteúdo de [Output_Tocrisna_Architecture_v1.0.md] ---
    # Proposta de Arquitetura Técnica: Fotix v1.0

**Documento Preparado Por:** Tocrisna (Agente Arquiteta de Software)
**Versão:** 1.0
**Data:** 2024-08-28

## 1. Visão Geral da Arquitetura

A arquitetura proposta para o `Fotix` é uma **Arquitetura em Camadas (Layered Architecture)** com forte separação de responsabilidades. Esta abordagem foi escolhida por sua clareza, manutenibilidade e testabilidade, adequadas para uma aplicação desktop com funcionalidades bem definidas.

As camadas principais são:

1.  **Camada de Apresentação (GUI):** Responsável pela interface com o usuário.
2.  **Camada de Aplicação (Serviços):** Orquestra os casos de uso, atuando como fachada para o núcleo.
3.  **Camada de Núcleo (Core/Domain):** Contém a lógica de negócio principal (identificação de duplicatas, regras de decisão).
4.  **Camada de Infraestrutura:** Lida com preocupações transversais como acesso ao sistema de arquivos, paralelismo, logging e persistência de backups.

**Justificativa:**
*   **Modularidade:** Separa claramente a interface do usuário, a lógica de negócio e o acesso a recursos externos (sistema de arquivos, etc.).
*   **Manutenibilidade:** Alterações na GUI não devem impactar o Core, e vice-versa. Novas fontes de arquivos (ex: outros formatos compactados no futuro) podem ser adicionadas na Infraestrutura sem afetar o Core.
*   **Testabilidade:** Cada camada pode ser testada isoladamente. O Core, sendo independente de UI e I/O direto, é altamente testável unitariamente. A Camada de Aplicação pode ser testada com mocks da Infraestrutura e do Core.
*   **Clareza:** Facilita o entendimento do fluxo de dados e responsabilidades.
*   **GUI Responsiva:** Permite que as operações intensivas (Core e Infraestrutura) rodem em threads/processos separados, mantendo a GUI (Apresentação) responsiva.

## 2. Diagrama de Componentes (Simplificado - Descrição Textual)

```
+-----------------------+      +--------------------------+      +---------------------+      +------------------------+
|   Apresentação (GUI)  |<---->|  Aplicação (Serviços)    |<---->|   Núcleo (Core)     |<---->| Infraestrutura         |
|-----------------------|      |--------------------------|      |---------------------|      |------------------------|
| - PySide6 (Views)     |      | - Orquestração Casos Uso |      | - Lógica Duplicatas |      | - FileSystemService    |
| - ViewModels (Qt)     |      | - Gerencia Estado Scan   |      | - Algoritmo Decisão |      | - ZipHandlingService   |
| - Interação Usuário   |      | - Fachada p/ GUI         |      | - Hashing (BLAKE3)  |      | - ConcurrencyManager   |
| - Signals/Slots       |----->| - Comunicação Async GUI <------| - Estruturas Dados  |      | - BackupRestoreService |
+-----------------------+      +--------------------------+      +---------------------+      | - LoggingService       |
                                                                                            | - (pathlib, shutil,    |
                                                                                            |  send2trash,           |
                                                                                            |  stream-unzip,         |
                                                                                            |  concurrent.futures)   |
                                                                                            +------------------------+
        ^                                                                                            ^
        |                                                                                            |
        +----------------------------------------- Utilidades (`utils`) -----------------------------+
                                             (Funções Comuns, Constantes, etc.)
```

**Fluxo Principal (Exemplo: Scan):**
GUI -> Aplicação (inicia scan) -> Infraestrutura (lista arquivos) -> Core (pré-filtra, hash) -> Infraestrutura (lê arquivos p/ hash) -> Core (compara hashes, agrupa) -> Aplicação (recebe resultados) -> GUI (exibe resultados)

## 3. Descrição dos Componentes/Módulos

1.  **`fotix.gui` (Apresentação)**
    *   **Responsabilidade:** Renderizar a interface gráfica, capturar entradas do usuário (seleção de diretórios, configurações), exibir o progresso e os resultados do escaneamento, permitir ações sobre os resultados (exclusão, restauração).
    *   **Tecnologias:** PySide6 (Qt for Python).
    *   **Interação:** Comunica-se *exclusivamente* com a camada `fotix.application` através de chamadas de método e recebe atualizações via Signals/Slots do Qt (ou um mecanismo similar de callback/fila) para manter a responsividade.

2.  **`fotix.application` (Aplicação/Serviços)**
    *   **Responsabilidade:** Orquestrar os fluxos de trabalho (casos de uso). Atua como uma fachada entre a GUI e o Core/Infraestrutura. Gerencia o estado geral da aplicação (ex: scan em andamento, resultados carregados). Inicia tarefas em background (usando `ConcurrencyManager` da Infraestrutura) e coordena a comunicação assíncrona de volta para a GUI (progresso, resultados, erros).
    *   **Tecnologias:** Python puro, `dataclasses`/`pydantic`.
    *   **Interação:** Chamado pela `gui`. Chama métodos do `core` para lógica de negócio e da `infrastructure` para operações de I/O, paralelismo e outras preocupações externas.

3.  **`fotix.core` (Núcleo/Domain)**
    *   **Responsabilidade:** Implementar a lógica central de identificação de duplicatas. Contém o algoritmo de hashing (usando BLAKE3), a lógica de comparação, a estratégia de pré-filtragem por tamanho, e o algoritmo de decisão para escolher qual arquivo manter. Define as estruturas de dados canônicas para representar arquivos, duplicatas e resultados. **Deve ser independente de UI e I/O direto.**
    *   **Tecnologias:** Python puro, BLAKE3 (via biblioteca), `dataclasses`/`pydantic`.
    *   **Interação:** Chamado pela `application`. Pode solicitar dados de arquivos (ex: stream de bytes para hashing) através de interfaces implementadas pela `infrastructure`, mas não acessa o sistema de arquivos diretamente.

4.  **`fotix.infrastructure` (Infraestrutura)**
    *   **Responsabilidade:** Lidar com todas as interações com o mundo exterior e preocupações transversais. Isso inclui:
        *   Acesso ao sistema de arquivos (listar diretórios, obter metadados, ler, mover, deletar arquivos).
        *   Manipulação de arquivos ZIP (leitura e extração otimizada).
        *   Gerenciamento de concorrência/paralelismo (pools de threads/processos).
        *   Operações de backup e restauração.
        *   Logging.
        *   (Opcional) Persistência de configuração.
    *   **Tecnologias:** `pathlib`, `shutil`, `os.path`, `send2trash`, `stream-unzip`, `concurrent.futures`, `logging`, Python puro.
    *   **Interação:** Chamado pela `application` para executar tarefas de I/O ou gerenciar concorrência. Implementa interfaces que podem ser usadas pelo `core` (ex: para obter dados de arquivos de forma abstrata).

5.  **`fotix.utils` (Utilidades)**
    *   **Responsabilidade:** Fornecer funções auxiliares, constantes, e talvez classes base ou decoradores usados por múltiplos módulos/camadas. Ex: formatação de tamanho de arquivo, setup inicial de logging.
    *   **Tecnologias:** Python puro.
    *   **Interação:** Usado por qualquer outra camada conforme necessário.

## 4. Definição das Interfaces Principais (Contratos entre Camadas)

Usaremos `dataclasses` ou `pydantic` para definir estruturas de dados claras.

**Estruturas de Dados Chave:**

```python
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Iterator

@dataclass(frozen=True)
class FileMetadata:
    path: Path
    size: int
    creation_time: float # Timestamp UTC
    # Potencialmente outros metadados úteis para decisão (resolução, etc. - a serem extraídos seletivamente)
    # hash: Optional[str] = None # Preenchido durante o processamento

@dataclass
class ScanConfig:
    directories_to_scan: List[Path]
    include_zip_files: bool
    # Outras configurações (ex: filtros de extensão, tamanho mínimo/máximo)

@dataclass
class DuplicateGroup:
    files: List[FileMetadata] # Lista de arquivos idênticos
    file_to_keep: Optional[FileMetadata] = None # Decidido pelo Core
    hash_value: str # Hash que identifica o grupo

@dataclass
class ScanProgress:
    files_scanned: int
    duplicates_found: int
    current_phase: str # Ex: "Listing files", "Hashing", "Comparing"
    error_message: Optional[str] = None

@dataclass
class BackupInfo:
    original_path: Path
    backup_path: Path
    timestamp: float
```

**Interfaces (Assinaturas de Métodos Chave):**

*   **`fotix.application.ScanService` (Interface exposta para a `gui`)**
    *   `start_scan(config: ScanConfig) -> None`: Inicia um novo processo de scan em background. Dispara sinais/callbacks para progresso.
    *   `get_current_results() -> List[DuplicateGroup]`: Retorna os grupos de duplicatas encontrados até o momento (ou ao final).
    *   `process_deletions(groups: List[DuplicateGroup]) -> None`: Inicia o processo de backup e remoção dos arquivos marcados para exclusão (não os `file_to_keep`). Dispara sinais/callbacks para progresso/conclusão.
    *   `restore_from_backup(backup_info: BackupInfo) -> None`: Inicia a restauração de um arquivo.
    *   `get_backup_list() -> List[BackupInfo]`: Retorna a lista de backups disponíveis.
    *   *Sinais/Callbacks para GUI (Conceitual):* `progress_updated(progress: ScanProgress)`, `scan_completed(results: List[DuplicateGroup])`, `deletion_completed()`, `error_occurred(message: str)`

*   **`fotix.core.DuplicateFinder` (Interface usada pela `application`)**
    *   `find_duplicates(file_iterator: Iterator[FileMetadata], hash_function: callable) -> List[DuplicateGroup]`: Recebe um iterador de metadados de arquivos e uma função para obter o hash (fornecida via `infrastructure`), retorna os grupos de duplicatas. O processo interno envolve:
        1. Pré-filtragem por tamanho.
        2. Agrupamento por tamanho.
        3. Hashing (usando `hash_function`) apenas para grupos com mais de um arquivo.
        4. Comparação final por hash.
    *   `decide_file_to_keep(group: DuplicateGroup) -> FileMetadata`: Aplica as regras de negócio (resolução, data, nome) para selecionar o melhor arquivo dentro de um grupo de duplicatas.

*   **`fotix.infrastructure.FileSystemService` (Interface usada pela `application` e potencialmente pelo `core` via `application`)**
    *   `scan_directory_recursively(path: Path, include_zip: bool) -> Iterator[FileMetadata]`: Itera sobre arquivos em diretórios, retornando `FileMetadata` básico (sem hash). Delega a extração de ZIPs ao `ZipHandlingService`.
    *   `get_file_stream(path: Path) -> Iterator[bytes]`: Retorna um iterador/stream de bytes para um arquivo (usado para hashing pelo `core`).
    *   `move_file_to_trash(path: Path) -> None`: Move um arquivo para a lixeira do sistema de forma segura (usando `send2trash`).
    *   `get_file_metadata(path: Path) -> FileMetadata`: Obtém metadados detalhados de um arquivo (pode incluir extração de metadados de mídia se necessário para a decisão do `core`).

*   **`fotix.infrastructure.ZipHandlingService` (Interface usada pelo `FileSystemService`)**
    *   `stream_files_from_zip(zip_path: Path) -> Iterator[Tuple[str, Iterator[bytes], int]]`: Usa `stream-unzip` para iterar sobre os arquivos dentro de um ZIP, retornando o nome do arquivo interno, um iterador para seus bytes e seu tamanho, sem extrair tudo para o disco.

*   **`fotix.infrastructure.ConcurrencyManager` (Interface usada pela `application`)**
    *   `submit_cpu_bound_task(func: callable, *args, **kwargs) -> Future`: Submete uma tarefa intensiva em CPU (ex: hashing de múltiplos arquivos) para execução em um pool de processos (`ProcessPoolExecutor`).
    *   `submit_io_bound_task(func: callable, *args, **kwargs) -> Future`: Submete uma tarefa intensiva em I/O (ex: listar muitos arquivos, ler muitos arquivos pequenos) para execução em um pool de threads (`ThreadPoolExecutor`).

*   **`fotix.infrastructure.BackupRestoreService` (Interface usada pela `application`)**
    *   `backup_file(source_path: Path) -> BackupInfo`: Move o arquivo para um local de backup seguro e retorna informações sobre o backup.
    *   `restore_file(backup_info: BackupInfo) -> None`: Restaura um arquivo do backup para seu local original.
    *   `list_backups() -> List[BackupInfo]`: Lista os backups existentes.
    *   `purge_old_backups(days_threshold: int) -> None`: (Opcional) Remove backups antigos.

## 5. Gerenciamento de Dados

*   **Dados de Scan:** Mantidos em memória durante o processamento pela `application` e `core`, usando as `dataclasses` definidas. Os resultados finais são passados para a `gui`. Não há persistência dos resultados do scan entre sessões do aplicativo na v1.0.
*   **Backups:** Gerenciados pela `BackupRestoreService` na camada de `infrastructure`. Os arquivos removidos são movidos para um diretório de backup dedicado (configurável, ex: `AppData/Local/Fotix/Backup` ou similar), possivelmente com metadados adicionais (um pequeno arquivo de índice ou nomeando os backups de forma informativa).
*   **Logs:** Gerenciados pela `LoggingService` na `infrastructure`. Logs detalhados são escritos em arquivos (`AppData/Local/Fotix/Logs`), e relatórios resumidos podem ser gerados ao final do processo.
*   **Configuração:** Configurações simples (últimos diretórios usados, etc.) podem ser salvas em um arquivo de configuração (ex: INI, JSON) gerenciado pela `infrastructure`.

## 6. Estrutura de Diretórios Proposta

```
fotix/
├── src/
│   └── fotix/
│       ├── __init__.py
│       ├── main.py           # Ponto de entrada da aplicação
│       ├── gui/              # Camada de Apresentação (PySide6 Widgets, Views, ViewModels)
│       │   ├── __init__.py
│       │   ├── main_window.py
│       │   └── widgets/
│       ├── application/      # Camada de Aplicação (Serviços/Orquestração)
│       │   ├── __init__.py
│       │   └── scan_service.py
│       ├── core/             # Camada de Núcleo (Lógica de Negócio)
│       │   ├── __init__.py
│       │   ├── duplicate_finder.py
│       │   └── decision_logic.py
│       ├── infrastructure/   # Camada de Infraestrutura
│       │   ├── __init__.py
│       │   ├── file_system.py
│       │   ├── zip_handler.py
│       │   ├── concurrency.py
│       │   ├── backup.py
│       │   └── logging_setup.py
│       ├── domain/           # Estruturas de dados compartilhadas (Dataclasses/Pydantic) - Alternativa a colocá-las em 'core'
│       │   ├── __init__.py
│       │   └── models.py
│       └── utils/            # Utilidades
│           ├── __init__.py
│           └── helpers.py
├── tests/                  # Testes unitários e de integração
│   ├── __init__.py
│   ├── gui/
│   ├── application/
│   ├── core/
│   └── infrastructure/
├── data/                   # (Opcional) Dados de exemplo, recursos
├── docs/                   # Documentação
├── scripts/                # Scripts auxiliares (build, etc.)
├── requirements.txt        # Dependências
└── README.md
```

## 7. Considerações de Segurança

*   **Validação de Input:** A camada `gui` e `application` devem validar as entradas do usuário (ex: caminhos de diretório existem e são acessíveis).
*   **Operações de Arquivo Seguras:** Usar `send2trash` para exclusão minimiza o risco de perda acidental de dados. O sistema de backup é a principal salvaguarda.
*   **Tratamento de Erros:** Capturar exceções específicas de I/O (`FileNotFoundError`, `PermissionError`) na camada de `infrastructure` e reportá-las adequadamente para a `application` e `gui` para informar o usuário. Evitar falhas silenciosas em operações críticas (backup, delete).
*   **Permissões:** A aplicação rodará com as permissões do usuário logado. Garantir que o acesso a arquivos e diretórios respeite as permissões do sistema operacional.
*   **Hashing Seguro:** BLAKE3 é um algoritmo de hash criptográfico moderno e rápido, adequado para identificação de arquivos idênticos e resistente a colisões acidentais.
*   **Dados Sensíveis:** O aplicativo lida com caminhos de arquivo do usuário. Não há dados sensíveis adicionais (senhas, etc.) previstos. Logs devem evitar informações excessivamente detalhadas que possam ser sensíveis, se aplicável.

## 8. Justificativas e Trade-offs

*   **Arquitetura em Camadas vs. Outras:** Escolhida pela simplicidade e clareza para uma aplicação desktop. Microsserviços seriam excessivos. Uma arquitetura puramente baseada em eventos poderia adicionar complexidade na comunicação entre componentes para este escopo.
*   **`concurrent.futures`:** Oferece uma abstração de alto nível para paralelismo (threads para I/O, processos para CPU-bound como hashing BLAKE3), simplificando o gerenciamento em comparação com `threading` ou `multiprocessing` puros.
*   **`stream-unzip`:** Essencial para o requisito de lidar com grandes ZIPs com baixo uso de memória, processando arquivos um a um em vez de extrair tudo de uma vez.
*   **PySide6 (Qt):** Framework robusto e maduro para GUIs desktop, com bom suporte a multithreading (via `QThread` e signals/slots) que se integra bem com a necessidade de tarefas em background.
*   **BLAKE3:** Oferece excelente desempenho para hashing, crucial para a velocidade de identificação de duplicatas em grandes volumes.
*   **Separação `core` vs. `infrastructure`:** Garante que a lógica de negócio principal seja pura e testável, isolada dos detalhes de implementação de I/O, que podem mudar (ex: suportar outros formatos compactados no futuro).
*   **Interfaces Explícitas:** A definição clara das interfaces e estruturas de dados é crucial para o baixo acoplamento e facilita a evolução e os testes (mocking).
*   **Trade-off:** A comunicação assíncrona entre a camada de Aplicação/Infraestrutura (background threads/processes) e a GUI adiciona alguma complexidade (gerenciamento de signals/slots ou filas), mas é necessária para a responsividade da UI.

---

Esta proposta fornece um blueprint sólido para o desenvolvimento do `Fotix`, priorizando os requisitos funcionais e não funcionais definidos, com foco em uma estrutura manutenível e robusta.
    ```

**Resultado Esperado:**

1.  **Prompt Preenchido Completo:** O conteúdo completo do `Prompt_Tocle_Implementation_v1.1.md` com todos os placeholders possíveis preenchidos com base nas fontes, formatado em Markdown e pronto para uso.
2.  **Relatório de Preenchimento (Validação Estrutural):** Uma breve seção ao final do output (ou como comentário) detalhando como as seções principais foram preenchidas:
    *   Liste cada seção principal preenchida.
    *   Indique qual(is) `Documento(s) Fonte` foi(ram) usado(s) para preencher aquela seção.
    *   Mencione quaisquer placeholders que não puderam ser preenchidos por falta de informação nas fontes.
    *   **Exemplo de Relatório de Preenchimento:**
        ```
        ---
        **Relatório de Preenchimento:**
        *   Seção 'Contexto Arquitetural > Dependências Diretas': Preenchida usando a Seção 3.1 do `Output_Tocrisna_Blueprint.md`.
        *   Seção 'Contexto Arquitetural > Interfaces de Dependências': Preenchida usando a Seção 4 do `Output_Tocrisna_Blueprint.md`.
        *   Seção 'Stack Tecnológica': Preenchida usando `Veredito_Stack.md`.
        *   Placeholder `[NOME_DO_PROJETO]`: Preenchido usando `Output_Tocrisna_Blueprint.md`.
        *   Placeholder `[PLACEHOLDER_EXEMPLO_NAO_ENCONTRADO]`: Informação não encontrada nas fontes fornecidas.
        ---
        ```