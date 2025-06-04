## Análise de Implementação e Próximos Passos para Fotix

**Instruções para o Coordenador:**

Este documento organiza os módulos do projeto Fotix para guiar a implementação. Ele separa os "Módulos Base" (definições, utilitários e interfaces) dos "Módulos Principais" (que contêm a lógica central e as implementações concretas dos serviços e da UI).

*   **NÃO implemente os "Módulos Base" listados abaixo diretamente agora.** Suas pastas e arquivos básicos (como `__init__.py`, arquivos de interfaces, modelos de dados) serão criados ou modificados quando necessário pela IA (`ImplementadorMestre`) durante a implementação dos módulos principais que dependem deles. O conteúdo específico de módulos como `fotix.utils` será adicionado organicamente conforme a necessidade surgir.
*   **SIGA a "Ordem de Implementação Sugerida (Módulos Principais e Pontos de Teste de Integração)" abaixo.** Comece pelo **Item #1** da lista de Módulos Principais e prossiga sequencialmente.
*   Para **CADA item** da ordem numerada de Módulo Principal, use o `Prompt_ImplementadorMestre_vX.Y` (recomenda-se a versão mais recente, ex: v1.7+), preenchendo apenas o nome do módulo alvo (ex: "Item 1: `fotix.infrastructure.implementations.logging_service`"). Anexe sempre o `@Blueprint_Arquitetural.md`, este arquivo (`@Ordem_Com_Descricoes_e_Testes_Integracao.md`) e o código relevante já existente como contexto. A "Descrição de Alto Nível Inicial" listada abaixo para cada item servirá como ponto de partida para a IA.
*   **PONTOS DE TESTE DE INTEGRAÇÃO:** Em certos pontos, este documento indicará uma **">>> PARADA PARA TESTES DE INTEGRAÇÃO (Nome do Subsistema) <<<"**. Nestes momentos, **antes de prosseguir** com o próximo Módulo Principal da lista, você deverá usar um prompt dedicado para testes de integração (ex: `Prompt_IntegradorTester_vX.Y`, que será definido posteriormente) para guiar a IA na criação e execução de testes de integração para o grupo de módulos recém-concluído. Utilize os "Cenários Chave para Teste de Integração" listados como ponto de partida para esses testes. Após os testes de integração serem concluídos e validados, você poderá prosseguir para o próximo item da ordem de implementação.

---

### Módulos Base (Estrutura Inicial / Conteúdo On-Demand)

*   **`fotix.domain.models`**: Define as estruturas de dados centrais da aplicação (Pydantic models: `FileEntry`, `DuplicateSet`, `ScanConfig`, `BackupRecord`, `AppConfig`).
*   **`fotix.app_config`**: Lógica para carregar e prover `AppConfig`.
*   **`fotix.infrastructure.interfaces.logging` (`ILoggingService`)**: Define o contrato para o serviço de logging.
*   **`fotix.infrastructure.interfaces.file_system` (`IFileSystemService`)**: Define o contrato para operações de sistema de arquivos.
*   **`fotix.infrastructure.interfaces.hashing` (`IHashingService`)**: Define o contrato para o serviço de cálculo de hash.
*   **`fotix.infrastructure.interfaces.zip` (`IZipService`)**: Define o contrato para o serviço de manipulação de arquivos ZIP.
*   **`fotix.infrastructure.interfaces.concurrency` (`IConcurrencyService`)**: Define o contrato para o serviço de concorrência.
*   **`fotix.infrastructure.interfaces.backup` (`IBackupService`)**: Define o contrato para o serviço de backup.
*   **`fotix.utils.helpers`**: Contém funções auxiliares genéricas (a serem criadas conforme necessidade).

---

### Ordem de Implementação Sugerida (Módulos Principais e Pontos de Teste de Integração) - COMECE AQUI (Item #1)

1.  **`fotix.infrastructure.implementations.logging_service` (`LoggingService`)**
    *   **Descrição de Alto Nível Inicial:** Implementa a interface `ILoggingService` para configurar e fornecer funcionalidade de logging para a aplicação, suportando diferentes níveis e destinos (console, arquivo).
    *   **Justificativa da Ordem:** Logging é fundamental para desenvolvimento e depuração desde o início. É uma dependência comum para muitos outros serviços.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.interfaces.logging.ILoggingService`, `fotix.domain.models.AppConfig` (para configurações de log via `app_config`).

2.  **`fotix.infrastructure.implementations.file_system_service` (`FileSystemService`)**
    *   **Descrição de Alto Nível Inicial:** Implementa a interface `IFileSystemService` para abstrair todas as operações de sistema de arquivos, como listar arquivos, obter tamanho, mover para lixeira, copiar, etc.
    *   **Justificativa da Ordem:** Operações de arquivo são a base para a maioria das funcionalidades do Fotix. Depende do `LoggingService`.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.interfaces.file_system.IFileSystemService`, `fotix.infrastructure.interfaces.logging.ILoggingService`.

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (INFRAESTRUTURA BÁSICA: LOGGING E SISTEMA DE ARQUIVOS) <<<**

*   **Módulos Implementados neste Grupo:**
    *   `fotix.infrastructure.implementations.logging_service.LoggingService`
    *   `fotix.infrastructure.implementations.file_system_service.FileSystemService`
    *   (Módulos base associados: `fotix.domain.models` (para `AppConfig`), `fotix.app_config`, `fotix.infrastructure.interfaces.logging`, `fotix.infrastructure.interfaces.file_system`)
*   **Objetivo do Teste de Integração:** Verificar se o `FileSystemService` realiza operações de arquivo corretamente e se suas ações são logadas conforme esperado pelo `LoggingService` (que utiliza configurações do `AppConfig`).
*   **Cenários Chave para Teste de Integração:**
    1.  **Criação e Listagem Logada:** Use `FileSystemService` para criar um diretório temporário e um arquivo dentro dele. Verifique se o diretório e arquivo existem e se `list_files_recursive` os retorna. Confirme se logs de INFO/DEBUG são gerados para essas operações.
    2.  **Obtenção de Metadados Logada:** Use `FileSystemService` para obter o tamanho e data de modificação de um arquivo. Verifique a exatidão dos dados e a presença de logs.
    3.  **Movimentação para Lixeira Logada:** Crie um arquivo temporário, use `FileSystemService.move_to_trash()` e verifique se o arquivo não existe mais no local original (e se possível, se foi para a lixeira - isso pode ser difícil de automatizar de forma portável). Confirme os logs da operação.
    4.  **Erro de Permissão Logado:** Tente criar um arquivo em um diretório sem permissão de escrita (simule isso se necessário) usando `FileSystemService`. Verifique se uma exceção apropriada é tratada e se um log de ERROR é gerado.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y` (a ser definido) para gerar testes para estes cenários. Crie arquivos e diretórios temporários para os testes. Após os testes passarem e serem validados, prossiga para o próximo item da ordem de implementação.

---

3.  **`fotix.infrastructure.implementations.hashing_service` (`HashingService`)**
    *   **Descrição de Alto Nível Inicial:** Implementa a interface `IHashingService` para calcular hashes de arquivos (BLAKE3), essencial para a identificação de duplicatas.
    *   **Justificativa da Ordem:** O cálculo de hash é um pilar da funcionalidade de detecção de duplicatas. Depende do `LoggingService` e interage com arquivos via `IFileSystemService` (indiretamente, através de `read_file_chunks`).
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.interfaces.hashing.IHashingService`, `fotix.infrastructure.interfaces.logging.ILoggingService`.

4.  **`fotix.domain.core.duplicate_finder` (`DuplicateFinderEngine`)**
    *   **Descrição de Alto Nível Inicial:** Contém a lógica principal para identificar conjuntos de arquivos duplicados com base em seus hashes e tamanhos.
    *   **Justificativa da Ordem:** Implementa o core da lógica de negócio de detecção. Depende de `IHashingService` para obter hashes e `IFileSystemService` para obter tamanhos de arquivo (se não vierem pré-calculados).
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.domain.models` (`FileEntry`, `DuplicateSet`), `fotix.infrastructure.interfaces.hashing.IHashingService`, `fotix.infrastructure.interfaces.file_system.IFileSystemService`.

5.  **`fotix.infrastructure.implementations.concurrency_service` (`ConcurrencyService`)**
    *   **Descrição de Alto Nível Inicial:** Implementa a interface `IConcurrencyService` para executar tarefas em paralelo, como o cálculo de hash de múltiplos arquivos, melhorando a performance.
    *   **Justificativa da Ordem:** Necessário para otimizar o `ScanService`. Depende do `LoggingService`.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.interfaces.concurrency.IConcurrencyService`, `fotix.infrastructure.interfaces.logging.ILoggingService`, `fotix.domain.models.AppConfig` (para `max_workers`).

6.  **`fotix.infrastructure.implementations.zip_service` (`ZipService`)**
    *   **Descrição de Alto Nível Inicial:** Implementa a interface `IZipService` para extrair progressivamente arquivos de dentro de arquivos ZIP e calcular seus hashes, sem armazená-los permanentemente.
    *   **Justificativa da Ordem:** Adiciona a capacidade de processar arquivos ZIP, uma funcionalidade chave. Depende do `LoggingService` e do `IHashingService` para processar os arquivos internos.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.interfaces.zip.IZipService`, `fotix.infrastructure.interfaces.logging.ILoggingService`, `fotix.infrastructure.interfaces.hashing.IHashingService`, `fotix.domain.models.FileEntry`.

7.  **`fotix.application.services.scan_service` (`ScanService`)**
    *   **Descrição de Alto Nível Inicial:** Orquestra todo o processo de escaneamento de arquivos e diretórios (incluindo ZIPs), utilizando os serviços de infraestrutura e o `DuplicateFinderEngine` para encontrar duplicatas.
    *   **Justificativa da Ordem:** Agrupa as funcionalidades de infraestrutura e domínio relacionadas ao escaneamento em um caso de uso coeso. É um dos principais serviços da aplicação.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.interfaces.file_system.IFileSystemService`, `fotix.infrastructure.interfaces.zip.IZipService`, `fotix.infrastructure.interfaces.concurrency.IConcurrencyService`, `fotix.domain.core.duplicate_finder.DuplicateFinderEngine`, `fotix.domain.models`, `fotix.infrastructure.interfaces.logging.ILoggingService`.

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (MECANISMO CENTRAL DE ESCANEAMENTO E DETECÇÃO DE DUPLICATAS) <<<**

*   **Módulos Implementados neste Grupo:**
    *   `fotix.infrastructure.implementations.hashing_service.HashingService`
    *   `fotix.domain.core.duplicate_finder.DuplicateFinderEngine`
    *   `fotix.infrastructure.implementations.concurrency_service.ConcurrencyService`
    *   `fotix.infrastructure.implementations.zip_service.ZipService`
    *   `fotix.application.services.scan_service.ScanService`
    *   (Módulos base associados e já implementados anteriormente)
*   **Objetivo do Teste de Integração:** Validar o fluxo completo de escaneamento, desde a listagem de arquivos e extração de ZIPs, passando pelo cálculo de hashes (concorrente) e a correta identificação de conjuntos de arquivos duplicados pelo `DuplicateFinderEngine`, tudo orquestrado pelo `ScanService`.
*   **Cenários Chave para Teste de Integração:**
    1.  **Escaneamento Simples com Duplicatas:** Crie um diretório com alguns arquivos, incluindo pares de duplicatas idênticas (mesmo conteúdo, nomes diferentes) e arquivos únicos. Execute o `ScanService` neste diretório. Verifique se os `DuplicateSet`s corretos são retornados e se os arquivos únicos não são listados como duplicatas.
    2.  **Escaneamento de ZIP com Duplicatas Internas e Externas:** Crie um arquivo ZIP contendo alguns arquivos, onde um deles é duplicata de um arquivo fora do ZIP, e dois arquivos dentro do ZIP são duplicatas entre si. Execute o `ScanService`. Verifique se todas as duplicatas são corretamente identificadas.
    3.  **Escaneamento com Filtro de Extensão (se aplicável no ScanConfig):** Prepare arquivos com diferentes extensões. Configure o `ScanService` (via `ScanConfig`) para incluir/excluir certas extensões. Verifique se apenas os arquivos correspondentes são processados e se as duplicatas são encontradas corretamente dentro do conjunto filtrado.
    4.  **Escaneamento Concorrente de Múltiplos Arquivos Grandes:** Crie vários arquivos relativamente grandes (ex: 10-50MB cada, alguns duplicados). Execute o `ScanService`. Verifique se o processamento é mais rápido que o sequencial (difícil de testar automaticamente, mas valide a lógica de uso do `ConcurrencyService`) e se as duplicatas são encontradas. Monitore logs para erros de concorrência.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y` para gerar testes. Prepare estruturas de diretórios e arquivos ZIP de teste. Valide os `FileEntry` e `DuplicateSet` retornados pelo `ScanService`. Após validação, prossiga.

---

8.  **`fotix.domain.core.selection_strategy` (`SelectionStrategy` - ex: `DefaultSelectionStrategy`)**
    *   **Descrição de Alto Nível Inicial:** Implementa a lógica para decidir automaticamente qual arquivo manter de um conjunto de duplicatas, com base em critérios como data, resolução, etc.
    *   **Justificativa da Ordem:** Necessário para o `DuplicateManagementService` automatizar a seleção de arquivos para remoção.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.domain.models` (`FileEntry`, `DuplicateSet`).

9.  **`fotix.infrastructure.implementations.backup_service` (`BackupService`)**
    *   **Descrição de Alto Nível Inicial:** Implementa a interface `IBackupService` para gerenciar a criação de backups de arquivos (copiando para local seguro) e sua restauração, incluindo metadados.
    *   **Justificativa da Ordem:** Funcionalidade crítica de segurança antes da remoção de arquivos. Depende do `LoggingService`, `IFileSystemService` e `AppConfig` (para `backup_root_path`).
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.interfaces.backup.IBackupService`, `fotix.infrastructure.interfaces.logging.ILoggingService`, `fotix.infrastructure.interfaces.file_system.IFileSystemService`, `fotix.domain.models` (`FileEntry`, `BackupRecord`, `AppConfig`).

10. **`fotix.application.services.duplicate_management_service` (`DuplicateManagementService`)**
    *   **Descrição de Alto Nível Inicial:** Orquestra a seleção de duplicatas (usando `SelectionStrategy`), o backup dos arquivos a serem removidos (via `BackupService`) e a remoção segura (via `FileSystemService`).
    *   **Justificativa da Ordem:** Combina a lógica de seleção, backup e remoção em um caso de uso. Depende dos serviços implementados anteriormente.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.interfaces.file_system.IFileSystemService`, `fotix.infrastructure.interfaces.backup.IBackupService`, `fotix.domain.core.selection_strategy.SelectionStrategy`, `fotix.domain.models`, `fotix.infrastructure.interfaces.logging.ILoggingService`.

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (GERENCIAMENTO DE DUPLICATAS: SELEÇÃO, BACKUP E REMOÇÃO) <<<**

*   **Módulos Implementados neste Grupo:**
    *   `fotix.domain.core.selection_strategy.DefaultSelectionStrategy`
    *   `fotix.infrastructure.implementations.backup_service.BackupService`
    *   `fotix.application.services.duplicate_management_service.DuplicateManagementService`
    *   (Módulos base associados e já implementados anteriormente)
*   **Objetivo do Teste de Integração:** Validar o fluxo completo de gerenciamento de duplicatas: a aplicação da estratégia de seleção, o backup correto dos arquivos marcados para remoção e a subsequente remoção (para lixeira) dos arquivos originais.
*   **Cenários Chave para Teste de Integração:**
    1.  **Seleção e Backup/Remoção Padrão:** Dado um `DuplicateSet`, use o `DuplicateManagementService` para aplicar a estratégia de seleção padrão. Verifique quais arquivos são selecionados para manter/remover. Confirme que os arquivos a serem removidos são backupeados pelo `BackupService` (verifique existência no diretório de backup e metadados) e depois movidos para a lixeira pelo `FileSystemService`.
    2.  **Seleção Alterada (se a estratégia permitir configuração ou se houver múltiplas):** Se a `SelectionStrategy` puder ser configurada (ex: priorizar arquivo mais antigo vs. mais novo), teste com diferentes configurações e verifique o resultado do backup/remoção.
    3.  **Falha no Backup Impedindo Remoção:** Simule uma falha no `BackupService` (ex: diretório de backup não gravável). Verifique se o `DuplicateManagementService` não prossegue com a remoção do arquivo original e loga o erro.
    4.  **Verificação de Metadados de Backup:** Após um backup bem-sucedido, verifique se os `BackupRecord`s criados pelo `BackupService` contêm as informações corretas sobre os arquivos originais.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y`. Prepare `DuplicateSet`s de teste. Configure um diretório de backup temporário. Valide os arquivos no backup, os metadados e o estado dos arquivos originais. Após validação, prossiga.

---

11. **`fotix.application.services.restore_service` (`RestoreService`)**
    *   **Descrição de Alto Nível Inicial:** Gerencia o processo de restauração de arquivos a partir dos backups feitos pelo `BackupService`.
    *   **Justificativa da Ordem:** Complementa a funcionalidade de backup, permitindo a recuperação de dados.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.interfaces.file_system.IFileSystemService`, `fotix.infrastructure.interfaces.backup.IBackupService`, `fotix.domain.models`, `fotix.infrastructure.interfaces.logging.ILoggingService`.

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (FUNCIONALIDADE DE RESTAURAÇÃO DE BACKUP) <<<**

*   **Módulos Implementados neste Grupo:**
    *   `fotix.application.services.restore_service.RestoreService`
    *   (Assume `BackupService` e `FileSystemService` já testados e funcionando)
*   **Objetivo do Teste de Integração:** Validar que arquivos previamente backupeados podem ser listados e restaurados para um local especificado.
*   **Cenários Chave para Teste de Integração:**
    1.  **Listar Backups Existentes:** Use o `BackupService` (ou `RestoreService` se ele expor essa funcionalidade) para listar os `BackupRecord`s disponíveis de backups feitos em testes anteriores.
    2.  **Restaurar Arquivo para Local Original:** Selecione um `BackupRecord` e use o `RestoreService` para restaurar o arquivo para seu caminho original (ou um caminho de teste que simule o original). Verifique se o arquivo é restaurado corretamente.
    3.  **Restaurar Arquivo para Novo Local:** Selecione um `BackupRecord` e use o `RestoreService` para restaurar o arquivo para um novo diretório. Verifique.
    4.  **Tentativa de Restaurar Backup Inexistente/Corrompido:** Tente restaurar usando um `BackupRecord` inválido ou apontando para um arquivo de backup que foi removido manualmente. Verifique o tratamento de erro e logs.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y`. Utilize backups criados em testes anteriores ou crie novos específicos para este teste. Valide o conteúdo e localização dos arquivos restaurados. Após validação, prossiga.

---

12. **`fotix.application.services.configuration_service` (`ConfigurationService`)**
    *   **Descrição de Alto Nível Inicial:** Gerencia as configurações da aplicação (lendo de `AppConfig` e, potencialmente, salvando modificações). Fornece acesso fácil às configurações para outros serviços e para a UI.
    *   **Justificativa da Ordem:** Embora `AppConfig` e `app_config.py` sejam base, este serviço encapsula a lógica de gerenciamento de forma mais robusta, podendo interagir com a UI. Colocado aqui pois as funcionalidades core já estão de pé.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.domain.models.AppConfig` (via `app_config.py`), `fotix.infrastructure.interfaces.file_system.IFileSystemService` (para salvar), `fotix.infrastructure.interfaces.logging.ILoggingService`.

13. **`fotix.application.services.reporting_service` (`ReportingService`)**
    *   **Descrição de Alto Nível Inicial:** Coleta informações e estatísticas do processamento para relatórios e fornece acesso aos logs detalhados para a UI.
    *   **Justificativa da Ordem:** Provê dados para a UI. Depende principalmente do `LoggingService` já estabelecido.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.interfaces.logging.ILoggingService`.

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (SERVIÇOS DE SUPORTE: CONFIGURAÇÃO E RELATÓRIOS) <<<**

*   **Módulos Implementados neste Grupo:**
    *   `fotix.application.services.configuration_service.ConfigurationService`
    *   `fotix.application.services.reporting_service.ReportingService`
*   **Objetivo do Teste de Integração:** Verificar se as configurações podem ser lidas (e salvas, se implementado) e se os logs podem ser recuperados para exibição.
*   **Cenários Chave para Teste de Integração:**
    1.  **Ler Configuração Padrão:** Use `ConfigurationService` para obter valores de configuração do `AppConfig` carregado. Verifique se correspondem aos padrões ou ao arquivo de configuração.
    2.  **Modificar e Salvar Configuração (se aplicável):** Se `ConfigurationService` suportar salvar, modifique uma configuração, salve-a e recarregue para verificar a persistência.
    3.  **Recuperar Logs via ReportingService:** Adicione algumas entradas de log usando o `LoggingService`. Use `ReportingService` para buscar as últimas N entradas de log. Verifique se os logs corretos são retornados.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y`. Prepare um arquivo de configuração de teste. Gere logs de teste. Valide os dados retornados pelos serviços. Após validação, prossiga para a camada de UI.

---

14. **`fotix.ui.dialogs.settings_dialog` (`SettingsDialog`)**
    *   **Descrição de Alto Nível Inicial:** Janela de diálogo que permite ao usuário visualizar e modificar as configurações da aplicação, interagindo com o `ConfigurationService`.
    *   **Justificativa da Ordem:** Uma das primeiras views da UI a ser implementada, pois interage com um serviço de backend já pronto e é relativamente independente de outros fluxos da UI.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.application.services.configuration_service.ConfigurationService`, PySide6.

15. **`fotix.ui.views.log_view` (`LogView`)**
    *   **Descrição de Alto Nível Inicial:** Componente de UI para exibir os logs da aplicação de forma amigável, obtendo-os do `ReportingService`.
    *   **Justificativa da Ordem:** UI para uma funcionalidade de backend já implementada.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.application.services.reporting_service.ReportingService`, PySide6.

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (UI: CONFIGURAÇÕES E VISUALIZAÇÃO DE LOGS) <<<**

*   **Módulos Implementados neste Grupo:**
    *   `fotix.ui.dialogs.settings_dialog.SettingsDialog`
    *   `fotix.ui.views.log_view.LogView`
    *   (Serviços de backend associados: `ConfigurationService`, `ReportingService`)
*   **Objetivo do Teste de Integração:** Verificar se as janelas de Configurações e Logs interagem corretamente com seus respectivos serviços de aplicação, exibindo dados e (para configurações) persistindo mudanças.
*   **Cenários Chave para Teste de Integração (Podem requerer testes manuais ou frameworks de teste de UI):**
    1.  **Exibir Configurações:** Abra o `SettingsDialog`. Verifique se os campos exibem os valores atuais do `ConfigurationService`.
    2.  **Modificar e Aplicar Configuração:** Modifique um valor no `SettingsDialog` (ex: caminho do backup) e aplique/salve. Feche e reabra o diálogo, ou verifique diretamente no `ConfigurationService` (ou no arquivo de config), se a mudança foi persistida.
    3.  **Exibir Logs no LogView:** Gere alguns logs de teste. Abra o `LogView`. Verifique se os logs são exibidos corretamente.
    4.  **Atualização de Logs (se dinâmico):** Se o `LogView` suportar atualização em tempo real, gere novos logs enquanto a view está aberta e veja se eles aparecem.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y` (para testes de UI, pode ser mais complexo, focando em interações com mocks dos serviços de aplicação inicialmente, ou testes E2E se o framework permitir). Após validação, prossiga.

---

16. **`fotix.ui.views.directory_selection_view` (`DirectorySelectionView`)**
    *   **Descrição de Alto Nível Inicial:** Permite ao usuário selecionar diretórios/ZIPs para escanear e configurar opções de escaneamento. Interage com `ScanService` e `ConfigurationService`.
    *   **Justificativa da Ordem:** Ponto de entrada para a funcionalidade principal de escaneamento.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.application.services.scan_service.ScanService`, `fotix.application.services.configuration_service.ConfigurationService`, PySide6.

17. **`fotix.ui.views.scan_progress_view` (`ScanProgressView`)**
    *   **Descrição de Alto Nível Inicial:** Exibe o progresso do escaneamento em tempo real e permite cancelamento. Interage com `ScanService`.
    *   **Justificativa da Ordem:** UI para feedback durante o escaneamento, ligada à `DirectorySelectionView`.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.application.services.scan_service.ScanService`, PySide6.

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (UI: FLUXO DE INÍCIO DE ESCANEAMENTO E PROGRESSO) <<<**

*   **Módulos Implementados neste Grupo:**
    *   `fotix.ui.views.directory_selection_view.DirectorySelectionView`
    *   `fotix.ui.views.scan_progress_view.ScanProgressView`
    *   (Serviço de backend associado: `ScanService`)
*   **Objetivo do Teste de Integração:** Validar que o usuário pode configurar e iniciar um escaneamento, e que o progresso é exibido corretamente.
*   **Cenários Chave para Teste de Integração:**
    1.  **Configurar e Iniciar Escaneamento:** No `DirectorySelectionView`, selecione um diretório de teste, defina opções (se houver) e inicie o escaneamento. Verifique se o `ScanService` é chamado com os parâmetros corretos.
    2.  **Exibir Progresso:** Durante o escaneamento (simulado ou real curto), verifique se o `ScanProgressView` exibe atualizações de progresso (arquivos processados, etc.) emitidas pelo `ScanService`.
    3.  **Cancelar Escaneamento:** Inicie um escaneamento. Clique no botão de cancelar no `ScanProgressView`. Verifique se o comando de cancelamento é enviado ao `ScanService` e se o processo é interrompido (ou sinalizado como cancelado).
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y`. Pode ser necessário mockar partes do `ScanService` para controlar o progresso e o cancelamento para testes de UI automatizados. Após validação, prossiga.

---

18. **`fotix.ui.views.results_view` (`ResultsView`)**
    *   **Descrição de Alto Nível Inicial:** Apresenta os conjuntos de duplicatas encontrados, permitindo revisão e confirmação de ações. Interage com `DuplicateManagementService`.
    *   **Justificativa da Ordem:** UI para interagir com os resultados do escaneamento e gerenciar duplicatas.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.application.services.duplicate_management_service.DuplicateManagementService`, PySide6.

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (UI: VISUALIZAÇÃO E GERENCIAMENTO DE RESULTADOS) <<<**

*   **Módulos Implementados neste Grupo:**
    *   `fotix.ui.views.results_view.ResultsView`
    *   (Serviço de backend associado: `DuplicateManagementService`)
*   **Objetivo do Teste de Integração:** Validar que a `ResultsView` exibe corretamente os `DuplicateSet`s e permite ao usuário interagir com eles para confirmar a remoção (que acionará o `DuplicateManagementService`).
*   **Cenários Chave para Teste de Integração:**
    1.  **Exibir Resultados:** Forneça `DuplicateSet`s de teste (obtidos de um `ScanService` mockado ou de um escaneamento real anterior) para o `ResultsView`. Verifique se os conjuntos e arquivos são exibidos corretamente, incluindo as seleções automáticas da `SelectionStrategy`.
    2.  **Alterar Seleção (se permitido):** Se a UI permitir, altere a seleção de qual arquivo manter/remover dentro de um `DuplicateSet`. Verifique se a UI reflete a mudança.
    3.  **Confirmar Remoção:** Clique no botão para confirmar a remoção dos arquivos selecionados. Verifique se o `DuplicateManagementService` é chamado com os `DuplicateSet`s e seleções corretas para processar o backup e a remoção.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y`. Prepare `DuplicateSet`s de teste. Valide a interação com o `DuplicateManagementService`. Após validação, prossiga.

---

19. **`fotix.ui.views.backup_restore_view` (`BackupRestoreView`)**
    *   **Descrição de Alto Nível Inicial:** Lista backups disponíveis e permite ao usuário restaurar arquivos/conjuntos. Interage com `RestoreService`.
    *   **Justificativa da Ordem:** UI para a funcionalidade de restauração.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.application.services.restore_service.RestoreService`, PySide6.

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (UI: FLUXO DE RESTAURAÇÃO DE BACKUP) <<<**

*   **Módulos Implementados neste Grupo:**
    *   `fotix.ui.views.backup_restore_view.BackupRestoreView`
    *   (Serviço de backend associado: `RestoreService`)
*   **Objetivo do Teste de Integração:** Validar que a `BackupRestoreView` lista backups e permite ao usuário iniciar uma restauração através do `RestoreService`.
*   **Cenários Chave para Teste de Integração:**
    1.  **Listar Backups:** Popule o `RestoreService` com `BackupRecord`s de teste. Abra a `BackupRestoreView`. Verifique se os backups são listados corretamente.
    2.  **Selecionar e Restaurar Backup:** Selecione um backup na lista e inicie a restauração. Verifique se o `RestoreService` é chamado com o `BackupRecord` correto e o caminho de destino.
    3.  **Feedback de Restauração:** Verifique se a UI fornece feedback sobre o sucesso ou falha da operação de restauração.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y`. Prepare `BackupRecord`s de teste. Valide a interação com o `RestoreService`. Após validação, prossiga.

---

20. **`fotix.ui.main_window` (`FotixMainWindow`)**
    *   **Descrição de Alto Nível Inicial:** Janela principal da aplicação, orquestrando a navegação entre as diferentes views/dialogs e integrando todas as funcionalidades.
    *   **Justificativa da Ordem:** Componente final da UI que une todas as partes.
    *   **Dependências Chave (Inferidas do Blueprint):** Todos os serviços de aplicação (`ScanService`, `DuplicateManagementService`, `RestoreService`, `ReportingService`, `ConfigurationService`), todas as Views/Dialogs, PySide6.

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (APLICAÇÃO COMPLETA - FLUXOS END-TO-END) <<<**

*   **Módulos Implementados neste Grupo:**
    *   `fotix.ui.main_window.FotixMainWindow`
    *   (Todas as Views, Dialogs e Serviços de Aplicação/Infraestrutura previamente implementados e testados)
*   **Objetivo do Teste de Integração:** Validar os principais fluxos de usuário de ponta a ponta, garantindo que todas as camadas e componentes interajam corretamente como um sistema coeso.
*   **Cenários Chave para Teste de Integração (Principalmente manuais ou com ferramentas E2E):**
    1.  **Fluxo Completo de Detecção e Remoção:**
        *   Abra a aplicação.
        *   Configure um diretório de backup nas Configurações.
        *   Selecione um diretório de teste (com duplicatas) na `DirectorySelectionView` e inicie o escaneamento.
        *   Observe o progresso na `ScanProgressView`.
        *   Revise os resultados na `ResultsView`, confirme as seleções.
        *   Execute a ação de remoção/backup.
        *   Verifique (fora da aplicação) se os arquivos foram movidos para a lixeira e se os backups foram criados.
        *   Verifique os logs na `LogView`.
    2.  **Fluxo Completo de Restauração:**
        *   Após o cenário 1, vá para a `BackupRestoreView`.
        *   Localize um dos backups criados.
        *   Restaure o arquivo para seu local original ou um novo local.
        *   Verifique (fora da aplicação) se o arquivo foi restaurado.
    3.  **Alteração de Configuração Afetando Comportamento:**
        *   Mude uma configuração relevante (ex: critério de seleção padrão) no `SettingsDialog`.
        *   Execute um novo escaneamento e verifique na `ResultsView` se a nova configuração de seleção foi aplicada.
*   **Instrução para o Coordenador:** Estes são testes E2E. Use o `Prompt_IntegradorTester_vX.Y` se ele evoluir para suportar a geração de scripts de teste E2E (ex: com Playwright para PySide se houver bindings, ou Selenium-like tools se fosse web). Caso contrário, realize testes manuais seguindo estes cenários. Esta é a validação final antes de considerar o ciclo de desenvolvimento principal para v5.0 como concluído.