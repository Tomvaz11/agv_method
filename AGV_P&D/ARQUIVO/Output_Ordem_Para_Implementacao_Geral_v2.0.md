## Análise de Implementação e Próximos Passos para Fotix

**Instruções para o Coordenador:**

Este documento organiza os módulos do projeto Fotix para guiar a implementação. Ele separa os "Módulos Base" (definições, utilitários e interfaces) dos "Módulos Principais" (que contêm a lógica central e as implementações concretas dos serviços).

*   **NÃO implemente os "Módulos Base" listados abaixo diretamente agora.** Suas pastas e arquivos básicos (como `__init__.py`, arquivos de interfaces, modelos de dados) serão criados ou modificados quando necessário pela IA (`ImplementadorMestre`) durante a implementação dos módulos principais que dependem deles. O conteúdo específico de módulos como `fotix.utils` será adicionado organicamente conforme a necessidade surgir.
*   **SIGA a "Ordem de Implementação Sugerida (Módulos Principais e Pontos de Teste de Integração)" abaixo.** Comece pelo **Item #1** da lista de Módulos Principais e prossiga sequencialmente.
*   Para **CADA item** da ordem numerada de Módulo Principal, use o `Prompt_ImplementadorMestre_vX.Y` (recomenda-se a versão mais recente, ex: v1.7+), preenchendo apenas o nome do módulo alvo (ex: "Item 1: `fotix.infrastructure.logging_impl.LoggingService`"). Anexe sempre o `@Blueprint_Arquitetural.md`, este arquivo (`@Ordem_Com_Descricoes_e_Testes_Integracao.md`) e o código relevante já existente como contexto. A "Descrição de Alto Nível Inicial" listada abaixo para cada item servirá como ponto de partida para a IA.
*   **PONTOS DE TESTE DE INTEGRAÇÃO:** Em certos pontos, este documento indicará uma **">>> PARADA PARA TESTES DE INTEGRAÇÃO (Nome do Subsistema) <<<"**. Nestes momentos, **antes de prosseguir** com o próximo Módulo Principal da lista, você deverá usar um prompt dedicado para testes de integração (ex: `Prompt_IntegradorTester_vX.Y`, que será definido posteriormente) para guiar a IA na criação e execução de testes de integração para o grupo de módulos recém-concluído. Utilize os "Cenários Chave para Teste de Integração" listados como ponto de partida para esses testes. Após os testes de integração serem concluídos e validados, você poderá prosseguir para o próximo item da ordem de implementação.

---

### Módulos Base (Estrutura Inicial / Conteúdo On-Demand)

*   **`fotix.domain.models`**: Define as estruturas de dados centrais da aplicação (ex: `FileInfo`, `DuplicateGroup`, `ScanSettings`, `AppConfig`, `BackupLogEntry`). Essencial para a comunicação entre camadas e para a lógica de negócio.
*   **`fotix.utils.media_parser`**: Contém utilitários para extrair metadados específicos de arquivos de mídia, como resolução de imagens e vídeos. Usado pelo `FileAnalyzer`.
*   **`fotix.infrastructure.file_system` (Interface `IFileSystemService`)**: Define o contrato para operações de sistema de arquivos.
*   **`fotix.infrastructure.zip_handler` (Interface `IZipHandlerService`)**: Define o contrato para manipulação de arquivos ZIP.
*   **`fotix.infrastructure.hashing` (Interface `IHashingService`)**: Define o contrato para cálculo de hash de arquivos.
*   **`fotix.infrastructure.concurrency` (Interface `IConcurrencyService`)**: Define o contrato para execução paralela de tarefas.
*   **`fotix.infrastructure.backup_manager` (Interface `IBackupManagerService`)**: Define o contrato para gerenciamento de backups.
*   **`fotix.infrastructure.logging` (Interface `ILoggingService`, se formalmente definida, ou a própria configuração do `logging` stdlib)**: Define o contrato ou a configuração para o sistema de logging.
*   **`fotix.infrastructure.config_loader` (Interface `IConfigLoader`, se formalmente definida)**: Define o contrato para carregar e persistir configurações da aplicação.

---

### Ordem de Implementação Sugerida (Módulos Principais e Pontos de Teste de Integração) - COMECE AQUI (Item #1)

1.  **`fotix.infrastructure.logging_impl.LoggingService`**
    *   **Descrição de Alto Nível Inicial:** Configurar e fornecer uma interface para o sistema de logging em toda a aplicação, utilizando a biblioteca `logging` padrão do Python.
    *   **Justificativa da Ordem:** Fundamental para permitir o rastreamento e depuração desde os primeiros estágios de desenvolvimento dos demais módulos.
    *   **Dependências Chave (Inferidas do Blueprint):** Nenhuma dependência de outros módulos principais nesta fase (pode depender de `AppConfig` do `fotix.domain.models` para configuração, que é um módulo base).

2.  **`fotix.infrastructure.file_system_impl.FileSystemService`**
    *   **Descrição de Alto Nível Inicial:** Implementar a interface `IFileSystemService` para abstrair operações de sistema de arquivos como listar, ler, mover e deletar arquivos de forma segura (usando `send2trash`).
    *   **Justificativa da Ordem:** Muitos outros módulos de infraestrutura e core dependerão de operações de arquivo.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.logging_impl.LoggingService` (para logar operações), interface `IFileSystemService`.

3.  **`fotix.infrastructure.config_loader_impl.ConfigLoader`**
    *   **Descrição de Alto Nível Inicial:** Implementar a lógica para carregar e persistir as configurações da aplicação (ex: de um arquivo JSON), utilizando `AppConfig` de `fotix.domain.models`.
    *   **Justificativa da Ordem:** Permite que a aplicação comece a gerenciar suas configurações, o que pode influenciar o comportamento de outros serviços.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.file_system_impl.FileSystemService` (para ler/escrever arquivo de config), `fotix.domain.models.AppConfig`, `fotix.infrastructure.logging_impl.LoggingService`.

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (INFRAESTRUTURA BÁSICA: LOG, ARQUIVOS, CONFIGURAÇÃO) <<<**

*   **Módulos Implementados neste Grupo:** `fotix.infrastructure.logging_impl.LoggingService`, `fotix.infrastructure.file_system_impl.FileSystemService`, `fotix.infrastructure.config_loader_impl.ConfigLoader` (e seus módulos base associados como `fotix.domain.models` para `AppConfig`).
*   **Objetivo do Teste de Integração:** Validar a capacidade de carregar/salvar configurações, realizar operações de arquivo e garantir que essas ações sejam corretamente logadas.
*   **Cenários Chave para Teste de Integração:**
    1.  **Carregar Configuração Padrão e Logar:** Tentar carregar uma configuração (usando `ConfigLoader`). Se o arquivo não existir, ele deve criar um padrão (`AppConfig`), salvá-lo (`FileSystemService`) e logar a ação (`LoggingService`). Verificar o conteúdo do arquivo e os logs.
    2.  **Modificar Configuração e Logar:** Carregar uma configuração existente, modificar um valor, salvá-la e verificar se o arquivo foi atualizado e se a ação foi logada.
    3.  **Operação de Arquivo Segura com Log:** Usar o `FileSystemService` para criar um arquivo, depois deletá-lo de forma segura (para a lixeira). Verificar se a operação foi bem-sucedida e se ambas as ações (criação e deleção) foram logadas adequadamente.
    4.  **Listagem de Arquivos Recursiva com Log:** Utilizar `FileSystemService` para listar arquivos em um diretório de teste (com subdiretórios) e verificar se a listagem está correta e se o início/fim da operação de listagem é logado.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y` (a ser definido) para gerar testes para estes cenários. Após os testes passarem e serem validados, prossiga para o próximo item da ordem de implementação.

---

4.  **`fotix.application.services.configuration_service.ConfigurationService`**
    *   **Descrição de Alto Nível Inicial:** Fornecer uma interface para a UI e outros serviços acessarem as configurações da aplicação carregadas pelo `ConfigLoader`.
    *   **Justificativa da Ordem:** Disponibiliza as configurações carregadas para o restante da aplicação de forma controlada.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.config_loader_impl.ConfigLoader`, `fotix.domain.models.AppConfig`.

5.  **`fotix.infrastructure.hashing_impl.HashingService`**
    *   **Descrição de Alto Nível Inicial:** Implementar a interface `IHashingService` para calcular hashes de arquivos (usando `blake3`), lendo-os em chunks para eficiência.
    *   **Justificativa da Ordem:** Componente crucial para a análise de arquivos e detecção de duplicatas.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.logging_impl.LoggingService`, interface `IHashingService`, `fotix.infrastructure.file_system_impl.FileSystemService` (para o método `calculate_hash_from_path`).

6.  **`fotix.infrastructure.zip_handler_impl.ZipHandlerService`**
    *   **Descrição de Alto Nível Inicial:** Implementar a interface `IZipHandlerService` para listar conteúdos de arquivos ZIP e extrair dados de entradas específicas de forma progressiva (usando `stream-unzip`).
    *   **Justificativa da Ordem:** Necessário para o `FileAnalyzer` processar arquivos dentro de ZIPs.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.logging_impl.LoggingService`, interface `IZipHandlerService`.

7.  **`fotix.core.file_analyzer.FileAnalyzer`**
    *   **Descrição de Alto Nível Inicial:** Analisar arquivos individuais (do disco ou de dentro de ZIPs) para extrair metadados (tamanho, datas, resolução via `fotix.utils.media_parser`) e calcular seu hash.
    *   **Justificativa da Ordem:** Combina vários serviços de infraestrutura para produzir `FileInfo`, que é a base para a detecção de duplicatas.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.hashing_impl.HashingService`, `fotix.infrastructure.file_system_impl.FileSystemService`, `fotix.infrastructure.zip_handler_impl.ZipHandlerService`, `fotix.domain.models.FileInfo`, `fotix.utils.media_parser` (módulo base), `fotix.infrastructure.logging_impl.LoggingService`.

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (ANÁLISE DE ARQUIVOS) <<<**

*   **Módulos Implementados neste Grupo:** `fotix.application.services.configuration_service.ConfigurationService`, `fotix.infrastructure.hashing_impl.HashingService`, `fotix.infrastructure.zip_handler_impl.ZipHandlerService`, `fotix.core.file_analyzer.FileAnalyzer` (e `fotix.utils.media_parser` que será criado organicamente).
*   **Objetivo do Teste de Integração:** Garantir que o `FileAnalyzer` consiga processar arquivos do sistema de arquivos e de dentro de arquivos ZIP, calculando hashes e extraindo metadados corretamente, usando os serviços de infraestrutura subjacentes.
*   **Cenários Chave para Teste de Integração:**
    1.  **Análise de Arquivo em Disco:** Criar um arquivo de teste no disco. Usar `FileAnalyzer` para processá-lo. Verificar se o `FileInfo` resultante contém o caminho correto, tamanho, hash (calculado pelo `HashingService` via `FileSystemService`) e metadados (simular `media_parser`).
    2.  **Análise de Arquivo dentro de ZIP:** Criar um arquivo ZIP de teste com um arquivo dentro. Usar `FileAnalyzer` para analisar a entrada do ZIP. Verificar se o `FileInfo` resultante indica que está num ZIP, tem o nome da entrada correto, e se o hash (calculado pelo `HashingService` via `ZipHandlerService`) e metadados estão corretos.
    3.  **Erro ao Analisar Arquivo Inexistente:** Tentar analisar um arquivo que não existe e verificar se o `FileAnalyzer` lida com o erro graciosamente (ex: loga o erro e retorna `None` ou lança uma exceção específica).
    4.  **Configuração Afetando Análise (se aplicável):** Se alguma configuração do `ConfigurationService` (ex: tipos de arquivo a ignorar, embora não especificado) pudesse afetar o `FileAnalyzer`, testar esse fluxo.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y` para gerar testes para estes cenários. Após os testes passarem e serem validados, prossiga.

---

8.  **`fotix.core.duplicate_finder.DuplicateFinderAlgorithm`**
    *   **Descrição de Alto Nível Inicial:** Receber uma lista de `FileInfo` e identificar grupos de arquivos duplicados baseados em seus hashes e tamanhos (com pré-filtragem por tamanho).
    *   **Justificativa da Ordem:** Lógica central para encontrar duplicatas, consome a saída do `FileAnalyzer`.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.domain.models.FileInfo`, `fotix.domain.models.DuplicateGroup`, `fotix.infrastructure.logging_impl.LoggingService`.

9.  **`fotix.core.decision_engine.DecisionEngine`**
    *   **Descrição de Alto Nível Inicial:** Aplicar lógica para decidir qual arquivo manter de um `DuplicateGroup`, com base em critérios como resolução, data, nome.
    *   **Justificativa da Ordem:** Define qual arquivo é o "original" ou "melhor" dentro de um conjunto de duplicatas.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.domain.models.FileInfo`, `fotix.domain.models.DuplicateGroup`, `fotix.infrastructure.logging_impl.LoggingService`.

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (LÓGICA DE DUPLICATAS E DECISÃO) <<<**

*   **Módulos Implementados neste Grupo:** `fotix.core.duplicate_finder.DuplicateFinderAlgorithm`, `fotix.core.decision_engine.DecisionEngine`.
*   **Objetivo do Teste de Integração:** Validar que, dada uma lista de `FileInfo` (alguns duplicados, outros únicos), o `DuplicateFinderAlgorithm` agrupa corretamente as duplicatas e o `DecisionEngine` seleciona o arquivo correto para manter em cada grupo.
*   **Cenários Chave para Teste de Integração:**
    1.  **Identificação de Duplicatas Simples:** Fornecer uma lista de `FileInfo` com dois arquivos idênticos (mesmo hash e tamanho) e alguns únicos. Verificar se `DuplicateFinderAlgorithm` cria um `DuplicateGroup` contendo os dois arquivos idênticos e não inclui os únicos.
    2.  **Múltiplos Grupos de Duplicatas:** Fornecer `FileInfo` para dois conjuntos de duplicatas (ex: A1, A2, A3 são duplicatas; B1, B2 são duplicatas). Verificar se dois `DuplicateGroup`s são formados corretamente.
    3.  **Decisão Baseada em Critério Único:** Criar um `DuplicateGroup` com dois arquivos onde um é claramente "melhor" por um critério (ex: data de modificação mais recente). Passar para o `DecisionEngine` e verificar se o arquivo correto é escolhido para `file_to_keep`.
    4.  **Decisão com Critérios Múltiplos (Ponderados):** Criar um `DuplicateGroup` onde a decisão envolve múltiplos critérios (ex: data vs. padrão de nome). Configurar os pesos em `ScanSettings` (que seria passado para o `DecisionEngine`) e verificar se a escolha reflete a ponderação. (Nota: A interação com `ScanSettings` pode ser simulada/mockada aqui se o `ScanOrchestrationService` ainda não estiver pronto).
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y` para gerar testes para estes cenários. Após os testes passarem e serem validados, prossiga.

---

10. **`fotix.infrastructure.concurrency_impl.ConcurrencyService`**
    *   **Descrição de Alto Nível Inicial:** Implementar a interface `IConcurrencyService` para abstrair a execução paralela de tarefas (usando `concurrent.futures`).
    *   **Justificativa da Ordem:** Será usado pelo `ScanOrchestrationService` para paralelizar a análise de arquivos, melhorando o desempenho.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.logging_impl.LoggingService`, interface `IConcurrencyService`.

11. **`fotix.infrastructure.backup_manager_impl.BackupManagerService`**
    *   **Descrição de Alto Nível Inicial:** Implementar a interface `IBackupManagerService` para gerenciar o backup de arquivos antes da remoção e a restauração, incluindo um log/índice dos backups.
    *   **Justificativa da Ordem:** Essencial para a segurança dos dados antes que o `ScanOrchestrationService` execute remoções.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.file_system_impl.FileSystemService`, `fotix.domain.models.BackupLogEntry`, `fotix.domain.models.FileInfo`, `fotix.infrastructure.logging_impl.LoggingService`, interface `IBackupManagerService`.

12. **`fotix.application.services.backup_restore_service.BackupRestoreService`**
    *   **Descrição de Alto Nível Inicial:** Lidar com as operações de listagem de backups e restauração de arquivos, utilizando o `BackupManagerService`.
    *   **Justificativa da Ordem:** Fornece a lógica de aplicação para as funcionalidades de backup e restauração.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.backup_manager_impl.BackupManagerService`, `fotix.infrastructure.logging_impl.LoggingService`, `fotix.domain.models` (para estruturas de dados, se necessário).

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (CONCORRÊNCIA E GERENCIAMENTO DE BACKUP/RESTAURAÇÃO) <<<**

*   **Módulos Implementados neste Grupo:** `fotix.infrastructure.concurrency_impl.ConcurrencyService`, `fotix.infrastructure.backup_manager_impl.BackupManagerService`, `fotix.application.services.backup_restore_service.BackupRestoreService`.
*   **Objetivo do Teste de Integração:** Validar a funcionalidade de backup e restauração de arquivos, e a capacidade do `ConcurrencyService` de executar tarefas em paralelo.
*   **Cenários Chave para Teste de Integração:**
    1.  **Backup e Listagem:** Criar um arquivo de teste. Usar `BackupRestoreService` (que usa `BackupManagerService`) para fazer backup do arquivo. Listar os backups e verificar se o arquivo consta na lista e se o arquivo físico de backup foi criado no local correto.
    2.  **Backup e Restauração para Local Original:** Fazer backup de um arquivo. Simular sua "remoção" do local original. Usar `BackupRestoreService` para restaurá-lo ao local original. Verificar se o arquivo foi restaurado corretamente.
    3.  **Execução de Tarefas Paralelas Simples:** Criar algumas funções simples que simulam trabalho (ex: `time.sleep(0.1)` e retornam um valor). Usar `ConcurrencyService` para executá-las em paralelo. Verificar se os resultados são retornados corretamente e se o tempo total é menor do que a execução sequencial.
    4.  **Restauração para Novo Local:** Fazer backup de um arquivo. Usar `BackupRestoreService` para restaurá-lo para um novo local especificado. Verificar se o arquivo foi restaurado no novo local.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y` para gerar testes para estes cenários. Após os testes passarem e serem validados, prossiga.

---

13. **`fotix.application.services.scan_orchestration_service.ScanOrchestrationService`**
    *   **Descrição de Alto Nível Inicial:** Orquestrar todo o fluxo de varredura: listar arquivos, analisar, encontrar duplicatas, aplicar decisões, e preparar para remoção com backup. Usará callbacks para notificar progresso.
    *   **Justificativa da Ordem:** Um dos principais serviços da aplicação, integra muitos dos componentes core e de infraestrutura já desenvolvidos.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.core.file_analyzer.FileAnalyzer`, `fotix.core.duplicate_finder.DuplicateFinderAlgorithm`, `fotix.core.decision_engine.DecisionEngine`, `fotix.infrastructure.file_system_impl.FileSystemService`, `fotix.infrastructure.zip_handler_impl.ZipHandlerService`, `fotix.infrastructure.concurrency_impl.ConcurrencyService`, `fotix.infrastructure.backup_manager_impl.BackupManagerService`, `fotix.infrastructure.logging_impl.LoggingService`, `fotix.domain.models` (para `ScanSettings`, `ScanResult`, etc.).

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (FLUXO DE VARREDURA COMPLETO SEM REMOÇÃO) <<<**

*   **Módulos Implementados neste Grupo:** `fotix.application.services.scan_orchestration_service.ScanOrchestrationService`.
*   **Objetivo do Teste de Integração:** Validar o fluxo completo de varredura orquestrado pelo `ScanOrchestrationService`, desde a listagem de arquivos até a identificação de duplicatas e a decisão de quais manter/remover, *sem* executar a remoção/backup ainda.
*   **Cenários Chave para Teste de Integração:**
    1.  **Varredura de Diretório com Duplicatas:** Preparar um diretório com alguns arquivos únicos e alguns grupos de duplicatas. Executar `perform_scan` do `ScanOrchestrationService`. Verificar se o `ScanResult` contém a contagem correta de arquivos processados, os `DuplicateGroup`s corretos com os arquivos `file_to_keep` e `files_to_remove` adequadamente preenchidos.
    2.  **Varredura Incluindo Arquivos ZIP:** Adicionar um arquivo ZIP com duplicatas internas e/ou duplicatas de arquivos externos ao diretório de teste. Executar `perform_scan`. Verificar se os arquivos dentro do ZIP são processados e incluídos nos `DuplicateGroup`s corretamente.
    3.  **Callbacks de Progresso e Resultados:** Implementar callbacks mock para `progress_callback` e `duplicate_group_processed_callback` em `ScanSettings`. Executar `perform_scan` e verificar se os callbacks são chamados com os dados esperados durante o processo.
    4.  **Varredura com Diretório Vazio ou Sem Duplicatas:** Executar `perform_scan` em um diretório vazio ou com apenas arquivos únicos. Verificar se o `ScanResult` é retornado corretamente (sem duplicatas, contagem de arquivos processados correta).
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y` para gerar testes para estes cenários. Após os testes passarem e serem validados, prossiga.

---

14. **Testes da funcionalidade `process_duplicates_for_removal` do `ScanOrchestrationService`** (Esta é uma extensão do módulo anterior, focando em uma parte específica).
    *   **Descrição de Alto Nível Inicial:** Focar especificamente na parte do `ScanOrchestrationService` que lida com o backup e remoção segura dos arquivos marcados em `files_to_remove` nos `DuplicateGroup`s.
    *   **Justificativa da Ordem:** É a ação final e destrutiva (embora com backup) do fluxo de varredura, necessitando de testes cuidadosos após a lógica de identificação estar validada.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.infrastructure.backup_manager_impl.BackupManagerService`, `fotix.infrastructure.file_system_impl.FileSystemService`.

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (PROCESSAMENTO DE REMOÇÃO DE DUPLICATAS) <<<**

*   **Módulos Implementados neste Grupo:** Foco na funcionalidade `process_duplicates_for_removal` do `fotix.application.services.scan_orchestration_service.ScanOrchestrationService`.
*   **Objetivo do Teste de Integração:** Validar que o `ScanOrchestrationService` pode corretamente fazer backup e remover os arquivos marcados para exclusão.
*   **Cenários Chave para Teste de Integração:**
    1.  **Remoção e Backup de Duplicata Única:** Criar um `DuplicateGroup` simples com um arquivo para manter e um para remover. Chamar `process_duplicates_for_removal`. Verificar se o arquivo a ser removido foi movido para o backup (`BackupManagerService`) e depois removido do local original (`FileSystemService.delete_file_safe`).
    2.  **Remoção e Backup de Múltiplas Duplicatas em Múltiplos Grupos:** Criar uma lista de `DuplicateGroup`s. Chamar `process_duplicates_for_removal`. Verificar se todos os arquivos marcados para remoção são processados corretamente.
    3.  **Falha no Backup Impede Remoção (Simulado):** Mockar o `BackupManagerService.backup_file` para falhar para um arquivo específico. Chamar `process_duplicates_for_removal`. Verificar se o arquivo não foi removido do local original e se o erro foi logado.
    4.  **Verificar Espaço Salvo Retornado:** Após uma remoção bem-sucedida, verificar se o valor de `total_space_saved` retornado por `process_duplicates_for_removal` está correto.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y` para gerar testes para estes cenários. Após os testes passarem e serem validados, prossiga.

---

15. **`fotix.application.services.reporting_service.ReportingService`**
    *   **Descrição de Alto Nível Inicial:** Gerar relatórios resumidos e estatísticas com base nos resultados da varredura (`ScanResult`).
    *   **Justificativa da Ordem:** Uma funcionalidade complementar que usa os resultados da varredura. Pode ser implementada após o fluxo principal estar funcional.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.domain.models.ScanResult`, `fotix.infrastructure.logging_impl.LoggingService`, `fotix.infrastructure.file_system_impl.FileSystemService` (para salvar relatórios).

16. **`fotix.ui.views.settings_view.SettingsView`**
    *   **Descrição de Alto Nível Inicial:** Permitir ao usuário configurar diretórios para varredura, arquivos ZIP e critérios de decisão (se aplicável), interagindo com `ConfigurationService` e `ScanOrchestrationService`.
    *   **Justificativa da Ordem:** Uma das primeiras interações do usuário, fornece os inputs para a varredura.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.application.services.configuration_service.ConfigurationService`, `fotix.application.services.scan_orchestration_service.ScanOrchestrationService`.

17. **`fotix.ui.views.scan_progress_view.ScanProgressView`**
    *   **Descrição de Alto Nível Inicial:** Exibir o progresso da varredura e permitir cancelamento, recebendo atualizações do `ScanOrchestrationService`.
    *   **Justificativa da Ordem:** Fornece feedback ao usuário durante a operação principal da aplicação.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.application.services.scan_orchestration_service.ScanOrchestrationService`.

18. **`fotix.ui.views.results_view.ResultsView`**
    *   **Descrição de Alto Nível Inicial:** Apresentar os grupos de arquivos duplicados encontrados, mostrando qual será mantido e quais serão removidos/foram removidos.
    *   **Justificativa da Ordem:** Exibe o resultado da operação principal para o usuário.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.application.services.scan_orchestration_service.ScanOrchestrationService`, `fotix.application.services.reporting_service.ReportingService`.

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (UI: FLUXO DE VARREDURA) <<<**

*   **Módulos Implementados neste Grupo:** `fotix.application.services.reporting_service.ReportingService`, `fotix.ui.views.settings_view.SettingsView`, `fotix.ui.views.scan_progress_view.ScanProgressView`, `fotix.ui.views.results_view.ResultsView`.
*   **Objetivo do Teste de Integração:** Validar a interação da UI (configurações, progresso, resultados) com os serviços de aplicação subjacentes para o fluxo de varredura. Testes aqui seriam mais focados na passagem de dados e chamadas de método, não necessariamente em testes de UI visuais automatizados complexos, a menos que o `Prompt_IntegradorTester` suporte isso.
*   **Cenários Chave para Teste de Integração:**
    1.  **Configurar e Iniciar Varredura:** Simular a entrada do usuário na `SettingsView`, verificar se as `ScanSettings` são corretamente passadas para o `ScanOrchestrationService` ao iniciar uma varredura.
    2.  **Exibição de Progresso:** Mockar o `ScanOrchestrationService` para emitir sinais/callbacks de progresso. Verificar se a `ScanProgressView` os recebe e (simuladamente) atualiza sua exibição.
    3.  **Exibição de Resultados:** Mockar o `ScanOrchestrationService` para retornar um `ScanResult`. Verificar se a `ResultsView` recebe esses dados e (simuladamente) os exibe corretamente.
    4.  **Geração de Relatório a partir da UI (se aplicável):** Se a `ResultsView` tiver um botão para gerar relatório, verificar se ele chama o `ReportingService` corretamente.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y` para gerar testes para estes cenários. Dada a natureza da UI, estes testes podem focar em verificar se os serviços corretos são chamados com os dados corretos, em vez de interações visuais. Após os testes passarem e serem validados, prossiga.

---

19. **`fotix.ui.views.backup_restore_view.BackupRestoreView`**
    *   **Descrição de Alto Nível Inicial:** Listar backups disponíveis e permitir ao usuário selecionar arquivos/pastas para restauração, interagindo com `BackupRestoreService`.
    *   **Justificativa da Ordem:** Implementa a UI para a funcionalidade de restauração.
    *   **Dependências Chave (Inferidas do Blueprint):** `fotix.application.services.backup_restore_service.BackupRestoreService`.

20. **`fotix.ui.main_window.FotixMainWindow`**
    *   **Descrição de Alto Nível Inicial:** Janela principal da aplicação, orquestrando as diferentes views e interações com os serviços da camada de aplicação.
    *   **Justificativa da Ordem:** Integra todas as views e funcionalidades da aplicação em uma interface coesa.
    *   **Dependências Chave (Inferidas do Blueprint):** Todas as views (`SettingsView`, `ScanProgressView`, `ResultsView`, `BackupRestoreView`) e os principais serviços de aplicação (`ScanOrchestrationService`, `BackupRestoreService`, `ReportingService`, `ConfigurationService`).

---

**>>> PARADA PARA TESTES DE INTEGRAÇÃO (UI: FLUXO DE BACKUP/RESTAURAÇÃO E INTEGRAÇÃO GERAL DA UI) <<<**

*   **Módulos Implementados neste Grupo:** `fotix.ui.views.backup_restore_view.BackupRestoreView`, `fotix.ui.main_window.FotixMainWindow`.
*   **Objetivo do Teste de Integração:** Validar a interação da UI para backup/restauração e a orquestração geral das views pela `FotixMainWindow`.
*   **Cenários Chave para Teste de Integração:**
    1.  **Listar Backups na UI:** Mockar o `BackupRestoreService` para retornar uma lista de `BackupLogEntry`. Verificar se a `BackupRestoreView` (simuladamente) exibe essa lista.
    2.  **Iniciar Restauração da UI:** Simular a seleção de um item de backup na `BackupRestoreView` e o acionamento da restauração. Verificar se o `BackupRestoreService` é chamado com os parâmetros corretos.
    3.  **Navegação entre Views na MainWindow:** Verificar se a `FotixMainWindow` pode (simuladamente) alternar entre as diferentes views (`SettingsView`, `ResultsView`, etc.) conforme o fluxo da aplicação.
    4.  **Disponibilidade de Serviços na MainWindow:** Verificar se a `FotixMainWindow` tem acesso e pode invocar (ou passar para as views) os serviços de aplicação necessários.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y` para gerar testes para estes cenários, com foco na lógica de interação e passagem de dados. Após os testes passarem e serem validados, a implementação inicial dos módulos principais estará concluída.

---