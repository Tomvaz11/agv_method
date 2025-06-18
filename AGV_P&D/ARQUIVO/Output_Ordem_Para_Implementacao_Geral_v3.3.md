## Análise de Implementação e Próximos Passos para Fotix v5.0

**Instruções para o Coordenador:**

Este documento organiza os módulos do projeto Fotix para guiar a implementação. Ele separa os "Módulos Base" (definições, utilitários e interfaces) dos "Módulos Principais" (que contêm a lógica central e as implementações concretas dos serviços).

*   **NÃO implemente os "Módulos Base" listados abaixo diretamente agora.** Suas pastas e arquivos básicos (como `__init__.py`, arquivos de interfaces contendo os ABCs, e modelos de dados Pydantic) serão criados ou modificados quando necessário pela IA (`ImplementadorMestre`) durante a implementação dos módulos principais que dependem deles. O conteúdo específico de módulos como `fotix.utils` será adicionado organicamente conforme a necessidade surgir.
*   **SIGA a "Ordem de Implementação Sugerida (Módulos Principais e Pontos de Teste de Integração)" abaixo.** Comece pelo **Item #1** da lista de Módulos Principais e prossiga sequencialmente.
*   Para **CADA item** da ordem numerada de Módulo Principal, use o `Prompt_ImplementadorMestre_vX.Y` (recomenda-se a versão mais recente, ex: v1.7+), preenchendo apenas o nome do módulo alvo (ex: "Item 1: `fotix.infrastructure.implementations.logging_service`"). Anexe sempre o `@Blueprint_Arquitetural.md`, este arquivo (`@Ordem_Com_Descricoes_e_Testes_Integracao.md`) e o código relevante já existente como contexto. A "Descrição de Alto Nível Inicial" listada abaixo para cada item servirá como ponto de partida para a IA.
*   **PONTOS DE TESTE DE INTEGRAÇÃO:** Em certos pontos, este documento indicará uma **">>> PARADA PARA TESTES DE INTEGRAÇÃO (Nome do Subsistema) <<<"**. Nestes momentos, **antes de prosseguir** com o próximo Módulo Principal da lista, você deverá usar um prompt dedicado para testes de integração (ex: `Prompt_IntegradorTester_vX.Y`, que será definido posteriormente) para guiar a IA na criação e execução de testes de integração para o grupo de módulos recém-concluído. Utilize os "Cenários Chave para Teste de Integração" listados como ponto de partida para esses testes. Após os testes de integração serem concluídos e validados, você poderá prosseguir para o próximo item da ordem de implementação.

---

### Módulos Base (Estrutura Inicial / Conteúdo On-Demand)

*   **`fotix.domain.models`**: Define as estruturas de dados centrais da aplicação (ex: `FileEntry`, `DuplicateSet`, `ScanConfig`, `AppConfig`) usando Pydantic.
*   **`fotix.infrastructure.interfaces`**: Contém todos os arquivos de interfaces (ABCs) que definem os contratos para os serviços de infraestrutura (ex: `IFileSystemService`, `IHashingService`, `IBackupService`, etc.).
*   **`fotix.utils.helpers`**: Conterá funções auxiliares genéricas que podem ser necessárias em várias partes do código.
*   **`fotix.app_config`**: Responsável pela lógica de carregar, validar e fornecer o objeto de configuração `AppConfig` para o resto da aplicação durante o bootstrapping.

---

### Ordem de Implementação Sugerida (Módulos Principais e Pontos de Teste de Integração) - COMECE AQUI (Item #1)

1.  **`fotix.infrastructure.implementations.logging_service`**
    *   **Descrição de Alto Nível Inicial:** Implementa a interface `ILoggingService`, configurando e fornecendo uma interface para o sistema de logging padrão do Python.
    *   **Justificativa da Ordem:** É o serviço mais fundamental. Ter logging funcional desde o início é crucial para a depuração e monitoramento de todos os outros componentes que serão desenvolvidos.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** Nenhuma (apenas biblioteca padrão).

2.  **`fotix.infrastructure.implementations.hashing_service`**
    *   **Descrição de Alto Nível Inicial:** Implementa a interface `IHashingService`, abstraindo o cálculo de hash de arquivos usando a biblioteca BLAKE3.
    *   **Justificativa da Ordem:** É um serviço de infraestrutura de baixo nível, com dependência apenas do logger, e é um pré-requisito para o `DuplicateFinderEngine` e o `ZipService`.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** Nenhuma (apenas biblioteca da stack).

3.  **`fotix.infrastructure.implementations.file_system_service`**
    *   **Descrição de Alto Nível Inicial:** Implementa a interface `IFileSystemService`, abstraindo todas as operações de sistema de arquivos como listar, copiar e mover para a lixeira.
    *   **Justificativa da Ordem:** É um serviço de infraestrutura essencial, dependente apenas do logger, e serve de base para quase todos os outros serviços da aplicação.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** Nenhuma (apenas bibliotecas padrão/stack definida).

4.  **`fotix.infrastructure.implementations.concurrency_service`**
    *   **Descrição de Alto Nível Inicial:** Implementa a interface `IConcurrencyService`, abstraindo o uso de `concurrent.futures` para a execução paralela de tarefas.
    *   **Justificativa da Ordem:** Serviço de infraestrutura fundamental para a performance do escaneamento. É independente de outros serviços de negócio e pode ser implementado no início.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** Nenhuma (apenas bibliotecas padrão).

---
**>>> PARADA PARA TESTES DE INTEGRAÇÃO (INFRAESTRUTURA BÁSICA) <<<**

*   **Módulos Implementados neste Grupo:** `LoggingService`, `HashingService`, `FileSystemService`, `ConcurrencyService` (e seus módulos base associados, como as interfaces em `fotix.infrastructure.interfaces`).
*   **Objetivo do Teste de Integração:** Validar que os serviços de infraestrutura fundamentais operam corretamente e se integram entre si (especialmente com o `LoggingService`).
*   **Cenários Chave para Teste de Integração:**
    1.  **Hashing com Log:** Criar um arquivo de teste usando o `FileSystemService`. Calcular seu hash usando o `HashingService` e verificar se o hash está correto e se a operação foi devidamente registrada pelo `LoggingService`.
    2.  **Listagem de Arquivos:** Usar o `FileSystemService` para listar arquivos em um diretório de teste (contendo subdiretórios) e verificar se a lista retornada está correta.
    3.  **Execução Paralela Simples:** Usar o `ConcurrencyService` para executar uma tarefa simples (ex: uma função que dorme por um curto período) em paralelo para múltiplos itens e verificar se os resultados são coletados corretamente.
    4.  **Tratamento de Erro:** Tentar usar o `FileSystemService` em um caminho inexistente e verificar se uma exceção é tratada e se um log de ERRO é gerado pelo `LoggingService`.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y` (a ser definido) para gerar testes para estes cenários. Após os testes passarem e serem validados, prossiga para o próximo item da ordem de implementação.
---

5.  **`fotix.domain.core.selection_strategy`**
    *   **Descrição de Alto Nível Inicial:** Implementa o algoritmo inteligente para decidir qual arquivo manter de um conjunto de duplicatas, com base em critérios como resolução, data ou nome.
    *   **Justificativa da Ordem:** É um componente de lógica de negócio pura, sem dependências de infraestrutura, e é necessário para o `DuplicateManagementService`. Implementá-lo agora isola essa lógica complexa.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** `fotix.domain.models`.

6.  **`fotix.domain.core.duplicate_finder`**
    *   **Descrição de Alto Nível Inicial:** Implementa a lógica central de identificação de duplicatas, agrupando arquivos com base em tamanho e hash.
    *   **Justificativa da Ordem:** É o coração da lógica de detecção. Depende dos serviços de infraestrutura já criados (`HashingService`, `FileSystemService`) e deve ser implementado antes do `ScanService`, que o utiliza.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** `fotix.domain.models`, `fotix.application.interfaces.IHashingService`, `fotix.application.interfaces.IFileSystemService`.

7.  **`fotix.infrastructure.implementations.zip_service`**
    *   **Descrição de Alto Nível Inicial:** Implementa a interface `IZipService` para extrair e processar arquivos de dentro de arquivos ZIP de forma progressiva (streaming).
    *   **Justificativa da Ordem:** Depende do `HashingService` para hashear os arquivos extraídos em memória. É um pré-requisito direto para o `ScanService`.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** Nenhuma (apenas biblioteca da stack).

8.  **`fotix.application.services.scan_service`**
    *   **Descrição de Alto Nível Inicial:** Orquestra todo o processo de escaneamento, coordenando os serviços de sistema de arquivos, ZIP, concorrência, hashing e o motor de busca de duplicatas.
    *   **Justificativa da Ordem:** Este é o primeiro grande serviço de orquestração. Ele integra múltiplos componentes de infraestrutura e domínio que já foram implementados, formando a espinha dorsal da principal funcionalidade da aplicação.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** `fotix.application.interfaces.IFileSystemService`, `fotix.application.interfaces.IZipService`, `fotix.application.interfaces.IConcurrencyService`, `fotix.application.interfaces.IHashingService`, `fotix.application.interfaces.ILoggingService`, `fotix.domain.core.DuplicateFinderEngine`, `fotix.domain.models`.

---
**>>> PARADA PARA TESTES DE INTEGRAÇÃO (WORKFLOW DE ESCANEAMENTO COMPLETO) <<<**

*   **Módulos Implementados neste Grupo:** `SelectionStrategy`, `DuplicateFinderEngine`, `ZipService`, `ScanService`.
*   **Objetivo do Teste de Integração:** Garantir que o `ScanService` pode orquestrar com sucesso todos os serviços subjacentes para encontrar corretamente conjuntos de arquivos duplicados em um cenário realista.
*   **Cenários Chave para Teste de Integração:**
    1.  **Escaneamento de Diretório Simples:** Executar o `ScanService` em um diretório com vários arquivos duplicados e únicos. Verificar se o resultado é uma lista de `DuplicateSet` contendo os arquivos corretos.
    2.  **Escaneamento com ZIP:** Executar o `ScanService` em um diretório contendo um arquivo ZIP com imagens duplicadas (tanto dentro do ZIP quanto com arquivos fora do ZIP). Verificar se as duplicatas são identificadas corretamente.
    3.  **Escaneamento com Filtro de Extensão:** Configurar o `ScanService` para escanear apenas por `.jpg` e `.png` e verificar se arquivos de outras extensões são ignorados.
    4.  **Escaneamento Vazio:** Executar o `ScanService` em um diretório vazio ou sem arquivos correspondentes e garantir que ele termina graciosamente retornando uma lista vazia.
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y` (a ser definido) para gerar testes para estes cenários. Este é um ponto de verificação crítico. Após os testes passarem e serem validados, prossiga.
---

9.  **`fotix.infrastructure.implementations.backup_service`**
    *   **Descrição de Alto Nível Inicial:** Implementa a interface `IBackupService`, gerenciando a cópia de arquivos para um local seguro e mantendo metadados sobre os backups.
    *   **Justificativa da Ordem:** É um serviço de infraestrutura necessário para a remoção segura de arquivos, que será orquestrada pelo `DuplicateManagementService`.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** `fotix.domain.models` (para `BackupRecord`).

10. **`fotix.application.services.duplicate_management_service`**
    *   **Descrição de Alto Nível Inicial:** Gerencia a lógica de aplicar a estratégia de seleção, realizar backups e remover com segurança os arquivos duplicados.
    *   **Justificativa da Ordem:** Este é o segundo grande serviço de orquestração. Ele depende dos resultados do `ScanService` (embora não diretamente) e utiliza os serviços `BackupService`, `FileSystemService` e a `SelectionStrategy` para agir sobre as duplicatas.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** `fotix.application.interfaces.IFileSystemService`, `fotix.application.interfaces.IBackupService`, `fotix.application.interfaces.ILoggingService`, `fotix.domain.core.SelectionStrategy`, `fotix.domain.models`.

11. **`fotix.application.services.restore_service`**
    *   **Descrição de Alto Nível Inicial:** Gerencia o processo de restauração de arquivos a partir de backups criados anteriormente.
    *   **Justificativa da Ordem:** Completa o ciclo de vida do backup, permitindo a recuperação de arquivos. Depende do `BackupService` e `FileSystemService` já implementados.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** `fotix.application.interfaces.IFileSystemService`, `fotix.application.interfaces.IBackupService`, `fotix.application.interfaces.ILoggingService`, `fotix.domain.models`.

---
**>>> PARADA PARA TESTES DE INTEGRAÇÃO (WORKFLOW DE GERENCIAMENTO E RESTAURAÇÃO) <<<**

*   **Módulos Implementados neste Grupo:** `BackupService`, `DuplicateManagementService`, `RestoreService`.
*   **Objetivo do Teste de Integração:** Validar o ciclo completo de gerenciamento de duplicatas: seleção, backup, remoção e restauração.
*   **Cenários Chave para Teste de Integração:**
    1.  **Ciclo Completo de Remoção:** Fornecer um `DuplicateSet` ao `DuplicateManagementService`. Verificar se ele usa a `SelectionStrategy` para escolher um arquivo para manter, se os outros são copiados pelo `BackupService`, e se os arquivos originais são movidos para a lixeira pelo `FileSystemService`.
    2.  **Listagem de Backups:** Chamar o `RestoreService` (ou `BackupService`) para listar os backups disponíveis e verificar se o backup criado no cenário anterior aparece corretamente.
    3.  **Restauração de Arquivo:** Usar o `RestoreService` para restaurar um arquivo do backup e verificar se ele reaparece em seu local original (ou em um novo local especificado).
*   **Instrução para o Coordenador:** Use o `Prompt_IntegradorTester_vX.Y` (a ser definido) para gerar testes para estes cenários. A validação deste fluxo é essencial para a segurança dos dados do usuário. Após a validação, prossiga.
---

12. **`fotix.application.services.configuration_service`**
    *   **Descrição de Alto Nível Inicial:** Gerencia a leitura e escrita das configurações da aplicação em um arquivo, provendo-as para outros serviços.
    *   **Justificativa da Ordem:** Embora fundamental, sua implementação completa (com persistência) é mais necessária agora que a UI será desenvolvida, permitindo que as configurações sejam alteradas pelo usuário.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** `fotix.application.interfaces.IFileSystemService`, `fotix.domain.models` (para o modelo de configuração).

13. **`fotix.application.services.reporting_service`**
    *   **Descrição de Alto Nível Inicial:** Coleta estatísticas e fornece acesso aos logs da aplicação para serem exibidos na UI.
    *   **Justificativa da Ordem:** É um serviço simples que depende apenas do `LoggingService`. É implementado agora como um pré-requisito para as views da UI que exibirão logs.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** `fotix.application.interfaces.ILoggingService`.

14. **`fotix.ui.dialogs.settings_dialog`**
    *   **Descrição de Alto Nível Inicial:** Cria a janela de diálogo que permite ao usuário visualizar e modificar as configurações da aplicação.
    *   **Justificativa da Ordem:** É um bom ponto de partida para a UI, pois é relativamente isolada e permite testar a integração com o `ConfigurationService` antes de construir as telas do fluxo principal.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** `ConfigurationService`.

15. **`fotix.ui.views.directory_selection_view` + `fotix.ui.views.scan_progress_view`**
    *   **Descrição de Alto Nível Inicial:** Implementa a tela inicial onde o usuário seleciona os diretórios para escanear e a tela que exibe o progresso dessa operação.
    *   **Justificativa da Ordem:** Constituem o ponto de partida do fluxo principal do usuário. Implementá-los juntos faz sentido, pois um leva diretamente ao outro e ambos interagem com o `ScanService`.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** `ScanService`, `ConfigurationService`.

16. **`fotix.ui.views.results_view`**
    *   **Descrição de Alto Nível Inicial:** Apresenta os conjuntos de duplicatas encontrados, permitindo ao usuário revisar as seleções e confirmar a remoção.
    *   **Justificativa da Ordem:** É a tela principal de resultados e a mais complexa da UI. Deve ser implementada após o fluxo de escaneamento estar funcional, pois depende dos seus resultados e do `DuplicateManagementService` para as ações.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** `DuplicateManagementService`.

17. **`fotix.ui.views.backup_restore_view` + `fotix.ui.views.log_view`**
    *   **Descrição de Alto Nível Inicial:** Implementa as telas para listar e restaurar backups e para exibir os logs da aplicação.
    *   **Justificativa da Ordem:** São funcionalidades secundárias, porém importantes. Podem ser implementadas após o fluxo principal (escanear -> gerenciar) estar completo.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** `RestoreService` (para BackupRestoreView), `ReportingService` (para LogView).

18. **`fotix.ui.main_window`**
    *   **Descrição de Alto Nível Inicial:** Implementa a janela principal da aplicação, que atua como o contêiner e orquestrador para todas as outras views e dialogs.
    *   **Justificativa da Ordem:** É o último componente, pois sua função é integrar todas as views e serviços que já foram criados e testados, formando a aplicação coesa final.
    *   **Dependências Diretas (Conforme Blueprint Arquitetural):** `ScanService`, `DuplicateManagementService`, `RestoreService`, `ConfigurationService`.