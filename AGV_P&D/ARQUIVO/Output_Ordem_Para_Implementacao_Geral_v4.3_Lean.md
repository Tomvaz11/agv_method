# Ordem de Implementação e Plano de Testes de Integração: Fotix

## Alvo Zero: Setup do Projeto

**Instruções para o `ImplementadorMestre`:**

1.  **Criar a Estrutura de Diretórios:** Crie a estrutura de diretórios completa conforme definido na seção `6. Estrutura de Diretórios Proposta` do Blueprint.
2.  **Criar o arquivo `.gitignore`:** Crie o arquivo `.gitignore` na raiz do projeto. O conteúdo deste arquivo deve ser copiado exatamente da seção `7. Arquivo .gitignore Proposto` do Blueprint.
3.  **Criar o arquivo `pyproject.toml`:** Crie o arquivo `pyproject.toml` na raiz do projeto. O conteúdo deste arquivo deve ser copiado exatamente da seção `11. Arquivo pyproject.toml Proposto` do Blueprint.
4.  **Criar os arquivos `__init__.py`:** Crie arquivos `__init__.py` vazios em todos os subdiretórios dentro de `src/fotix/` (application, domain, infrastructure, ui, ui/views) para garantir que sejam tratados como pacotes Python.

---

## Ordem de Implementação por Módulo Principal

1.  `fotix.domain.models`
2.  `fotix.domain.strategies`
    `>>> PARADA PARA TESTES DE INTEGRAÇÃO (NÚCLEO DO DOMÍNIO) <<<`

    *   **Módulos no Grupo:**
        *   `fotix.domain.models`
        *   `fotix.domain.strategies`
    *   **Objetivo do Teste:** Validar que a estratégia de seleção (`ISelectionStrategy`) processa corretamente um conjunto de modelos de dados (`DuplicateSet` com `FileMeta`) e seleciona o arquivo correto para manter, de acordo com as regras de negócio puras.
    *   **Cenários Chave:**
        1.  **Cenário de Prioridade por Data:** Dado um `DuplicateSet` com três arquivos, cada um com uma data de criação (`creation_time`) diferente, verificar se a estratégia seleciona consistentemente o arquivo mais antigo.
        2.  **Cenário de Desempate por Caminho:** Dado um `DuplicateSet` onde dois arquivos têm a mesma data de criação, verificar se a estratégia seleciona o arquivo com o caminho (`path`) mais curto como critério de desempate.
        3.  **Cenário de Prioridade de Arquivo Não-ZIP:** Dado um `DuplicateSet` onde um arquivo tem `is_in_zip=True` e outro `is_in_zip=False` (e outros metadados são idênticos ou menos prioritários), verificar se a estratégia prefere o arquivo que não está dentro de um ZIP.
        4.  **Cenário de Prioridade por Resolução:** Dado um `DuplicateSet` de imagens, onde uma tem uma resolução (`resolution`) significativamente maior que as outras, verificar se a estratégia prioriza o arquivo de maior resolução, mesmo que não seja o mais antigo.

3.  `fotix.infrastructure.hashing`
4.  `fotix.infrastructure.file_system`
5.  `fotix.infrastructure.concurrency`
    `>>> PARADA PARA TESTES DE INTEGRAÇÃO (INFRAESTRUTURA DE VARREDURA E PROCESSAMENTO) <<<`

    *   **Módulos no Grupo:**
        *   `fotix.infrastructure.hashing`
        *   `fotix.infrastructure.file_system`
        *   `fotix.infrastructure.concurrency`
    *   **Objetivo do Teste:** Verificar que os serviços de infraestrutura podem colaborar para encontrar arquivos de mídia no sistema, popular seus metadados (`FileMeta`) e calcular seus hashes de forma concorrente.
    *   **Cenários Chave:**
        1.  **Cenário de Varredura e Hash Paralelo:** Criar uma estrutura de diretórios temporária com arquivos duplicados e únicos. Usar `FileSystemService` para encontrar os arquivos e, em seguida, usar `ConcurrencyService.map` para aplicar o `HashingService.calculate_hash` (ou uma função wrapper). Verificar se todos os objetos `FileMeta` são preenchidos com o hash correto e se os arquivos idênticos produzem hashes idênticos.
        2.  **Cenário de Extração de Metadados:** Verificar se o `FileSystemService` preenche corretamente todos os campos do `FileMeta` durante a varredura: `path`, `size`, `creation_time`, e `resolution` (para imagens válidas).
        3.  **Cenário de Movimentação para Lixeira:** Chamar o método `move_to_trash` do `FileSystemService` em um arquivo temporário e verificar se o arquivo desaparece do local original e pode ser encontrado na lixeira do sistema operacional (verificação manual ou com helpers de teste específicos).

6.  `fotix.infrastructure.zip_handler`
7.  `fotix.infrastructure.backup`
8.  `fotix.infrastructure.logging`
9.  `fotix.application.services`
    `>>> PARADA PARA TESTES DE INTEGRAÇÃO (FLUXO END-TO-END DO SERVIÇO DE APLICAÇÃO) <<<`

    *   **Módulos no Grupo:**
        *   `fotix.infrastructure.zip_handler`
        *   `fotix.infrastructure.backup`
        *   `fotix.infrastructure.logging`
        *   `fotix.application.services`
        *   (E todos os módulos das paradas anteriores)
    *   **Objetivo do Teste:** Validar que o `ScanService` orquestra corretamente o fluxo completo de ponta a ponta: configuração, varredura (incluindo ZIPs), identificação de duplicatas, seleção, backup e remoção segura, sem a necessidade de uma UI.
    *   **Cenários Chave:**
        1.  **Cenário Completo "Caminho Feliz":** Preparar um diretório com um par de arquivos duplicados. Executar o fluxo completo do `ScanService`. Verificar se: (a) o `BackupService` cria uma cópia do arquivo a ser removido em seu diretório de backup, (b) o manifesto de backup (`manifest.json`) é atualizado corretamente, e (c) o arquivo duplicado original é movido para a lixeira.
        2.  **Cenário com Arquivo ZIP:** Preparar um diretório com `foto.jpg` e `arquivo.zip` contendo uma cópia de `foto.jpg`. Executar a varredura com `include_zips=True`. Verificar se o `ScanService` identifica a duplicata e (assumindo a lógica padrão) marca o arquivo de dentro do ZIP para remoção (sem executar a remoção, já que não é possível remover de dentro de um ZIP, mas a identificação deve ocorrer).
        3.  **Cenário de Restauração de Backup:** Após executar o Cenário 1, usar a instância do `BackupService` para listar os backups e restaurar o arquivo removido. Verificar se o arquivo retorna ao seu local original e se a entrada correspondente é removida do manifesto.
        4.  **Cenário "Sem Duplicatas":** Executar o `ScanService` em um diretório contendo apenas arquivos únicos. Verificar se nenhum arquivo é enviado para backup ou lixeira e se o `ScanStats` retornado reporta `duplicates_found = 0`.

10. `fotix.ui`
    `>>> PARADA PARA TESTES DE INTEGRAÇÃO (INTEGRAÇÃO COMPLETA DA UI COM O BACKEND) <<<`

    *   **Módulos no Grupo:**
        *   `fotix.ui` (incluindo `MainWindow`, `views` e `worker`)
    *   **Objetivo do Teste:** Garantir que a camada de apresentação (PySide6) se comunique corretamente com a camada de aplicação (`ScanService`), iniciando tarefas em uma thread separada, exibindo progresso e resultados, e acionando ações sem congelar a interface.
    *   **Cenários Chave:**
        1.  **Cenário de Início e Progresso:** Usando `pytest-qt`, simular a seleção de um diretório na `ConfigView` e o clique no botão "Iniciar". Verificar se o `ScanWorker` é iniciado em uma `QThread`. Monitorar os sinais emitidos pelo worker e garantir que a UI (ex: `ProgressView`) os receba e atualize uma barra de progresso ou um contador de texto.
        2.  **Cenário de Exibição e Confirmação de Resultados:** Após a conclusão de uma varredura (com duplicatas), verificar se os dados do `DuplicateSet` são corretamente populados na `ResultsView`. Simular o clique do usuário no botão "Aplicar" ou "Remover Duplicatas" e verificar se o método apropriado no `ScanService` é invocado.
        3.  **Cenário de Responsividade da UI:** Iniciar uma varredura mockada para ser longa (usando `time.sleep` no `ScanWorker`). Durante a execução, verificar se a janela principal (`MainWindow`) permanece responsiva (pode ser movida, redimensionada) e se os botões não relacionados à varredura ainda respondem ou estão corretamente desabilitados.
        4.  **Cenário de Restauração via UI:** Navegar para a `RestoreView`, verificar se ela exibe corretamente a lista de arquivos obtida do `BackupService`. Simular a seleção de um item e o clique no botão "Restaurar" e confirmar que a chamada correspondente no backend é executada.