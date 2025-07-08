# Output: Ordem de Implementação e Testes de Integração

A seguir estão as diretrizes para o Coordenador e a ordem de implementação sequencial para os Desenvolvedores, baseada na análise do `@Blueprint_Arquitetural.md`.

---

### Módulos Base para Implementação

*   Alvo 0: Setup do Projeto Profissional
*   `fotix.domain.models`
*   `fotix.application.interfaces`
*   `fotix.domain.logic.keeper_selection`
*   `fotix.infrastructure.logging_service`
*   `fotix.infrastructure.filesystem_service`
*   `fotix.infrastructure.hashing_service`
*   `fotix.infrastructure.concurrency_service`
*   `fotix.infrastructure.backup_service`
*   `fotix.application.services.scan_service`
*   `fotix.ui.settings_view`
*   `fotix.ui.progress_view`
*   `fotix.ui.results_view`
*   `fotix.ui.restore_view`
*   `fotix.ui.main_window`

---

### Ordem de Implementação e Pontos de Teste

1.  **Alvo 0: Setup do Projeto Profissional**
2.  `fotix.domain.models`
3.  `fotix.application.interfaces`
4.  `fotix.domain.logic.keeper_selection`

`>>> PARADA PARA TESTES DE INTEGRAÇÃO (LÓGICA DE DOMÍNIO E CONTRATOS) <<<`
*   **Módulos no Grupo:** `fotix.domain.models`, `fotix.application.interfaces`, `fotix.domain.logic.keeper_selection`.
*   **Objetivo do Teste:** Validar que os modelos de dados são robustos, que a lógica de negócio principal (seleção de "keeper") funciona corretamente em isolamento e que os contratos (interfaces) estão bem definidos para as próximas camadas.
*   **Cenários Chave:**
    1.  **Validação de Modelos:** Instanciar os modelos do Pydantic (`ScanConfig`, `MediaFile`) com dados válidos e inválidos para garantir que as validações e tipos funcionem como esperado.
    2.  **Lógica de Seleção (Resolução):** Criar um `DuplicateSet` com múltiplos `MediaFile` onde a resolução é o critério de desempate. Passar o conjunto para a lógica de `keeper_selection` e verificar se o arquivo com a maior resolução é corretamente identificado como `keeper`.
    3.  **Lógica de Seleção (Data):** Criar um `DuplicateSet` onde as resoluções são idênticas, mas as datas de criação são diferentes. Verificar se a lógica de `keeper_selection` seleciona o arquivo mais antigo como `keeper`.

---
5.  `fotix.infrastructure.logging_service`
6.  `fotix.infrastructure.filesystem_service`
7.  `fotix.infrastructure.hashing_service`
8.  `fotix.infrastructure.concurrency_service`
9.  `fotix.infrastructure.backup_service`
10. `fotix.application.services.scan_service`

`>>> PARADA PARA TESTES DE INTEGRAÇÃO (MECANISMO DE VARREDURA COMPLETO - HEADLESS) <<<`
*   **Módulos no Grupo:** `fotix.infrastructure.*` (todos), `fotix.application.services.scan_service`.
*   **Objetivo do Teste:** Validar o fluxo completo de varredura "headless" (sem UI), garantindo que o `ScanService` orquestre corretamente os serviços de infraestrutura para encontrar, analisar, agrupar e processar duplicatas.
*   **Cenários Chave:**
    1.  **Caminho Feliz (Arquivos Simples):** Criar uma estrutura de diretórios de teste com arquivos duplicados e únicos. Invocar o `ScanService` para executar a varredura e verificar se o `ScanResult` retornado contém o número correto de `DuplicateSet` e se a seleção do "keeper" foi feita.
    2.  **Varredura de Arquivos ZIP:** Criar um diretório de teste contendo um arquivo de imagem e um arquivo ZIP que contém uma cópia dessa mesma imagem. Executar a varredura com `include_zips=True` e verificar se a duplicata entre o arquivo externo e o interno é corretamente identificada.
    3.  **Fluxo de Remoção/Backup:** Após uma varredura bem-sucedida, invocar o método de remoção no `ScanService`. Verificar (usando um `BackupService` real ou mockado) se o arquivo correto (não o "keeper") foi movido para o local de backup e se um `BackupInfo` foi gerado.
    4.  **Varredura Recursiva vs. Não Recursiva:** Preparar um diretório com subdiretórios contendo duplicatas. Executar o `ScanService` com `recursive=False` e verificar se apenas as duplicatas no nível raiz são encontradas. Em seguida, executar com `recursive=True` e verificar se todas as duplicatas são encontradas.

---
11. `fotix.ui.settings_view`
12. `fotix.ui.progress_view`
13. `fotix.ui.results_view`
14. `fotix.ui.restore_view`
15. `fotix.ui.main_window`

`>>> PARADA PARA TESTES DE INTEGRAÇÃO (FLUXO DE USUÁRIO END-TO-END) <<<`
*   **Módulos no Grupo:** `fotix.ui.*` (todos os componentes).
*   **Objetivo do Teste:** Validar a integração completa entre a Camada de Apresentação (UI) e a Camada de Aplicação (`ScanService`), garantindo que o fluxo do usuário, da configuração à ação final, funcione de ponta a ponta.
*   **Cenários Chave:**
    1.  **Fluxo Completo de Varredura e Limpeza:** Usar um driver de teste de UI (ou testes manuais) para: (a) selecionar um diretório na `SettingsView`, (b) iniciar a varredura e observar a `ProgressView`, (c) revisar os resultados na `ResultsView` e (d) confirmar a remoção. Verificar no sistema de arquivos se a operação foi bem-sucedida.
    2.  **Fluxo de Restauração de Backup:** Após executar o cenário anterior, navegar para a `RestoreView`. Verificar se o item removido está listado. Acionar a restauração e confirmar no sistema de arquivos que o arquivo retornou ao seu local original.
    3.  **Comunicação UI-Serviço (Sinais/Slots):** Iniciar uma varredura e verificar se os sinais emitidos pelo `ScanService` (ex: progresso, log de mensagens) estão sendo corretamente capturados e exibidos pelos widgets na `ProgressView`.